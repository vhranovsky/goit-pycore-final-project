# тут створюємо спільні винятки, констатнти та інші спілні для всього модуля функції

# Базовий виняток для помилок валідації.
class ValidError(Exception):
    pass


# Виняток для невалідного номера телефону.
class ValidPhoneError(ValidError):
    pass


# Виняток для невалідної дати народження.
class ValidBdayError(ValidError):
    pass


# Виняток для невалідної електронної пошти.
class ValidEmailError(ValidError):
    pass


# Виняток для невалідного контенту нотатки.
class ValidNoteContentError(ValidError):
    pass


# Виняток для невалідного тегу.
class ValidTagError(ValidError):
    pass


# Виняток для невалідного пошукового запиту.
class ValidSearchQueryError(ValidError):
    pass


# Константи
INVALID_PHONE = "Inavlid phone number! " \
    "Enter the phone number in the format 10 digits"
INVALID_ARGUMENTS = "Enter valid arguments for the command."
KEY_ERROR = "Record is missing!"
INVALID_COMMAND = "Enter valid command."
INVALID_BDAY = "Invalid date format. Use DD.MM.YYYY"
INVALID_EMAIl = "Invalid email format. Use xxx@xxx.xx"
INVALID_NOTE_CONTENT = "Note content cannot be empty."
INVALID_TAG = "Tag cannot be empty."
INVALID_SEARCH_QUERY = "Search query cannot be empty."


# Декоратор
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return INVALID_ARGUMENTS
        except KeyError:
            return KEY_ERROR
        except ValidPhoneError:
            return INVALID_PHONE
        except ValidBdayError:
            return INVALID_BDAY
        except ValidEmailError:
            return INVALID_EMAIl
        except ValidNoteContentError:
            return INVALID_NOTE_CONTENT
        except ValidTagError:
            return INVALID_TAG
        except ValidSearchQueryError:
            return INVALID_SEARCH_QUERY
        except ValueError:
            return INVALID_ARGUMENTS
        except AttributeError:
            return KEY_ERROR
        except TypeError:
            return KEY_ERROR
    return inner
