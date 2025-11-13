from . import note_book
from .general import input_error


class PersonalAssistantNoteBookHandler:
    def __init__(self):
        pass

    @input_error
    def add_note(self, args: list, nbook: note_book.NoteBook) -> str:
        content = " ".join(args)
        note_id = nbook.add_note(content)
        return f"Note #{note_id} added."

    @input_error
    def delete_note(self, args: list, nbook: note_book.NoteBook) -> str:
        note_id = int(args[0])
        ok = nbook.delete_note(note_id)

        if not ok:
            raise KeyError

        return f"Note #{note_id} deleted."

    @input_error
    def edit_note(self, args: list, nbook: note_book.NoteBook) -> str:
        note_id = int(args[0])
        new_content = " ".join(args[1:])
        ok = nbook.edit_note_content(note_id, new_content)

        if not ok:
            raise KeyError

        return f"Note #{note_id} updated."

    @input_error
    def get_note(self, args: list, nbook: note_book.NoteBook) -> str:
        note_id = int(args[0])
        note = nbook.find_note_by_id(note_id)

        if note is None:
            raise KeyError

        return str(note)

    @input_error
    def get_all_notes(self, args: list, nbook: note_book.NoteBook) -> str:
        return str(nbook)

    @input_error
    def add_tag(self, args: list, nbook: note_book.NoteBook) -> str:
        note_id = int(args[0])
        tag = args[1]
        note = nbook.find_note_by_id(note_id)

        if note is None:
            raise KeyError

        note.add_tag(tag)
        return f"Tag '{tag.lower()}' added to note #{note_id}."

    @input_error
    def remove_tag(self, args: list, nbook: note_book.NoteBook) -> str:
        note_id = int(args[0])
        tag = args[1]
        note = nbook.find_note_by_id(note_id)

        if note is None:
            raise KeyError

        ok = note.remove_tag(tag)

        if ok:
            return f"Tag '{tag.lower()}' removed from note #{note_id}."

        return f"Tag '{tag.lower()}' not found on note #{note_id}."

    @input_error
    def search_notes(self, args: list, nbook: note_book.NoteBook) -> str:
        query = " ".join(args)
        found = nbook.search_notes_by_content(query)

        if not found:
            return "No matches."

        lines = [str(note) for note in found]
        return "\n".join(lines)

    @input_error
    def search_by_tag(self, args: list, nbook: note_book.NoteBook) -> str:
        tag = args[0]
        found = nbook.search_notes_by_tag(tag)

        if not found:
            return "No matches."

        lines = [str(note) for note in found]
        return "\n".join(lines)

    @input_error
    def sort_by_tags(self, args: list, nbook: note_book.NoteBook) -> str:
        sorted_notes = nbook.sort_notes_by_tags()

        if not sorted_notes:
            return "Note book is empty."

        lines = [str(note) for note in sorted_notes]
        return "\n".join(lines)
