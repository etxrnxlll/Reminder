import customtkinter as ctk
import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass
from tkinter import messagebox
# window render
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

@dataclass
class Reminder:
    id: uuid.UUID
    reminder_text: str
    reminder_time: datetime
    reminder_status: str

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "reminder_text": self.reminder_text,
            "reminder_time": self.reminder_time.isoformat(),
            "reminder_status": self.reminder_status
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reminder":
        return cls(
            id=uuid.UUID(data["id"]),
            reminder_text=data["reminder_text"],
            reminder_time=datetime.fromisoformat(data["reminder_time"]),
            reminder_status=data["reminder_status"]
        )

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

        self.list_frame = ctk.CTkScrollableFrame(self, width=220, height=100)
        self.list_frame.grid(row=3, column=1, padx=5, pady=5)
        # hack: скрыть скроллбар, публичного API нет
        self.list_frame._scrollbar.configure(height=0)

    def _start_polling(self):
        pass

    def render_reminders(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for r in self.active_reminders:
            if r.reminder_status == "missed":
                continue

            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", padx=2, pady=2)

            prefix = "✓ " if r.reminder_status == "done" else ""
            text = f'{prefix}{r.reminder_text} - {r.reminder_time.strftime("%d.%m %H:%M")}'

            label = ctk.CTkLabel(row, text=text)
            label.pack(side="left", padx=5)

            delete_button = ctk.CTkButton(
                row,
                text="Delete",
                width=50,
                command=lambda rid=r.id: self.delete_reminder(rid)
            )
            delete_button.pack(side="right", padx=5)

    def delete_reminder(self, reminder_id):
        self.active_reminders = [r for r in self.active_reminders if r.id != reminder_id]
        self.render_reminders()

    def check_reminders(self):
        pass

    def add_reminder(self):
        reminder_text = self.entry.get()
        reminder_time_raw = self.time_entry.get()

        if not reminder_text.strip():
            return

        try:
            parsed = datetime.strptime(reminder_time_raw, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM format.")
            return

        now = datetime.now()
        candidate = now.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)

        if candidate <= now:
            candidate = candidate + timedelta(days=1)

        new_reminder = Reminder(
            id=uuid.uuid4(),
            reminder_text=reminder_text,
            reminder_time=candidate,
            reminder_status="pending"
        )
        self.active_reminders.append(new_reminder)
        self.render_reminders()
        self.entry.delete(0, "end")
        self.time_entry.delete(0, "end")
        print("created:", new_reminder.reminder_time.isoformat())

if __name__ == "__main__":
    app = ReminderApp()
    app.mainloop()