# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request


class WebsiteSaleExpectedDate(http.Controller):

    @http.route("/update_expected_date", type="json", auth="public", methods=["POST"])
    def update_expected_date(self, date):
        """Inherited funcation to update the delivery date in the sale order"""
        website = request.env["website"].get_current_website()
        sale_order = website.sale_get_order()

        if sale_order:
            sale_order.write({"delivery_expected_date": date})
            return {"status": "success", "order_id": sale_order.id}
        return {"status": "error", "message": "Sale order not found"}


class SelectedDayController(http.Controller):

    @http.route("/get_user_selected_days", type="json", auth="user")
    def get_user_selected_days(self):
        """ funcation to get the selected delivery day of login user"""
        user = request.env.user
        locale = user.lang
        locale = locale[:2] or "en"
        selected_day = user.partner_id.week_day_ids.mapped("id")
        return selected_day, locale
