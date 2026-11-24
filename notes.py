class Note:
    def __init__(self, note_id, text, tags=None):
        self.tags = []
        self.note_id = note_id
        self.text = Note._validate_text(text)
        if tags is not None:
            self.tags.extend(tags)

    @staticmethod
    def _validate_text(text):
        validated_text = text.strip()
        if not validated_text:
            raise ValueError("Note is empty")
        return validated_text
    
    def edit_note(self, new_text):
        self.text = self._validate_text(new_text)

    def __str__(self):
        tags = ', '.join(self.tags)
        return f"{self.note_id} : {self.text}. tags: {tags if tags else 'No tags'}"
