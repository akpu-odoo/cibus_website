# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class InheritedPricelist(models.Model):
    _inherit = "product.pricelist"

    def _compute_price_rule(self, products, quantity, currency=None, uom=None, date=False, compute_price=True, **kwargs):
        self.ensure_one()
        website_id = self.env.context.get("website_id")
        if website_id:
            website_id = self.env["website"].browse(website_id)
            orderId = website_id.sale_get_order()
            if orderId.is_checked_out and orderId.delivery_expected_date:
                date = orderId.delivery_expected_date

        return super()._compute_price_rule(
            products, quantity, currency, uom, date, compute_price, **kwargs
        )
