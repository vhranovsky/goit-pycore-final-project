from . import address_book
from . import note_book
import pickle
import os
from .personal_assistant_address_book_handler import PersonalAssistantAddressBookHandler
from .personal_assistant_note_book_handler import PersonalAssistantNoteBookHandler
from .general import input_error
import difflib


# Наш бот
class PersonalAssistant:
    def __init__(self):
        self.__abook__ = None
        self.__nbook__ = None
        self.__assistant_handler__ = PersonalAssistantAddressBookHandler()
        self.__note_handler__ = PersonalAssistantNoteBookHandler()

        self.__exit_commands__ = ["close", "exit", "bye", "bye-bye"]

        self.__abook_commands__ = {
            "add": self.__assistant_handler__.add_contact,
            "add-phone": self.__assistant_handler__.add_phone,
            "add-email": self.__assistant_handler__.add_email,
            "add-birthday": self.__assistant_handler__.add_birthday,
            "add-address": self.__assistant_handler__.add_address,
            "get-birthday": self.__assistant_handler__.get_birthday,
            "get-birthdays": self.__assistant_handler__.birthdays,
            "get-phone": self.__assistant_handler__.get_phone_by_name,
            "get-all": self.__assistant_handler__.get_all_contacts,
            "get-info": self.__assistant_handler__.get_contact_info,
            "change-phone": self.__assistant_handler__.change_phone,
            "change-email": self.__assistant_handler__.change_email,
            "change-birthday": self.__assistant_handler__.add_birthday,
            "change-address": self.__assistant_handler__.add_address
         }

        self.__nbook_commands__ = {
            "add-note":  self.__note_handler__.add_note,
            "get-note":  self.__note_handler__.get_note,
            "get-notes": self.__note_handler__.get_all_notes,
            "change-note": self.__note_handler__.edit_note,
            "delete-note": self.__note_handler__.delete_note,
            "add-tag":    self.__note_handler__.add_tag,
            "delete-tag": self.__note_handler__.remove_tag,
            "get-notes-by-text": self.__note_handler__.search_notes,
            "get-notes-by-tag":  self.__note_handler__.search_by_tag,
            "get-notes-sorted-by-tags": self.__note_handler__.sort_by_tags,
        }

    # privat methods
    def __clear_console__(self):
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For macOS and Linux
            os.system('clear')

    def __load_abook__(self, file_name: str) -> address_book.AddressBook:
        try:
            with open(file_name, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return address_book.AddressBook()
        except ModuleNotFoundError:
            return address_book.AddressBook()

    def __load_nbook__(self, file_name: str) -> note_book.NoteBook:
        try:
            with open(file_name, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return note_book.NoteBook()
        except ModuleNotFoundError:
            return note_book.NoteBook()

    def __save__(self, save_folder_path: str = None):
        if save_folder_path is None:
            save_folder_path = os.path.expanduser("~")

        with open(save_folder_path + "/abook.pkl", "wb") as f:
            pickle.dump(self.__abook__, f)

        with open(save_folder_path + "/nbook.pkl", "wb") as f:
            pickle.dump(self.__nbook__, f)

    def __load__(self, save_folder_path: str = None):
        if save_folder_path is None:
            save_folder_path = os.path.expanduser("~")

        self.__abook__ = self.__load_abook__(save_folder_path+"/abook.pkl")
        self.__nbook__ = self.__load_nbook__(save_folder_path+"/nbook.pkl")

    # handlers
    @input_error
    def __parse_input__(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def __run_command__(self, user_input: str) -> bool:
        command, *args = self.__parse_input__(user_input)

        if command in self.__nbook_commands__:
            print(self.__nbook_commands__[command](args, self.__nbook__))
            if not command.startswith("get"):
                self.__save__()
        elif command in self.__abook_commands__:
            print(self.__abook_commands__[command](args, self.__abook__))
            if not command.startswith("get"):
                self.__save__()
        elif command in self.__exit_commands__:
            print("Good bye!")
            return True
        elif command == "hello":
            print("How can I help you?")
        elif command == "clear":
            self.__clear_console__()
        else:
            print("Invalid command.")
            suggestions_list = self.get_suggestion(command)
            if suggestions_list is not None and len(suggestions_list) > 0:
                print(f"    Did you mean: {", ".join(suggestions_list)}")
                return self.apply_suggestion(suggestions_list[0]+" "+" ".join(args))

        return False

    def __main_run__(self):
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            if self.__run_command__(user_input):
                break

    # public methods
    @input_error
    def get_suggestion(self, command) -> list | None:
        # cutoff=0.5 означає, що команда має бути схожа принаймні на 50%
        matches = difflib.get_close_matches(command, self.__abook_commands__.keys(), n=3, cutoff=0.5)
        if len(matches) == 0:
            matches = difflib.get_close_matches(command, self.__nbook_commands__.keys(), n=3, cutoff=0.5)
        if len(matches) == 0:
            matches = difflib.get_close_matches(command, self.__exit_commands__, n=3, cutoff=0.5)
        return matches

    def apply_suggestion(self, params: str) -> bool:
        print(f"\nDo you want run this command: {params} \n[y]=yes [any key]=no")
        user_input = input()
        if user_input.lower() == "y":
            print(params)
            return self.__run_command__(params)

        return False

    def run(self):
        self.__load__()
        self.__main_run__()
        self.__save__()


def run():
    PersonalAssistant().run()
