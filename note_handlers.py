from notes import Note, NoteBook
from command_registry import CommandFormatError


def _parse_note_id(value: str) -> int:
    try:
        note_id = int(value)
    except ValueError:
        raise ValueError("Note id has to be a number") from None
    return note_id

def _format_notes(notes: list[Note]) -> str:
    return "\n".join(str(note) for note in notes)


def add_note(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise CommandFormatError
    note_text = " ".join(args)
    added_note = notebook.add_note(note_text)
    return f"Note {added_note.note_id} added"


def show_notes(args: list[str], notebook: NoteBook) -> str:
    result = _format_notes(notebook.get_all_notes())
    return result if result else "No notes yet"


def search_notes(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise CommandFormatError
    
    text_to_search = " ".join(args)
    result = _format_notes(notebook.search(text_to_search))
    return result if result else "No notes found"


def edit_note(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise CommandFormatError
    raw_id, *raw_text = args
    note_id = _parse_note_id(raw_id)
    new_text = " ".join(raw_text)
    notebook.edit_note(note_id, new_text)
    return f"Note {note_id} edited"


def delete_note(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise CommandFormatError
    raw_id, *_ = args
    note_id = _parse_note_id(raw_id)
    notebook.delete_note(note_id)
    return f"Note {note_id} deleted"


def sort_notes(args: list[str], notebook: NoteBook) -> str:
    groups = notebook.group_by_tags()
    if not groups:
        return "No notes yet"
    blocks = []
    for tag, notes in groups.items():
        row = ("#" + tag if tag else "No tag") + "\n" + _format_notes(notes)
        blocks.append(row)
    
    return "\n\n".join(blocks)


def add_tag(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise CommandFormatError
    raw_id, *tags = args
    note_id = _parse_note_id(raw_id)
    notebook.add_tags(note_id, tags)
    tags_text = " ".join(f"#{Note.normalize_tag(tag)}" for tag in tags)
    return f"{tags_text} added to note {note_id}"


def remove_tag(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise CommandFormatError
    raw_id, tag, *_ = args
    note_id = _parse_note_id(raw_id)
    notebook.remove_tag(note_id, tag)
    return f"Tag #{Note.normalize_tag(tag)} removed from note {note_id}"


def search_tag(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise CommandFormatError
    tag, *_ = args
    result = notebook.search_by_tag(tag)
    return _format_notes(result) if result else "No notes found"
