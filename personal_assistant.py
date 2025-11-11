import address_book
import note_book
import pickle
import os
from personal_assistant_handler import PersonalAssistantHandler


# Наш бот
class PersonalAssistant:
    def __init__(self):
        self.__abook__ = None
        self.__nbook__ = None
        self.__assistant_handler__ = None

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

    def __main_run__(self):
        self.__assistant_handler__ = PersonalAssistantHandler()
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = self.__parse_input__(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(self.__assistant_handler__.add_contact(args, self.__abook__))
            elif command == "add-phone":
                print(self.__assistant_handler__.add_phone(args, self.__abook__))
            elif command == "add-email":
                print(self.__assistant_handler__.add_email(args, self.__abook__))
            elif command == "add-birthday":
                print(self.__assistant_handler__.add_birthday(args, self.__abook__))
            elif command == "get-birthday":
                print(self.__assistant_handler__.get_birthday(args, self.__abook__))
            elif command == "get-birthdays":
                print(self.__assistant_handler__.birthdays(args, self.__abook__))
            elif command == "get-phone":
                print(self.__assistant_handler__.get_phone_by_name(args, self.__abook__))
            elif command == "get-all":
                print(self.__assistant_handler__.get_all_contacts(args, self.__abook__))
            elif command == "get-info":
                print(self.__assistant_handler__.get_contact_info(args, self.__abook__))
            elif command == "change-phone":
                print(self.__assistant_handler__.change_phone(args, self.__abook__))
            elif command == "change-email":
                print(self.__assistant_handler__.change_email(args, self.__abook__))
            elif command == "change-birthday":
                print(self.__assistant_handler__.add_birthday(args, self.__abook__))
            elif command == "clear":
                self.__assistant_handler__.clear_console()
            else:
                print("Invalid command.")

    # public methods
    def run(self):
        self.__load__()
        self.__main_run__()
        self.__save__()


if __name__ == "__main__":
    PersonalAssistant().run()
