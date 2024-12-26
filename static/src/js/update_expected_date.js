/** @odoo-module **/

import { jsonrpc } from "@web/core/network/rpc_service";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.UpdateExpectedDate = publicWidget.Widget.extend({
  selector: "#checkout_date_input",

  events: {
    change: "_onDateChange",
  },
  _onDateChange: function (ev) {
    const selectedDate = ev.currentTarget.value;
    jsonrpc("/update_expected_date", { date: selectedDate })
      .then((response) => {
        if (response.status === "success") {
          return;
        } else {
          console.error("Failed to update expected date");
        }
      })
      .catch((error) => {
        console.error("Error during RPC call:", error);
      });
  },
});
