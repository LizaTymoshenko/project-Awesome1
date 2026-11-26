from collections import UserDict, defaultdict

class Note:
    def __init__(self, note_id: int, text: str, tags: list[str] | None = None):
        self.note_id = note_id
        self.text = text
        self.tags = set()
        if tags:
            self.add_tags(tags)


    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value: str):
        validated_text = value.strip()
        if not validated_text:
            raise ValueError("Note is empty")
        self._text = validated_text

    def __str__(self):
        tags = ', '.join(sorted(self.tags))
        return f"{self.note_id} : {self.text} | tags: {tags if tags else 'No tags'}"

    def __repr__(self):
        return f"id:{self.note_id}, text={self.text!r}, tags={self.tags}"

    @staticmethod
    def normalize_tag(tag: str) -> str:
        return tag.lower().strip()
    
    def add_tags(self, tags: list[str]) -> None:
        for tag in tags:
            normalized_tag = Note.normalize_tag(tag)
            if normalized_tag:
                self.tags.add(normalized_tag)

    def remove_tag(self, tag: str) -> None:
        tag = Note.normalize_tag(tag)
        if tag not in self.tags:
            raise ValueError(f"Note {self.note_id} has no tag #{tag}")    
        self.tags.remove(tag)




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
        raise ValueError(f"Note {note_id} not found")

    def search(self, target_string: str) -> list[Note]:
        target_string = target_string.lower()
        found_notes = [note for note in self.data.values()
                       if target_string in note.text.lower()]
        return found_notes

    def edit_note(self, note_id: int, new_text: str) -> None:
        target_note = self.find_note(note_id)
        target_note.text = new_text

    def delete_note(self, note_id: int) -> None:
        self.find_note(note_id)
        del self.data[note_id]

    def get_all_notes(self) -> list[Note]:
        return list(self.data.values())
    
    def add_tags(self, note_id: int, tags: list[str]) -> None:
        note = self.find_note(note_id)
        note.add_tags(tags)  

    def remove_tag(self, note_id: int, tag: str) -> None:
        note = self.find_note(note_id)
        note.remove_tag(tag)  

    def search_by_tag(self, tag: str) -> list[Note]:
        tag = Note.normalize_tag(tag)
        found_notes = [note for note in self.data.values() if tag in note.tags]
        return found_notes

    # returns a dict: key - tag name, value - list of notes that have this tag
    # key: None - stores notes without tags
    def group_by_tags(self) -> dict[str | None, list[Note]]:
        groups = defaultdict(list)
        for note in self.data.values():
            if not note.tags:
                groups[None].append(note)
                continue
            for tag in note.tags:
                groups[tag].append(note)

        result = {
            tag: groups[tag]
            for tag in sorted(tag for tag in groups if tag is not None)
        }
        if None in groups:
            result[None] = groups[None]
        return result
                   
        



