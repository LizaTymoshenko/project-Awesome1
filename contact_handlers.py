from address_book import Record, AddressBook
from decorators import input_error
from console import render_contacts_table
from command_registry import CommandFormatError
from decorators import input_error
from console import render_contacts_table


# functions layer between the user and the classes
def add_contact(args, book):
    if len(args) < 2:
        raise CommandFormatError
    
    name, phone, *_ = args

    if name in book:
        book.find(name).add_phone(phone)
        return "Contact updated"

    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added"


def delete_contact(args, book):
    if len(args) < 1:
        raise CommandFormatError
    
    name, *_ = args
    book.delete(name)
    return "Contact deleted"


def change_contact(args, book):
    if len(args) < 3:
        raise CommandFormatError

    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    record.edit_phone(old_phone, new_phone)
    return "Contact updated"


def show_phone(args, book):
    if len(args) != 1:
        raise CommandFormatError

    name, *_ = args
    record = book.find(name)

    return f"{record.name} {', '.join(str(phone) for phone in record.phones)}"


def show_all_contacts(args, book: AddressBook):
    if book.is_empty():
        return "Contact book is empty"
    return book.show_all()


def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise CommandFormatError
    name, birthday, *_ = args
    record = book.find(name)

    record.add_birthday(birthday)
    return "Birth date added"


def show_birthday(args, book):
    if len(args) != 1:
        raise CommandFormatError
    name, *_ = args
    record = book.find(name)

    if record.birthday is None:
        return "No information"
    return f"{name} celebrates birthday on {record.birthday}"


def show_upcoming_birthdays(args, book: AddressBook):
    if book.is_empty():
        return "Contact book is empty"
    if len(args) > 0:
        n_days, *_ = args
        # check if n_days is positive integer
        try:
            n_days = int(n_days)
            if n_days <= 0:
                raise ValueError
        except ValueError:
            return "Number of days should be positive integer."
    else:
        n_days = 7
    upcoming = book.get_upcoming_birthdays(n_days)
    if not upcoming:
        return f"No birthdays in the upcoming {n_days} days"
    result = ""
    for user in upcoming:
        result += f"{user['name']}: {user['congratulation_date']}\n"
    return result

@input_error
def search_contacts(args, book: AddressBook):
    if len(args) < 1:
        raise ValueError("Correct format: search [name, phone, e-mail]")
    query = " ".join(args)
    found = book.search(query)
    if not found:
        return "Nothing found"
    return render_contacts_table(found)
