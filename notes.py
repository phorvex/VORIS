import json
import os
import datetime

NOTES_FILE = os.path.expanduser("~/.voris/notes.json")
REMINDERS_FILE = os.path.expanduser("~/.voris/reminders.json")

def ensure_dir():
    os.makedirs(os.path.expanduser("~/.voris"), exist_ok=True)

def load_notes():
    ensure_dir()
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    ensure_dir()
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def add_note(text):
    notes = load_notes()
    note = {
        "text": text,
        "created_at": datetime.datetime.now().isoformat()
    }
    notes.append(note)
    save_notes(notes)
    return f"Note saved."

def get_notes():
    notes = load_notes()
    if not notes:
        return "You have no notes."
    result = f"You have {len(notes)} note{'s' if len(notes) > 1 else ''}:\n"
    for i, note in enumerate(notes, 1):
        result += f"{i}. {note['text']}\n"
    return result.strip()

def clear_notes():
    save_notes([])
    return "All notes cleared."

def delete_note(index):
    notes = load_notes()
    if index < 1 or index > len(notes):
        return "I couldn't find that note."
    removed = notes.pop(index - 1)
    save_notes(notes)
    return f"Deleted note: {removed['text']}"

def load_reminders():
    ensure_dir()
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    ensure_dir()
    with open(REMINDERS_FILE, "w") as f:
        json.dump(reminders, f, indent=2)

def add_reminder(text, minutes):
    reminders = load_reminders()
    due = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    reminder = {
        "text": text,
        "due": due.isoformat(),
        "created_at": datetime.datetime.now().isoformat()
    }
    reminders.append(reminder)
    save_reminders(reminders)
    return f"Reminder set for {minutes} minute{'s' if minutes != 1 else ''} from now."

def check_reminders():
    reminders = load_reminders()
    now = datetime.datetime.now()
    due_now = []
    remaining = []
    for r in reminders:
        if datetime.datetime.fromisoformat(r["due"]) <= now:
            due_now.append(r["text"])
        else:
            remaining.append(r)
    save_reminders(remaining)
    return due_now

def get_reminders():
    reminders = load_reminders()
    if not reminders:
        return "You have no pending reminders."
    now = datetime.datetime.now()
    result = f"You have {len(reminders)} reminder{'s' if len(reminders) > 1 else ''}:\n"
    for r in reminders:
        due = datetime.datetime.fromisoformat(r["due"])
        mins_left = int((due - now).total_seconds() / 60)
        if mins_left <= 0:
            result += f"- {r['text']} (due now)\n"
        else:
            result += f"- {r['text']} (in {mins_left} minute{'s' if mins_left != 1 else ''})\n"
    return result.strip()