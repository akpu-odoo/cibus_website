from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    show_invoice_button = fields.Boolean(
        string="show invoice button",
        compute="_compute_show_inovice_button",
        store=True,
        default=False,
    )

    @api.depends("sale_id", "partner_id.invoicing_type", "state")
    def _compute_show_inovice_button(self):
        for line in self:
            line.show_invoice_button = False
            if (
                line.state == "done"
                and line.sale_id
                and line.partner_id.invoicing_type == "daily_invoice"
            ):
                line.show_invoice_button = True
