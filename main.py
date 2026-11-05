import customtkinter as ctk
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass
from tkinter import messagebox
# window render
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class ReminderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x240")
        self.title("Reminder")
        self.active_reminders = []
        self._setup_ui()
        self._start_polling()

    def _setup_ui(self):
        self.entry = ctk.CTkEntry(self, placeholder_text="Enter a reminder")
        self.entry.grid(row=0, column=0, padx=5, pady=5)

        self.time_entry = ctk.CTkEntry(self, placeholder_text="Enter a reminder time")
        self.time_entry.grid(row=1, column=0, padx=5, pady=5)

        self.add_button = ctk.CTkButton(self, text="Add reminder", command=self.add_reminder)
        self.add_button.grid(row=2, column=0, padx=5, pady=5)

        self.list_frame = ctk.CTkScrollableFrame(self, width=200, height=70)
        self.list_frame.grid(row=3, column=1, padx=5, pady=5)
        # hack: скрыть скроллбар, публичного API нет
        self.list_frame._scrollbar.configure(height=0)

    def _start_polling(self):
        pass

    def add_reminder(self):
        pass

if __name__ == "__main__":
    app = ReminderApp()
    app.mainloop()