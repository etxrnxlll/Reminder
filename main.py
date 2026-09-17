import customtkinter as ctk
import uuid
from datetime import datetime
from dataclasses import dataclass

active_reminders = []

ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("400x240")
app.title("Reminder")

@dataclass
class Reminder:
    id: uuid.UUID
    reminder_text: str
    reminder_time: datetime
    reminder_flag: bool

example = Reminder(
    id=uuid.uuid4(),
    reminder_text="Check mail",
    reminder_time=datetime.now(),
    reminder_flag=True
)

entry = ctk.CTkEntry(app, placeholder="Enter a reminder")

app.mainloop()