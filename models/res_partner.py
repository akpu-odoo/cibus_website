# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    week_day_ids = fields.Many2many(
        comodel_name="week.day",
        string="Week Days",
        help="Select the days of the week for which this partner is available.",
    )
    invoicing_type = fields.Selection(
        [("daily_invoice", "Daily Invoice"), ("monthly_invoice", "Monthly Invoice")],
        string="Invoicing Type",
    )
