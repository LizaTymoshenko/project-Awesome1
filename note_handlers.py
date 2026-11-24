from notes import Note, NoteBook
from decorators import input_error


def _parse_note_id(value: str) -> int:
    try:
        note_id = int(value)
    except ValueError:
        raise ValueError("Note id has to be a number") from None
    return note_id

def _format_notes(notes: list[Note]) -> str:
    return "\n".join(str(note) for note in notes)

@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Correct format: add-note [text]")
    note_text = " ".join(args)
    added_note = notebook.add_note(note_text)
    return f"Note {added_note.note_id} added"


@input_error
def show_notes(args: list[str], notebook: NoteBook) -> str:
    result = _format_notes(notebook.get_all_notes())
    return result if result else "No notes yet"


@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Correct format: search-note [text]")
    
    text_to_search = " ".join(args)
    result = _format_notes(notebook.search(text_to_search))
    return result if result else "No notes found"


@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Correct format: edit-note [id] [new text]")
    raw_id, *raw_text = args
    note_id = _parse_note_id(raw_id)
    new_text = " ".join(raw_text)
    notebook.edit_note(note_id, new_text)
    return f"Note {note_id} edited"

@input_error
def delete_note(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Correct format: delete-note [id]")
    raw_id, *_ = args
    note_id = _parse_note_id(raw_id)
    notebook.delete_note(note_id)
    return f"Note {note_id} deleted"

@input_error
def sort_notes(args: list[str], notebook: NoteBook) -> str:
    groups = notebook.group_by_tags()
    if not groups:
        return "No notes yet"
    blocks = []
    for tag, notes in groups.items():
        row = ("#" + tag if tag else "No tag") + "\n" + _format_notes(notes)
        blocks.append(row)
    
    return "\n\n".join(blocks)

@input_error
def add_tag(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Correct format: add-tag [note id] [tag1] [tag2] ...")
    raw_id, *tags = args
    note_id = _parse_note_id(raw_id)
    notebook.add_tags(note_id, tags)
    tags_text = " ".join(f"#{Note.normalize_tag(tag)}" for tag in tags)
    return f"{tags_text} added to note {note_id}"

@input_error
def remove_tag(args: list[str], notebook: NoteBook) -> str:
    if len(args) < 2:
        raise ValueError("Correct format: remove-tag [note id] [tag]")
    raw_id, tag, *_ = args
    note_id = _parse_note_id(raw_id)
    notebook.remove_tag(note_id, tag)
    return f"Tag #{Note.normalize_tag(tag)} removed from note {note_id}"

@input_error
def search_tag(args: list[str], notebook: NoteBook) -> str:
    if not args:
        raise ValueError("Correct format: search-tag [tag]")
    tag, *_ = args
    result = notebook.search_by_tag(tag)
    return _format_notes(result) if result else "No notes found"
