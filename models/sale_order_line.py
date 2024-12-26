# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    nature_price = fields.Char(related="pricelist_item_id.nature_price")
    product_variant_packaging_id = fields.Many2one("product.packaging", string="Packaging")
    product_variant_packaging_qty = fields.Float(string="Packaging Quantity", related='product_variant_packaging_id.qty')

    @api.depends(
        "product_id",
        "product_uom",
        "product_uom_qty",
        "order_id.delivery_expected_date",
    )
    def _compute_pricelist_item_id(self):
        super()._compute_pricelist_item_id()
        for line in self:
            if line.order_id and line.order_id.delivery_expected_date:
                if (
                    not line.product_id
                    or line.display_type
                    or not line.order_id.pricelist_id
                ):
                    line.pricelist_item_id = False
                else:
                    line.pricelist_item_id = (
                        line.order_id.pricelist_id._get_product_rule(
                            line.product_id,
                            quantity=line.product_uom_qty or 1.0,
                            uom=line.product_uom,
                            date=line.order_id.delivery_expected_date,
                        )
                    )
    