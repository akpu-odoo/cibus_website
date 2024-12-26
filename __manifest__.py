# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Cibus - Website",
    "version": "17.0.1.0.0",
    "summary": "eCommerce Website Improvements",
    "Description": "Goal is to achieve changes in website and sales according to expected delivery date",
    "author": "Odoo PS",
    "license": "LGPL-3",
    "depends": ["sale", "website_sale", 'website_sale_product_configurator', 'stock'],
    "data": [
        "security/ir.model.access.csv",
        "data/week_day_demo_data.xml",
        "views/sale_order_views.xml",
        "views/res_partner_view.xml",
        "views/product_pricelist_item_view.xml",
        "views/product_pricelist_view.xml",
        "views/cart_popup_template.xml",
        "views/website_cart_template.xml",
        "views/website_sale_template.xml",
        "views/product_template_form_view.xml",
        "views/stock_picking_views.xml",
        "views/portal_template.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "cibus_website/static/src/js/restricted_datepicker.js",
        ],
        "web.assets_frontend": [
            "web/static/lib/fullcalendar/core/main.css",
            "web/static/lib/fullcalendar/core/main.js",
            "web/static/lib/fullcalendar/daygrid/main.css",
            "web/static/lib/fullcalendar/daygrid/main.js",
            "web/static/lib/fullcalendar/interaction/main.js",
            "cibus_website/static/src/js/checkout_template_popover.js",
            "cibus_website/static/src/js/datetime_picker.js",
            "cibus_website/static/src/js/update_expected_date.js",
            "cibus_website/static/src/js/variant_mixin.js",
            "cibus_website/static/src/js/website_sale.js",
        ],
    },
    "application": True,
    "installable": True,
}
