"""Synthetic display module with two contributors' pending changes."""


def display_value(value):
    if value is None or value == "":
        return "—"
    return str(value)


def render_admin_note(note):
    text = note.strip()
    if text:
        return "ADMIN: " + text
    return "ADMIN: (empty)"
