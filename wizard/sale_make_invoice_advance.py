from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        response = super().create_invoices()
        if self.env.context.get("active_model") == "stock.picking":
            invoices = self.env["account.move"].browse(response.get("res_id"))
            invoices.action_post()

            active_picking_id = self.env.context.get("active_id")
            picking_id = self.env["stock.picking"].browse(active_picking_id)
            picking_id.message_post(
                body="Invoice has been generated",
                subject="Invoice Generation",
            )

            mail_template_id = self.env["mail.template"].search(
                [("model", "=", "account.move")]
            )
            mail_template_id = invoices.env.ref(invoices._get_mail_template(), raise_if_not_found=False)
            active_account_move_send_id = (
                self.env["account.move.send"]
                .with_context(default_move_ids=invoices.ids)
                .create(
                    {
                        "move_ids": invoices.ids,
                        "mail_template_id": mail_template_id.id,
                    }
                )
            )
            active_account_move_send_id.action_send_and_print()
        return response
