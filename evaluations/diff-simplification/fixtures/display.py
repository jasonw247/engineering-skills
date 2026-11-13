"""Synthetic display module with two contributors' pending changes."""


def _render_present(value):
    return str(value)


def display_value(value):
    if value is None or value == "":
        result = "—"
    else:
        result = _render_present(value)
    return result


def render_admin_note(note):
    text = note.strip()
    if text:
        return "ADMIN: " + text
    return "ADMIN: (empty)"
