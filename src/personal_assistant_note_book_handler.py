from . import note_book
from .general import input_error


class PersonalAssistantNoteBookHandler:
    def __init__(self):
        pass

    @input_error
    def add_note(self, args: list, nbook: note_book.NoteBook) -> str:
        if not args:
            return "Enter valid arguments for the command."
        content = " ".join(args)
        note_id = nbook.add_note(content)
        return f"Note #{note_id} added."

    @input_error
    def delete_note(self, args: list, nbook: note_book.NoteBook) -> str:
        note_id = int(args[0])
        ok = nbook.delete_note(note_id)
        return f"Note #{note_id} deleted." if ok else "Record is missing!"

    @input_error
    def edit_note(self, args: list, nbook: note_book.NoteBook) -> str:
        # edit-note <id> <new content...>
        note_id = int(args[0])
        new_content = " ".join(args[1:])
        if not new_content:
            return "Enter valid arguments for the command."
        ok = nbook.edit_note_content(note_id, new_content)
        return f"Note #{note_id} updated." if ok else "Record is missing!"

    @input_error
    def get_note(self, args: list, nbook: note_book.NoteBook) -> str:
        note_id = int(args[0])
        note = nbook.find_note_by_id(note_id)
        return str(note) if note else "Record is missing!"

    @input_error
    def get_all_notes(self, args: list, nbook: note_book.NoteBook) -> str:
        return f"{nbook}"

    @input_error
    def add_tag(self, args: list, nbook: note_book.NoteBook) -> str:
        # add-tag <id> <tag>
        note_id = int(args[0])
        tag = args[1]
        note = nbook.find_note_by_id(note_id)
        if not note:
            return "Record is missing!"
        note.add_tag(tag)
        return f"Tag '{tag.lower()}' added to note #{note_id}."

    @input_error
    def remove_tag(self, args: list, nbook: note_book.NoteBook) -> str:
        # remove-tag <id> <tag>
        note_id = int(args[0])
        tag = args[1]
        note = nbook.find_note_by_id(note_id)
        if not note:
            return "Record is missing!"
        ok = note.remove_tag(tag)
        return (f"Tag '{tag.lower()}' removed from note #{note_id}."
                if ok else f"Tag '{tag.lower()}' not found on note #{note_id}.")

    @input_error
    def search_notes(self, args: list, nbook: note_book.NoteBook) -> str:
        # search-notes <query...>
        if not args:
            return "Enter valid arguments for the command."
        query = " ".join(args)
        found = nbook.search_notes_by_content(query)
        if not found:
            return "No matches."
        return "\n".join(str(n) for n in found)

    @input_error
    def search_by_tag(self, args: list, nbook: note_book.NoteBook) -> str:
        # search-by-tag <tag>
        tag = args[0]
        found = nbook.search_notes_by_tag(tag)
        if not found:
            return "No matches."
        return "\n".join(str(n) for n in found)

    @input_error
    def sort_by_tags(self, args: list, nbook: note_book.NoteBook) -> str:
        sorted_notes = nbook.sort_notes_by_tags()
        if not sorted_notes:
            return "Note book is empty."
        return "\n".join(str(n) for n in sorted_notes)
