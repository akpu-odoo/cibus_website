/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { OptionalProductsModal } from "@website_sale_product_configurator/js/sale_product_configurator_modal";

publicWidget.registry.WebsiteSale.include({
  /**
   * Override regular _onChangeCombination method
   * @override
   */
  _onChangeCombination: function (ev, $parent, combination) {
    this._super.apply(this, arguments);

    this.current_base_unit_price =
      combination["base_unit_price"] || combination["price"];
    this.currency_symbol = $("#o_price_currency_icon").val();

    if (combination["product_packaging_ids"].length != 0) {
      $("#product_variant_packaging_id")
        .parent()?.[0]
        ?.classList.remove("d-none");
      $("#o_input_packaging_qty").parent()?.[0]?.classList.remove("d-none");
      combination["variable_weight"]
        ? $(".css_quantity").addClass("d-none")
        : $(".css_quantity").removeClass("d-none");

      if (this.curr_prod != combination["product_id"]) {
        this.curr_prod = combination["product_id"];
        $parent.find("#product_variant_packaging_id").empty();
        combination["product_packaging_ids"].forEach((packag) => {
          $parent.find("#product_variant_packaging_id").append(
            $("<option>", {
              value: packag.qty,
              text: packag.name,
              id: packag.id,
            })
          );
        });
        this.current_pkd_qty =
          combination["product_packaging_ids"][0]["qty"] || 1;
        var price_tag = $(".oe_price")[0];
        if (price_tag) {
          price_tag.innerText =
            (
              this.current_base_unit_price * (this.current_pkd_qty || 1)
            ).toFixed(2) +
            " " +
            this.currency_symbol;
        }
      }
    } else {
      this.curr_prod = null;
      this.current_pkd_qty = 1;
      $("#product_variant_packaging_id").parent()[0]?.classList.add("d-none");
      $("#o_input_packaging_qty").parent()?.[0]?.classList.add("d-none");
      $("#o_input_packaging_qty").val(1);
      var price_tag = $(".oe_price")[0];
        if (price_tag) {
          price_tag.innerText =
            (this.current_base_unit_price * (this.current_pkd_qty || 1)
            ).toFixed(2) + " " + this.currency_symbol;
        }
    }
  },
  /**
   * Hook to add optional info to the combination info call.
   *
   * @param {$.Element} $product
   */
  _getOptionalCombinationInfoParam($product) {
    var super_res = this._super.apply(this, arguments);
    if ($("#product_variant_packaging_id").val()){
      super_res["product_variant_packaging_id"] =
      $("#product_variant_packaging_id option:selected").attr("id") || 'false';
    }
    return super_res;
  },
});

OptionalProductsModal.include({
  /**
   * When a product is added or when the quantity is changed,
   * we need to refresh the total price row
   */
  _computePriceTotal: function () {
    this._super.apply(this, arguments);
    if (this.$modal.find('.js_price_total').length) {
        var price = 0;
        this.$modal.find('.js_product.in_cart').each(function () {
            var quantity = parseFloat($(this).find('input[name="add_qty"]').first().val().replace(',', '.') || 1);
            price += parseFloat($(this).find('.js_raw_price').html()) * quantity;
        });
    }
    var total_qty = parseFloat($('#product_variant_packaging_id').val() || 1);
    var current_show_price = price*total_qty;
    $(".css_quantity").removeClass("d-none");
    price = price * total_qty;
    this.$modal.find('.js_price_total .oe_currency_value').text(
        this._priceToStr(parseFloat(price))
    );
    this.$modal.find('.oe_price .oe_currency_value').text(
        this._priceToStr(parseFloat(current_show_price))
    );
},
});
