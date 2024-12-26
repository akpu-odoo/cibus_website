/** @odoo-module **/
import { WebsiteSale } from "@website_sale/js/website_sale";
import { AddToCartNotification } from "@website_sale/js/notification/add_to_cart_notification/add_to_cart_notification";
import { patch } from "@web/core/utils/patch";


WebsiteSale.include({
  events: Object.assign({}, WebsiteSale.prototype.events, {
    'change select[name="product_variant_packaging_id"]':
      "_onProductVariantPackagingChange",
    'change input[name="packaging_qty"]': "_onPackagingQtyChange",
    "click #backToShopPage": "_onClickWindowHistoryBack",
  }),
  start() {
    const super_res = this._super.apply(this, arguments);
    this.curr_prod = null;
    this.current_pkd_qty = 0;
    return super_res;
  },
  _submitForm: function () {
    this.rootProduct.product_variant_packaging_id = $("#product_variant_packaging_id option:selected").attr("id")
    return this._super.apply(this, arguments);
  },
  _onClickWindowHistoryBack: function (event) {
    var url = window.history.back();
  },
  /**
   * @private
   * @param event
   */
  _onProductVariantPackagingChange: async function (event) {
    event.preventDefault();
    const $target = $(event.currentTarget);
    this.current_pkd_qty =
      parseFloat($target.closest("#product_variant_packaging_id").val()) || 1;
    var qty = parseInt($("#o_input_packaging_qty").val());
    $target
      .closest(".js_main_product")
      .find(".quantity")
      .val((qty > 0 ? qty : 1))
      .trigger("change");
    var price_tag = $(".oe_price")[0];
    var currency_symbol = $("#o_price_currency_icon").val();
    if (price_tag) {
      price_tag.innerText =
        (this.current_base_unit_price * (this.current_pkd_qty || 1)).toFixed(
          2
        ) +
        " " +
        currency_symbol;
    }
  },

  _onPackagingQtyChange: function (event) {
    event.preventDefault();
    const $target = $(event.currentTarget);
    this.current_pkd_qty =
      parseFloat($("#product_variant_packaging_id").val()) || 1;
    var qty = parseFloat($target.val()) || 1;
    qty <= 0 ? $target.val(1).trigger("change") : $target.val(qty);
    $target
      .closest(".js_main_product")
      .find(".quantity")
      .val((qty > 0 ? qty : 1))
      .trigger("change");
  },
});

const super_getProductSummary = AddToCartNotification.prototype.getProductSummary;
patch(AddToCartNotification.prototype, {
 
  /**
   * @param {Object} line - The line element for which to return the product summary.
   * @return {String} - The product summary.
   */
  getProductSummary(line) {
    let res = super_getProductSummary.apply(this, arguments);
    var total_quantity =
      line.quantity / ($("#product_variant_packaging_id").val() || 1);
    return total_quantity + " x " + line.name;
  },
});
