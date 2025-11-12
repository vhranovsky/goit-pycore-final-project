import address_book
import note_book
import os


INVALID_PHONE = "Inavlid phone number! " \
    "Enter the phone number in the format 10 digits"
INVALID_ARGUMENTS = "Enter valid arguments for the command."
KEY_ERROR = "Record is missing!"
INVALID_COMMAND = "Enter valid command."
INVALID_BDAY = "Invalid date format. Use DD.MM.YYYY"
INVALID_EMAIl = "Invalid email format. Use xxx@xxx.xx"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return INVALID_ARGUMENTS
        except KeyError:
            return KEY_ERROR
        except address_book.ValidPhoneError:
            return INVALID_PHONE
        except address_book.ValidBdayError:
            return INVALID_BDAY
        except address_book.ValidEmailError:
            return INVALID_EMAIl
        except ValueError:
            return INVALID_ARGUMENTS
        except AttributeError:
            return KEY_ERROR
        except TypeError:
            return KEY_ERROR
    return inner


class PersonalAssistantHandler:
    def __init__(self):
        pass

    # handlers
    def clear_console(self):
        if os.name == 'nt':  # For Windows
            os.system('cls')
        else:  # For macOS and Linux
            os.system('clear')

    @input_error
    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args

    @input_error
    def add_contact(self, args: list, book: address_book.AddressBook) -> str:
        name = args[0]
        phone = args[1] if len(args) > 1 else None
        email = args[2] if len(args) > 2 else None
        bday = args[3] if len(args) > 3 else None
        address = args[4] if len(args) > 4 else None

        name = name.capitalize()
        record = book.find(name)

        message = f"Contact {name} updated."
        if record is None:
            record = address_book.Record(name)
            book.add_record(record)
            message = f"Contact {name} added."

        if phone is not None:
            record.add_phone(phone)

        if email is not None:
            record.add_email(email)

        if bday is not None:
            record.add_birthday(bday)

        if address is not None:
            args.remove(name)
            args.remove(phone)
            args.remove(email)
            args.remove(bday)
            args.remove(address)
            address +=" " + " ".join(args)
            record.add_address(address)

        return message

    @input_error
    def add_email(self, args: list, book: address_book.AddressBook) -> str:
        name, email, *_ = args

        name = name.capitalize()
        record = book.find(name)

        message = f"Contact {name} updated."
        if record is None:
            record = address_book.Record(name)
            book.add_record(record)
            message = f"Contact {name} added."

        record.add_email(email)
        return message

    @input_error
    def add_phone(self, args: list, book: address_book.AddressBook) -> str:
        name, phone, *_ = args

        name = name.capitalize()
        record = book.find(name)

        message = f"Contact {name} updated."
        if record is None:
            record = address_book.Record(name)
            book.add_record(record)
            message = f"Contact {name} added."

        record.add_phone(phone)
        return message

    @input_error
    def add_address(self, args: list, book: address_book.AddressBook) -> str:
        name, address, *_ = args

        args.remove(name) 
        args.remove(address)
        address +=" " + " ".join(args)

        name = name.capitalize()
        record = book.find(name)

        message = f"Contact {name} updated."
        if record is None:
            record = address_book.Record(name)
            book.add_record(record)
            message = f"Contact {name} added."
        
        record.add_address(address)
        return message

    @input_error
    def change_phone(self, args: list, book: address_book.AddressBook) -> str:
        name, old_phone, new_phone, *_ = args

        name = name.capitalize()
        record = book.find(name)
        if record is None:
            return self.add_contact(args, book)

        if record.find_phone(old_phone) is None:
            return f"The phone number {old_phone} does not belong to {name}."

        if record.find_phone(new_phone) is not None:
            return f"The phone number {new_phone} belong to {name}."

        record.edit_phone(old_phone, new_phone)
        return f"Phone {old_phone} changed to {new_phone} for {name}."

    @input_error
    def change_email(self, args: list, book: address_book.AddressBook) -> str:
        name, old_email, new_email, *_ = args

        name = name.capitalize()
        record = book.find(name)

        if record is None:
            return self.add_contact(args, book)

        if record.email is not None and record.email.value != old_email:
            return f"Email {old_email} does not belong to {name}."

        if record.email is not None and record.email.value == new_email:
            return f"Email {new_email} belong to {name}."

        record.add_email(new_email)
        return f"Email {old_email} changed to {new_email} for {name}."

    @input_error
    def get_phone_by_name(self, args: list, book: address_book.AddressBook) -> str:
        name = args[0]
        name = name.capitalize()

        record = book.find(name)
        return list(map(lambda phone: phone.value, record.phones))

    @input_error
    def add_birthday(self, args: list, book: address_book.AddressBook):
        name, bday, *_ = args

        name = name.capitalize()
        record = book.find(name)
        record.add_birthday(bday)

        return f"Birthday {record.birthday.value} successfully added for {record.name.value} "

    @input_error
    def get_birthday(self, args: list, book: address_book.AddressBook) -> str:
        name = args[0]
        name = name.capitalize()

        record = book.find(name)
        return record.birthday if record.birthday is not None else "Birthday record absent."

    @input_error
    def get_contact_info(self, args: list, book: address_book.AddressBook) -> str:
        name = args[0]
        name = name.capitalize()

        record = book.find(name)
        return str(record) if record is not None else "Record is missing."

    @input_error
    def birthdays(self, args: list, book: address_book.AddressBook) -> str:
        try:
            days : int = int(args[0]) if len(args)>0 else 7
        except Exception:
            days = 7
        finally:
            return book.get_upcoming_birthdays(days)

    def get_all_contacts(self, args: list, book: address_book.AddressBook) -> str:
        return f"{book}"
