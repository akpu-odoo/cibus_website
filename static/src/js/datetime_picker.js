/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CheckoutDateWidget = publicWidget.Widget.extend({
    selector: "#checkout_date_input",
    start: function () {
        this._initializeFullCalendar();
    },
    _initializeFullCalendar: function () {
        const inputField = this.el;
        inputField.addEventListener("focus", (e) => {
            this._showFullCalendar(inputField);
        });
    },

    _showFullCalendar: async function (inputField) {
        inputField.blur();
        const existingCalendar = document.getElementById("checkout_calendar");
        if (existingCalendar) {
            existingCalendar.remove();
            return;
        }

        const calendarContainer = document.createElement("div");
        calendarContainer.id = "checkout_calendar";
        calendarContainer.style.position = "absolute";
        calendarContainer.style.zIndex = "9999";
        calendarContainer.style.background = "#fff";
        calendarContainer.style.border = "1px solid #ddd";
        calendarContainer.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";
        calendarContainer.style.padding = "10px";
        calendarContainer.style.borderRadius = "4px";

        const updateCalendarPosition = () => {
            const rect = inputField.getBoundingClientRect();
            calendarContainer.style.top = rect.bottom + window.scrollY + "px";
            calendarContainer.style.left = rect.left + window.scrollX + "px";
        };

        updateCalendarPosition();

        calendarContainer.style.width = "450px";
        calendarContainer.style.height = "500px";
        document.body.appendChild(calendarContainer);
        let selectedDays = [];
        let final_response;
        let current_locale = "en"

        try {
            const response = await fetch("/get_user_selected_days", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({}),
            });
            if (response.ok) {
                final_response = await response.json()
                selectedDays = final_response.result[0];
                current_locale = final_response.result[1] || "en";
            } else {
                console.error("Failed to fetch selected days");
            }
        } catch (error) {
            console.error("Error fetching selected days:", error);
        }
        let enabledDays = selectedDays.map((day) => day == 7 ? 0 : day);

        if (enabledDays.length == 0) {
          enabledDays = [0, 1, 2, 3, 4, 5, 6];
        }

        const calendar = new FullCalendar.Calendar(calendarContainer, {
            plugins: ["dayGrid", "interaction"],
            initialView: "dayGridMonth",
            locale: current_locale,
            dayRender: (dayRenderInfo) => {
                const date = new Date(dayRenderInfo.date);
                const day = date.getDay();
                const today = new Date();
                const isTomorrow =
                  date.getDate() === today.getDate() + 1 &&
                  date.getMonth() === today.getMonth() &&
                  date.getFullYear() === today.getFullYear();
                if (!enabledDays.includes(day) || today > date || (today.getHours() > 21 && isTomorrow)) {
                  dayRenderInfo.el.classList.add("fc-disabled-day");
                }
            },

            dateClick: (info) => {
                if (!info.dayEl?.classList.contains("fc-disabled-day")) {
                  inputField.value = info.dateStr;
                  inputField.blur();
                  calendarContainer.remove();

                  const changeEvent = new Event("change", {
                    bubbles: true,
                    cancelable: true,
                  });
                  inputField.dispatchEvent(changeEvent);
                }
            },

            aspectRatio: 1.5,
            contentHeight: 400,
        });

        calendar.render();

        const handleScrollOrResize = () => {
            if (document.body.contains(calendarContainer)) {
                updateCalendarPosition();
            }
        };

        window.addEventListener("scroll", handleScrollOrResize, true);
        window.addEventListener("resize", handleScrollOrResize, true);

        calendarContainer.addEventListener("remove", () => {
            window.removeEventListener("scroll", handleScrollOrResize, true);
            window.removeEventListener("resize", handleScrollOrResize, true);
        });
    },
});
