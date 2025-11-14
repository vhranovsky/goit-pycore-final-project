from collections import UserDict
from .address_book import Field
from .general import (
    ValidNoteContentError,
    ValidTagError,
    ValidSearchQueryError,
)


# Клас для контенту нотатки з валідацією.
class NoteContent(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, text: str):
        # Порожній або нестроковий текст нотатки вважаємо невалідним.
        if not isinstance(text, str) or not text.strip():
            raise ValidNoteContentError()
        self.__value = text


# Клас для тегів нотаток з валідацією.
class Tag(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, tag: str):
        # Тег не може бути порожнім або з одних пробілів.
        if not isinstance(tag, str) or not tag.strip():
            raise ValidTagError()
        self.__value = tag.lower()


# Клас для представлення однієї нотатки.
class Note:
    def __init__(self, content: str, note_id: int):
        self.id = note_id
        self.content = NoteContent(content)
        self.tags: list[Tag] = []

    def add_tag(self, tag_str: str):
        tag = Tag(tag_str)
        if not self.has_tag(tag.value):
            self.tags.append(tag)

    def find_tag(self, tag_str: str) -> Tag | None:
        tag_lower = tag_str.lower()
        tags = list(filter(lambda tag: tag.value == tag_lower, self.tags))
        return tags[0] if len(tags) > 0 else None

    def remove_tag(self, tag_str: str) -> bool:
        tag_to_remove = self.find_tag(tag_str)
        if tag_to_remove:
            self.tags.remove(tag_to_remove)
            return True
        return False

    def edit_content(self, new_content: str):
        self.content.value = new_content

    def has_tag(self, tag_query: str) -> bool:
        return self.find_tag(tag_query) is not None

    def __str__(self):
        tags_str = ", ".join(str(t) for t in self.tags) or "No tags"
        return f"[ID: {self.id}] | Теги: [{tags_str}]\n  {self.content.value}\n"

    def __repr__(self):
        return str(self)


# Клас для зберігання книги нотаток.
class NoteBook(UserDict):

    def __init__(self):
        super().__init__()
        self.note_id_counter = 1

    def add_note(self, content: str) -> int:
        new_id = self.note_id_counter
        note = Note(content, new_id)
        self.data[new_id] = note
        self.note_id_counter += 1
        return new_id

    def find_note_by_id(self, note_id: int) -> Note | None:
        return self.data.get(note_id)

    def delete_note(self, note_id: int) -> bool:
        if note_id in self.data:
            del self.data[note_id]
            return True
        return False

    def edit_note_content(self, note_id: int, new_content: str) -> bool:
        note = self.find_note_by_id(note_id)
        if note:
            note.edit_content(new_content)
            return True
        return False

    def search_notes_by_content(self, query: str) -> list[Note]:
        query = query.strip()
        if not query:
            raise ValidSearchQueryError()
        results: list[Note] = []
        query_lower = query.lower()
        for note in self.data.values():
            if query_lower in note.content.value.lower():
                results.append(note)
        return results

    def search_notes_by_tag(self, tag_query: str) -> list[Note]:
        tag_query = tag_query.strip()
        if not tag_query:
            raise ValidTagError()
        results: list[Note] = []
        tag_query_lower = tag_query.lower()
        for note in self.data.values():
            if note.has_tag(tag_query_lower):
                results.append(note)
        return results

    def sort_notes_by_tags(self) -> list[Note]:
        # \uffff - символ, який гарантовано буде "більшим" за будь-який інший тег
        def sort_key(note: Note):
            if note.tags:
                return note.tags[0].value
            return "\uffff"

        return sorted(self.data.values(), key=sort_key)

    def __str__(self):
        if not self.data:
            return "Note book is empty."
        return "\n".join(str(note) for note in self.data.values())
