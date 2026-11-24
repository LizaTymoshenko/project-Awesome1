from address_book import Record, AddressBook
from decorators import input_error



# functions layer between the user and the classes
@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Correct format: add [Contact name] [phone number]")

    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added"
    
    record.add_phone(phone)
    return "Contact updated"


@input_error
def delete_contact(args, book):
    if len(args) < 1:
        raise ValueError("Correct format: delete [Contact name]")
    
    name, *_ = args
    book.delete(name)
    return "Contact deleted"



@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Correct format: change [Contact name] [Old phone] [Newphone]")

    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise ValueError("No such contact")

    record.edit_phone(old_phone, new_phone)
    return "Contact updated"


@input_error
def show_phone(args, book):
    if len(args) != 1:
        raise ValueError("Correct format: phone [Contact name]")

    name, *_ = args
    record = book.find(name)

    if record is None:
        raise ValueError("Contact not found")

    return f"{record.name} {', '.join(str(phone) for phone in record.phones)}"


@input_error
def show_all_contacts(args, book: AddressBook):
    if book.is_empty():
        return "Contact book is empty"
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Correct format:  add-birthday [Contact name] DD.MM.YYYY in digits")
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "No such contact"

    record.add_birthday(birthday)
    return "Birth date added"


@input_error
def show_birthday(args, book):
    if len(args) != 1:
        raise ValueError("Correct format: show-birthday [Contact name] ")
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "No such contact"

    if record.birthday is None:
        return "No information"
    return f"{name} celebrates birthday on {record.birthday}"


@input_error
def show_upcoming_birthdays(args, book: AddressBook):
    if book.is_empty():
        return "Contact book is empty"

    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays next week"
    result = ""
    for user in upcoming:
        result += f"{user['name']}: {user['congratulation_date']}\n"
    return result

