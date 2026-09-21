import customtkinter as ctk
import uuid
from datetime import datetime
from dataclasses import dataclass
import time

# list of reminders
active_reminders = []

# window render
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")
app.title("Reminder")

# Reminder class
@dataclass
class Reminder:
    id: uuid.UUID
    reminder_text: str
    reminder_time: datetime
    reminder_flag: bool

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "reminder_text": self.reminder_text,
            "reminder_time": self.reminder_time,
            "reminder_flag": self.reminder_flag
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reminder":
        return cls(
            id=uuid.UUID(data["id"]),
            reminder_text=data["reminder_text"],
            reminder_time=datetime.strptime(data["reminder_time"], "%H:%M"),
            reminder_flag=data["reminder_flag"]
        )

# delete reminder
def delete_reminder(reminder_id):
    global active_reminders
    active_reminders = [r for r in active_reminders if r.id != reminder_id]
    render_reminders()

# render reminders
def render_reminders():
    for w in list_frame.winfo_children():
        w.destroy()

    for r in active_reminders:
        row = ctk.CTkFrame(list_frame)
        row.pack(fill="x", padx=2, pady=2)

        label = ctk.CTkLabel(
            row,
            text=f'{r.reminder_text} - {r.reminder_time.strftime("%H:%M")}'
        )
        label.pack(side="left", padx=5)
        delete_button = ctk.CTkButton(
            row,
            text="Delete",
            width=50,
            command=lambda rid=r.id: delete_reminder(rid)
        )
        delete_button.pack(side="right", padx=5)

# func to add a reminder
def add_reminder():
    reminder_text = entry.get()
    reminder_time_raw = time_entry.get()

    if not reminder_text.strip():
        return

    try:
        reminder_time = datetime.strptime(reminder_time_raw, "%H:%M")
    except ValueError:
        print("Invalid time format")
        return
    new_reminder = Reminder(
        id=uuid.uuid4(),
        reminder_text=reminder_text,
        reminder_time=reminder_time,
        reminder_flag=True
    )
    active_reminders.append(new_reminder)
    render_reminders()
    entry.delete(0, "end")
    time_entry.delete(0, "end")

def check_reminders():
    print(f'Checking... Active reminders: {len(active_reminders)}')
    app.after(1000, check_reminders)

# rendering of text input fields
entry = ctk.CTkEntry(app, placeholder_text="Enter a reminder")
entry.grid(row=0, column=0, padx=5, pady=5)
time_entry = ctk.CTkEntry(app, placeholder_text="Enter a reminder time")
time_entry.grid(row=1, column=0, padx=5, pady=5)

# rendering of button field
button = ctk.CTkButton(app, text="Add a Reminder", command=add_reminder)
button.grid(row=2, column=0, padx=5, pady=5)

list_frame = ctk.CTkScrollableFrame(app, width=200, height=200)
list_frame.grid(row=3, column=1, padx=5, pady=5)
list_frame._scrollbar.configure(height=0)

check_reminders()
app.mainloop()
