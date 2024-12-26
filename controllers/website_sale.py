# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.website.controllers.main import Website

class CustomWebsiteSale(WebsiteSale):

    @http.route(["/shop/confirmation"], type="http", auth="public", website=True, sitemap=False)
    def shop_payment_confirmation(self, **post):
        """Inherited funcation to update the commitment date of sale order"""
        sale_order_id = request.session.get("sale_last_order_id")
        if sale_order_id:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
            if order.delivery_expected_date:
                order.commitment_date = order.delivery_expected_date
        return super().shop_payment_confirmation(**post)

    @http.route("/shop/cart/popover", type="json", auth="public", methods=["POST"], website=True)
    def cart_checkout_popover(self, **post):
        website_id = request.env.context.get("website_id")
        website = request.env["website"].browse(website_id)
        order = website.sale_get_order()

        if not order.delivery_expected_date:
            return self._render_cart_popup(False)

        changed_product_price, total_price = self._get_changed_product_prices(order)

        if not changed_product_price:
            return

        return self._render_cart_popup(True, changed_product_price, total_price)

    def _get_changed_product_prices(self, order):
        """function to calculate changed product prices and total price."""
        changed_product_price = []
        total_price = 0

        for line in order.order_line:
            product = line.product_id
            if not product:
                continue

            qty = line.product_uom_qty
            old_price = round(line.price_unit, 2)
            current_price = self._get_current_price(order, product, qty)

            total_price += qty * current_price
            if old_price != current_price:
                changed_product_price.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "old_price": old_price,
                    "new_price": current_price,
                    "qty": qty,
                })

        return changed_product_price, total_price

    def _get_current_price(self, order, product, qty):
        """Function to compute the current price of a product."""
        pricelist_price = order.pricelist_id._compute_price_rule(product, qty, date=order.delivery_expected_date)
        return round(pricelist_price[product.id][0], 2)

    def _render_cart_popup(self, delivery_date_available, changed_product_price=None, total_price=None):
        """Function to render the popup template."""
        context = {
            "response": "success",
            "delivery_date_available": delivery_date_available,
        }
        if changed_product_price is not None:
            context["changed_product_price"] = changed_product_price
        if total_price is not None:
            context["total_price"] = round(total_price, 2)

        return request.env["ir.ui.view"]._render_template("cibus_website.cart_popup_template", context)


class WebsiteSale(payment_portal.PaymentPortal):

    @http.route(["/shop/checkout"], type="http", auth="public", website=True, sitemap=False)
    def checkout(self, **post):
        order = request.website.sale_get_order()
        order.is_checked_out = True
        return super().checkout(**post)

class Website(Website):
    @http.route('/website/snippet/autocomplete', type='json', auth='public', website=True)
    def autocomplete(self, search_type=None, term=None, order=None, limit=5, max_nb_chars=999, options=None):
        res = super().autocomplete(search_type, term, order, limit, max_nb_chars, options)
        if not request.env.context.get('uid'):
            for result in res['results']:
                result['detail'] = ""
        return res