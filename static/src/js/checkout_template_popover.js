/** @odoo-module **/
import { WebsiteSale } from "@website_sale/js/website_sale";
import { _t } from "@web/core/l10n/translation";
import Dialog from "@web/legacy/js/core/dialog";
import { jsonrpc } from "@web/core/network/rpc_service";

export const cartPopoverModel = Dialog.extend({
  init: function (parent, params) {
    this.preventOpening = false;
    var options = Object.assign(
      {
        size: "large",
        buttons: [
          {
            text: _t('Go to cart'),
            click: this._onConfirmButtonClick,
          },
        ],
        technical: !params.isWebsite,
      },
      params || {}
    );
    this._super(parent, options);
  },

  _onConfirmButtonClick: function () {
    this.close();
  },

  willStart: function () {
    var self = this;
    this.getModalContent = jsonrpc("/shop/cart/popover", {}).then(function (
      modalContent
    ) {
      if (modalContent) {
        var $modalContent = $(modalContent);
        self.$content = $modalContent;
      } else {
        self.preventOpening = true;
      }
    });
    var parentInit = self._super.apply(self, arguments);
    return Promise.all([this.getModalContent, parentInit]);
  },
});

WebsiteSale.include({
  events: Object.assign({}, WebsiteSale.prototype.events, {
    "click #onclickOpenTemplate": "async _openCartPopover",
  }),
  _openCartPopover: async function (ev) {
    this.cartPopover = new cartPopoverModel(this.$form, {
      isWebsite: true,
      title: _t("Price Change Alert"),
    });

    await this.cartPopover.willStart();

    if (this.cartPopover && !this.cartPopover.preventOpening) {
      this.cartPopover.open();
    } else {
      window.location.href = "/shop/checkout?express=1";
    }
  },
});

export default WebsiteSale;
