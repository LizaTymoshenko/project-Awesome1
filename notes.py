from collections import UserDict

class Note:
    def __init__(self, note_id: int, text: str, tags: list[str] | None = None):
        self.tags = []
        self.note_id = note_id
        self.text = text
        if tags is not None:
            self.tags.extend(tags)


    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value: str):
        validated_text = value.strip()
        if not validated_text:
            raise ValueError("Note is empty")
        self._text = validated_text
            
    # text is validated via setter
    def edit_note(self, new_text: str):
        self.text = new_text

    def __str__(self):
        tags = ', '.join(self.tags)
        return f"{self.note_id} : {self.text} tags: {tags if tags else 'No tags'}"
    
    def __repr__(self):
        return f"id:{self.note_id}, text={self.text!r}, tags={self.tags}"

# dict: key: id, value: note
class NoteBook(UserDict):
    def __init__(self):
        super().__init__()
        self.counter = 1

    # tags are optional when adding the note
    # when adding an empty note, class Note will throw ValueError
    def add_note(self, text: str, tags: list[str] | None = None) -> Note:
        note = Note(self.counter, text, tags)
        self.data[self.counter] = note
        self.counter += 1
        return note

    def find_note(self, note_id: int) -> Note:
        if note_id in self.data:
            return self.data[note_id]
        raise ValueError("Note not found")

    def search(self, target_string: str) -> list[Note]:
        found_notes = []
        for note in self.data.values():
            if target_string.lower() in note.text.lower():
                found_notes.append(note)
        return found_notes

    def edit_note(self, note_id: int, new_text: str) -> None:
        target_note = self.find_note(note_id)
        target_note.edit_note(new_text)

    def delete_note(self, note_id: int) -> None:
        self.find_note(note_id)
        del self.data[note_id]

    def get_all_notes(self) -> list[Note]:
        return list(self.data.values())
       



    