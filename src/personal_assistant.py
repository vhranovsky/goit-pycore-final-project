from . import address_book
from . import note_book
import pickle
import os
from .personal_assistant_address_book_handler import PersonalAssistantAddressBookHandler
from .personal_assistant_note_book_handler import PersonalAssistantNoteBookHandler
from .general import input_error
import difflib
import re
from pathlib import Path
from . import __version__


# Наш бот
class PersonalAssistant:
    def __init__(self):
        self.__abook__ = None
        self.__nbook__ = None
        self.__assistant_handler__ = PersonalAssistantAddressBookHandler()
        self.__note_handler__ = PersonalAssistantNoteBookHandler()

        self.__sys_commands__ = {
            "close": [self.__exit__, True],
            "exit": [self.__exit__, True],
            "bye": [self.__exit__, True],
            "bye-bye": [self.__exit__, True],
            "hello": [(lambda args: "How can I help you?"), False],
            "clear": [self.__clear_console__, False],
            "help": [self.__show_help__, False],
            "version": [(lambda args: __version__), False],
        }

        self.__abook_commands__ = {
            "add-contact": self.__assistant_handler__.add_contact,
            "add-phone": self.__assistant_handler__.add_phone,
            "add-email": self.__assistant_handler__.add_email,
            "add-birthday": self.__assistant_handler__.add_birthday,
            "add-address": self.__assistant_handler__.add_address,
            "get-birthday": self.__assistant_handler__.get_birthday,
            "get-upcoming-birthdays": self.__assistant_handler__.get_upcoming_birthdays,
            "get-phone": self.__assistant_handler__.get_phone_by_name,
            "get-contacts": self.__assistant_handler__.get_all_contacts,
            "get-info": self.__assistant_handler__.get_contact_info,
            "change-phone": self.__assistant_handler__.change_phone,
            "change-email": self.__assistant_handler__.change_email,
            "change-birthday": self.__assistant_handler__.add_birthday,
            "change-address": self.__assistant_handler__.add_address,
            "delete-contact": self.__assistant_handler__.delete_contact,
            "delete-phone": self.__assistant_handler__.delete_phone
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

        self.__pool_commands__ = [self.__abook_commands__, self.__nbook_commands__, self.__sys_commands__]

    # privat methods
    def __exit__(self, args) -> str:
        return "Bye Bye"

    # read ../README.md and show commands info
    def __show_help__(self, args) -> str:
        help: str = ""
        symb = r"[а-яА-Яa-zA-Z іїІЇєЄ -\"`]"
        try:
            current_file_path = Path(__file__).parent.parent
            file_path = current_file_path / "README.md"
            mark_read_cmd: bool = False
            with open(file=file_path, mode="r", encoding="UTF-8") as f:
                for line in f:
                    if line.find("# ") == 0:  # read name of module
                        res = re.findall(symb, line)
                        help = "\n" + "".join(res).strip() + "\n"
                    elif line.find("###") == 0:  # read name of commands block
                        res = re.findall(symb, line)
                        help += "  " + "".join(res).strip() + ":\n"
                        mark_read_cmd = True
                        # skip two technical lines
                        next(f)
                        next(f)
                    elif mark_read_cmd:
                        desc = line.split("|")
                        if len(desc) == 4:  # read command and description
                            help += f"      {desc[1].strip()}: {desc[2].strip()}\n"
                        else:
                            mark_read_cmd = False
                            help += "\n"
        except FileNotFoundError:
            pass
        except StopIteration:
            pass

        return help

    def __clear_console__(self, args) -> str:
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For macOS and Linux
            os.system('clear')

        return ""

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

    @input_error
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
        elif command in self.__sys_commands__:
            print(self.__sys_commands__[command][0](args))
            if self.__sys_commands__[command][1]:
                return True
        else:
            print("Invalid command.")
            suggestions_list = self.get_suggestion(command)
            if suggestions_list is not None and len(suggestions_list) > 0:
                commands_str: str = ", ".join(suggestions_list)
                print(f"    Did you mean: {commands_str}")
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
    def get_suggestion(self, command: str, count: int = 1, prc: float = 0.6) -> list | None:
        matches: list = []
        for cmd_dic in self.__pool_commands__:
            matches += difflib.get_close_matches(command, cmd_dic.keys(), n=count, cutoff=max(0.2, min(1, prc)))

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
