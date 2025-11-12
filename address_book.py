from collections import UserDict
import re
from datetime import datetime, timedelta
from general import ValidPhoneError
from general import ValidEmailError
from general import ValidBdayError


# --- БЛОК ОСНОВНИХ КЛАСІВ AddressBook ---

# Базовий клас для всіх полів (ім'я, телефон, дата народження).
class Field:

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


# Клас для зберігання імені. Успадковує Field.
class Name(Field):
    pass


# Клас для зберігання номера телефону. Включає валідацію.
class Phone(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone: str):
        # Валідація номера телефону (має бути 10 цифр).
        if not (isinstance(phone, str) and re.match(r"^\d{10}$", phone)):
            raise ValidPhoneError("Invalid phone format.")
        self.__value = phone


# Клас для зберігання дати народження. Включає валідацію.
class Birthday(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        # Валідація дати. Приймає рядок 'DD.MM.YYYY' і зберігає як об'єкт date.
        try:
            parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
            self.__value = parsed_date
        except ValueError:
            raise ValidBdayError("Invalid date format. Expect 'DD.MM.YYYY'.")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


# Клас для зберігання email. Включає валідацію.
class Email(Field):

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, email: str):
        if not (isinstance(email, str) and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)):
            raise ValidEmailError("Invalid email format.")
        self.__value = email


# Клас для зберігання адреси.
class Address(Field):
    pass


# Клас для зберігання запису про контакт.
class Record:

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def add_phone(self, phone_number: str):
        if not self.find_phone(phone_number):
            phone = Phone(phone_number)
            self.phones.append(phone)

    def add_birthday(self, bday: str):
        self.birthday = Birthday(bday)

    def add_email(self, email: str):
        self.email = Email(email)

    def add_address(self, address: str):
        self.address = Address(address)

    def remove_phone(self, phone_number: str):
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        phone_to_edit = self.find_phone(old_phone_number)
        if phone_to_edit is not None:
            phone_to_edit.value = new_phone_number

    def find_phone(self, phone_number: str) -> Phone | None:
        phones = list(filter(lambda phone: phone.value == phone_number, self.phones))
        return phones[0] if len(phones) > 0 else None

    def __str__(self) -> str:
        phones_str = ", ".join(str(p) for p in self.phones) or "None"
        bday_str = str(self.birthday) if self.birthday else "Not set"
        email_str = str(self.email) if self.email else "Not set"
        address_str = str(self.address) if self.address else "Not set"

        return (f"  Contact: {self.name.value}\n"
                f"      Phones: {phones_str}\n"
                f"      Email: {email_str}\n"
                f"      Adress: {address_str}\n"
                f"      Birthday: {bday_str}")


# Клас для зберігання адресної книги.
class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7) -> list:
        result = []
        curr_date: datetime.date = datetime.today().date()
        user_bday_date_corrected: datetime.date = None

        for key, record in self.data.items():
            if record.birthday is None:
                continue

            user_bday_date: datetime.date = record.birthday.value

            if curr_date.month == 12 and user_bday_date.month == 1:
                user_bday_date_corrected = user_bday_date.replace(year=curr_date.year+1)
            else:
                user_bday_date_corrected = user_bday_date.replace(year=curr_date.year)

            time_delta = user_bday_date_corrected - curr_date
            if 0 <= time_delta.days <= days:
                if user_bday_date_corrected.weekday() > 4:
                    increment_days = timedelta(days=7-user_bday_date_corrected.weekday())
                    user_bday_date_corrected += increment_days

                time_delta = user_bday_date_corrected - curr_date
                if time_delta.days >= 0 and time_delta.days <= days:
                    result.append(f"{record.name.value}'s birthday {user_bday_date_corrected.strftime("%d.%m.%Y")}")
        return result

    # Пошук контактів за частковим збігом в імені,
    # телефонах, email або адресі (нечутливий до регістру).
    def search(self, query: str) -> list[Record]:
        results = []
        query_lower = query.lower()

        for record in self.data.values():
            if query_lower in record.name.value.lower():
                results.append(record)
                continue

            if record.email and query_lower in record.email.value.lower():
                results.append(record)
                continue

            if record.address and query_lower in record.address.value.lower():
                results.append(record)
                continue

            for phone in record.phones:
                if query_lower in phone.value:
                    results.append(record)
                    break

        return results

    def __str__(self):
        if not self.data:
            return "Adress book is empty."

        return "\n".join(str(record) for record in self.data.values())
