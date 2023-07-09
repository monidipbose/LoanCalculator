import tkinter as tk
import time
from datetime import datetime
import math


class TimerApp:
    def __init__(self):
        self.date = datetime.now().date()
        self.base_price = 0.0
        self.rate = 0
        self.start_time = 0.0
        self.running = False

        self.root = tk.Tk()
        self.root.title("Loan Calculator")
        self.root.state('zoomed')

        # Color theme
        self.bg_color = "#D1E8E4"
        self.label_color = "#554994"
        self.button_color = "#D3DEDC"
        self.label_color_start_end = "#6E5773"
        self.clock_color = "#6E5773"
        self.final_amount_color = "#374259"

        self.root.configure(bg=self.bg_color)

        # First Division - Textboxes
        self.textboxes_frame = tk.Frame(self.root, bg=self.bg_color)
        self.textboxes_frame.pack(pady=10)

        self.base_price_label = tk.Label(self.textboxes_frame, text="Bank Balance (₹):", font=("Helvetica", 14),
                                         bg=self.bg_color, fg=self.label_color)
        self.base_price_label.grid(row=0, column=0, padx=10)
        self.base_price_entry = tk.Entry(self.textboxes_frame, font=("Helvetica", 14))
        self.base_price_entry.grid(row=0, column=1, padx=10)
        self.base_price_validation = tk.Label(self.textboxes_frame, text="", fg="red", bg=self.bg_color)
        self.base_price_validation.grid(row=1, column=0, columnspan=2)

        self.rate_label = tk.Label(self.textboxes_frame, text="Rate per second(paisa):", font=("Helvetica", 14),
                                   bg=self.bg_color, fg=self.label_color)
        self.rate_label.grid(row=0, column=2, padx=10)
        self.rate_entry = tk.Entry(self.textboxes_frame, font=("Helvetica", 14))
        self.rate_entry.grid(row=0, column=3, padx=10)
        self.rate_validation = tk.Label(self.textboxes_frame, text="", fg="red", bg=self.bg_color)
        self.rate_validation.grid(row=1, column=3, columnspan=2)

        # Second Division - Labels for Date/Time
        self.datetime_labels_frame = tk.Frame(self.root, bg=self.bg_color)
        self.datetime_labels_frame.pack(pady=10)

        self.start_date_time_label = tk.Label(self.datetime_labels_frame, text="Start Date/Time:",
                                              font=("Helvetica", 14), bg=self.bg_color, fg=self.label_color)
        self.start_date_time_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.start_date_time_value = tk.StringVar()
        self.start_date_time_entry = tk.Label(self.datetime_labels_frame, textvariable=self.start_date_time_value,
                                              font=("Helvetica", 14), bg=self.bg_color, fg=self.label_color_start_end)
        self.start_date_time_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.end_date_time_label = tk.Label(self.datetime_labels_frame, text="End Date/Time:",
                                            font=("Helvetica", 14), bg=self.bg_color, fg=self.label_color)
        self.end_date_time_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.end_date_time_value = tk.StringVar()
        self.end_date_time_entry = tk.Label(self.datetime_labels_frame, textvariable=self.end_date_time_value,
                                            font=("Helvetica", 14), bg=self.bg_color, fg=self.label_color_start_end)
        self.end_date_time_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Base Price and Rate Labels
        self.base_price_display_label = tk.Label(self.root, text="Price: ₹", font=("Helvetica", 14),
                                                 bg=self.bg_color, fg=self.label_color)
        self.base_price_display_label.pack()

        self.rate_display_label = tk.Label(self.root, text="Rate per second(paisa): ", font=("Helvetica", 14),
                                           bg=self.bg_color, fg=self.label_color)
        self.rate_display_label.pack()

        # Third Division - Buttons
        self.buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        self.buttons_frame.pack(pady=20)

        self.start_stop_button = tk.Button(self.buttons_frame, text="Start", command=self.start_stop_timer,
                                           font=("Helvetica", 14), padx=10, pady=5, bg=self.button_color)
        self.start_stop_button.grid(row=0, column=0, padx=10)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_timer,
                                      font=("Helvetica", 14), padx=10, pady=5, bg=self.button_color)
        self.reset_button.grid(row=0, column=1, padx=10)

        # Clock and Final Amount Labels
        # self.clock_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 36),
        #                             bg=self.bg_color, fg=self.clock_color)
        # self.clock_label.pack(pady=20)

        self.final_amount_label = tk.Label(self.root, text="₹", font=("Helvetica", 60),
                                            bg=self.bg_color, fg=self.final_amount_color)
        self.final_amount_label.pack()

        # Notes Text Area
        self.notes_label = tk.Label(self.root, text="Notes:", font=("Helvetica", 14),
                                    bg=self.bg_color, fg=self.label_color)
        self.notes_label.pack(side=tk.TOP, pady=5)
        self.notes_textarea = tk.Text(self.root, height=10, font=("Helvetica", 14))
        self.notes_textarea.pack(padx=10, pady=5, side=tk.TOP)

        self.clock_label = tk.Label(self.root, text="00:00:00", font=("Helvetica", 16),
                                    bg=self.bg_color, fg=self.clock_color)
        self.clock_label.pack(pady=10, side=tk.BOTTOM)

    def start_stop_timer(self):
        if self.running:
            self.running = False
            self.start_stop_button.config(text="Start")
            self.reset_button.config(state=tk.NORMAL)
            self.end_date_time_value.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            if self.validate_inputs():
                self.base_price = float(self.base_price_entry.get())
                self.rate = float(self.rate_entry.get())
                self.start_time = time.time()
                self.running = True
                self.start_stop_button.config(text="Stop")
                self.reset_button.config(state=tk.DISABLED)
                self.start_date_time_value.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                self.end_date_time_value.set("")
                self.update_clock()

    def reset_timer(self):
        self.running = False
        self.start_stop_button.config(text="Start")
        self.reset_button.config(state=tk.NORMAL)
        self.start_date_time_value.set("")
        self.end_date_time_value.set("")
        self.base_price_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.clock_label.config(text="00:00:00")
        self.final_amount_label.config(text="₹")
        self.base_price_display_label.config(text="Price: ₹")
        self.rate_display_label.config(text="Rate per second(paisa):")
        # self.notes_textarea.delete("1.0", tk.END)

    # def check_midnight(self):
    #     current_time = datetime.now().time()
    #     if current_time.hour == 0 and current_time.minute == 0 and current_time.second == 0:
    #         self.clock_label.config(text="00:00:00")
    #         self.final_amount_label.config(text="₹")
    #         self.start_time = time.time()
    #         self.start_date_time_value.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    def check_midnight(self):
        current_date = datetime.now().date()
        # print(self.date)
        if current_date != self.date:
            self.date = datetime.now().date()
            self.clock_label.config(text="00:00:00")
            self.final_amount_label.config(text="₹")
            self.start_time = time.time()
            self.start_date_time_value.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def update_clock(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            self.clock_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # final_amount = (int(elapsed_time) * self.rate) / 100 + self.base_price
            final_amount = (math.ceil(elapsed_time) * self.rate) / 100 + self.base_price
            self.final_amount_label.config(text=f"₹{final_amount:,.2f}/-")

            self.check_midnight()

        self.root.after(1000, self.update_clock)

    def validate_inputs(self):
        base_price = self.base_price_entry.get().strip()
        rate = self.rate_entry.get().strip()

        if not base_price.isdigit():
            self.base_price_validation.config(text="Invalid input", fg="red")
            return False
        else:
            self.base_price_validation.config(text="")
            self.base_price_display_label.config(text=f"Price: ₹{float(base_price):,.0f}")

        if not rate.replace(".", "").isdigit():
            self.rate_validation.config(text="Invalid input", fg="red")
            return False
        else:
            self.rate_validation.config(text="")
            self.rate_display_label.config(text=f"Rate per second(paisa): {rate}")

        return True

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TimerApp()
    app.run()