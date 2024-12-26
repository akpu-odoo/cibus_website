/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onWillStart } from "@odoo/owl";
import { DateTimePicker } from "@web/core/datetime/datetime_picker";

patch(DateTimePicker.prototype, {
  setup() {
    super.setup();
    this.ormService = useService("orm");
    this.enabledDays = [];
    this.curr_input_tag = null;
    const curr_input_tag = document.getElementById("delivery_expected_date_0");
    this.prepare_selected_day =
      curr_input_tag?.classList.contains("text-primary");
    if (this.prepare_selected_day) {
      const current_sale_order =
        this.__owl__?.app?.root?.component?.router?.current?.hash?.id;
      if (!current_sale_order) {
        this.prepare_selected_day = false;
      } else {
        onWillStart(async () => {
          await this._fetchAllowedDays(current_sale_order);
        });
      }
    }
  },

  async _fetchAllowedDays(current_sale_order) {
    try {
      const result = await this.ormService.call(
        "sale.order",
        "get_allowed_days",
        [current_sale_order]
      );
      this.deliver_today = result.deliver_today;
      this.enabledDays = result.allowed_days;
      if (result.allowed_days.length == 0) {
        this.prepare_selected_day = false;
      }
    } catch (error) {
      this.prepare_selected_day = false;
      console.error("Error fetching allowed days:", error);
    }
  },

  getActiveRangeInfo({ isOutOfRange, range }) {
    if (
      this.prepare_selected_day &&
      this.itemInfo.range[1].ts - this.itemInfo.range[0].ts == 86399999
    ) {
      this.itemInfo.isValid = false;
      if (this?.itemInfo?.range[0]?.weekday) {
        for (let i in this.enabledDays) {
          if (this.enabledDays[i] === this?.itemInfo?.range[0]?.weekday) {
            this.itemInfo.isValid = true;
          }
        }
      }
      let today_date = new Date();
      let process_date = new Date(this.itemInfo.id);

      if (process_date < today_date) {
        this.itemInfo.isValid = false;
      }
      if (
        this.deliver_today &&
        process_date.getDate() == today_date.getDate() &&
        process_date.getMonth() == today_date.getMonth() &&
        process_date.getFullYear() == today_date.getFullYear()
      ) {
        this.itemInfo.isValid = true;
      }
    }

    return super.getActiveRangeInfo({ isOutOfRange, range });
  },
});
