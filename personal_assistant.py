import address_book
import note_book
import pickle
import os
from personal_assistant_handler import PersonalAssistantHandler
import difflib

# Наш бот
class PersonalAssistant:
    def __init__(self):
        self.__abook__ = None
        self.__nbook__ = None
        self.__assistant_handler__ = PersonalAssistantHandler()

        self.__abook_commands__= {
            "add" : self.__assistant_handler__.add_contact,
            "add-phone" : self.__assistant_handler__.add_phone,
            "add-email" : self.__assistant_handler__.add_email,
            "add-birthday" : self.__assistant_handler__.add_birthday,
            "add-address" : self.__assistant_handler__.add_address,
            "get-birthday" : self.__assistant_handler__.get_birthday,
            "get-birthdays" : self.__assistant_handler__.birthdays,
            "get-phone" : self.__assistant_handler__.get_phone_by_name,
            "get-all" : self.__assistant_handler__.get_all_contacts,
            "get-info" : self.__assistant_handler__.get_contact_info,
            "change-phone" : self.__assistant_handler__.change_phone,
            "change-email" : self.__assistant_handler__.change_email,
            "change-birthday" : self.__assistant_handler__.add_birthday,
            "change-address" : self.__assistant_handler__.add_address
         }
        
        self.__nbook_commands__= {
        }

    # Приватні методи
    def __load_abook__(self, file_name: str) -> address_book.AddressBook:
        try:
            with open(file_name, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return address_book.AddressBook()

    def __load_nbook__(self, file_name: str) -> note_book.NoteBook:
        try:
            with open(file_name, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
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
    def __parse_input__(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    def get_suggestion(self, command) -> list | None:
        # cutoff=0.6 означає, що команда має бути схожа принаймні на 60%
        matches = difflib.get_close_matches(command, self.__abook_commands__.keys(), n=1, cutoff=0.6)
        return matches

    def __main_run__(self):
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = self.__parse_input__(user_input)

            if command in self.__abook_commands__:
                print(self.__abook_commands__[command](args, self.__abook__))
            elif command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "clear":
                self.__assistant_handler__.clear_console()
            else:
                print("Invalid command.")
                suggestions_list = self.get_suggestion(command)
                if suggestions_list is not None:
                    print(f"    You may have tried the following commands: {suggestions_list}")

    # public methods
    def run(self):
        self.__load__()
        self.__main_run__()
        self.__save__()


if __name__ == "__main__":
    PersonalAssistant().run()
