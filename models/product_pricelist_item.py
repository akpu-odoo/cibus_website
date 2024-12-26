# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    nature_price = fields.Char(string="nature of price")

