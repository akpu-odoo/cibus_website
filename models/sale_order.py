# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_expected_date = fields.Date(string="Expected Delivery Date")
    is_checked_out = fields.Boolean(string="Is Checked Out")
    is_delivery_price_updated = fields.Boolean(string="Is price updated")
    deliver_today = fields.Boolean(string="Deliver Today")
    is_delivery_date = fields.Boolean(string="Is delivery Date")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self.ensure_one()
        self.is_delivery_date = False

    @api.onchange("delivery_expected_date", "pricelist_id")
    def _onchange_delivery_expected_date(self):
        self.ensure_one()
        if self.delivery_expected_date:
            self.is_delivery_price_updated = True

    @api.model
    def get_allowed_days(self, order_id):
        """Fetches the allowed delivery days based on the customer's
        preferred days and the 'deliver today' flag.
        """
        allowed_days = []
        deliver_today = False
        if order_id:
            order = self.env["sale.order"].browse(order_id)
            allowed_days = order.partner_id.week_day_ids.mapped("id")
            deliver_today = order.deliver_today
        return {"allowed_days": allowed_days, "deliver_today": deliver_today}

    def action_confirm(self):
        """Confirm the sale order and check if the delivery price has been updated."""
        self.ensure_one()

        if self.is_delivery_price_updated:
            raise UserError(
                "Prices are not updated. Please update prices before confirming."
            )

        if self.delivery_expected_date:
            # Set the commitment date to the expected delivery date.
            self.write({"commitment_date": self.delivery_expected_date})

        return super(SaleOrder, self).action_confirm()

    def update_orderline_price(self):
        """Update the price for each order line based on the expected delivery date."""
        self.ensure_one()
        pricelist_id = self.pricelist_id
        order_lines = self.order_line
        self.is_delivery_price_updated = False

        if not self.delivery_expected_date:
            return

        for orderline in order_lines:
            product = orderline.product_id
            if product:
                current_price = pricelist_id._compute_price_rule(
                    product, orderline.product_uom_qty, date=self.delivery_expected_date
                )
                orderline.price_unit = current_price[product.id][0]

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if "partner_id" in vals:
            self.is_delivery_date = True
        return res

    def create(self, vals):
        for val in vals:
            if 'partner_id' in val:
                val['is_delivery_date'] = True
        return super(SaleOrder, self).create(vals)

    @api.depends("order_line.product_uom_qty", "order_line.product_id")
    def _compute_cart_info(self):
        """Displayed Cart Quantity According to Variant Packaging"""
        super()._compute_cart_info()
        for order in self:
            total = 0
            for line in order.website_order_line:
                total += line.product_uom_qty / (line.product_variant_packaging_qty or 1)
            order.cart_quantity = total

    def _cart_find_product_line(self, product_id, line_id=None, **kwargs):
        SaleOrderLine = super()._cart_find_product_line(product_id, line_id, **kwargs) 
        """Filter Variant Packaging id in Sale Order Line According to Selected Variant Packaging"""
        if  kwargs.get("product_variant_packaging_id"):
            if kwargs.get("product_variant_packaging_id") == 'false':
                SaleOrderLine = SaleOrderLine.filtered(lambda l: not l.product_variant_packaging_id.id)
            else:
                current_packaging_id = int(kwargs.get("product_variant_packaging_id"))
                SaleOrderLine = SaleOrderLine.filtered(
                    lambda l: l.product_variant_packaging_id.id == current_packaging_id
                )
        return SaleOrderLine

    def _cart_update_order_line(self, product_id, quantity, order_line, **kwargs):
        """Update Variant Packaging id in Sale Order Line According to Selected Variant Packaging"""
        if order_line:
            if kwargs.get("product_variant_packaging_id") and kwargs.get("product_variant_packaging_id") != 'false':
                order_line.product_variant_packaging_id =  int(kwargs.get("product_variant_packaging_id"))
                quantity  = order_line.product_uom_qty + (quantity - order_line.product_uom_qty) * order_line.product_variant_packaging_qty 
            else:
                quantity = quantity * (order_line.product_variant_packaging_qty or 1)
        else:
            if kwargs.get("product_variant_packaging_id") and kwargs.get("product_variant_packaging_id") != 'false':
                packaging_id = self.env["product.packaging"].browse(int(kwargs.get("product_variant_packaging_id")))
                quantity = quantity * (packaging_id.qty or 1)
        response =  super()._cart_update_order_line(
            product_id, quantity, order_line, **kwargs
        )
        if kwargs.get("product_variant_packaging_id") and kwargs.get("product_variant_packaging_id") != 'false' and response:
            response.product_variant_packaging_id =  int(kwargs.get("product_variant_packaging_id"))
        return response
