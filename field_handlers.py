from address_book import AddressBook
from decorators import input_error


@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Correct format: add-address [Contact name] [address]")

    name, *address_parts = args
    record = book.get(name)

    action = "updated" if record.address else "added"
    record.add_address(" ".join(address_parts))
    return f"Address {action}"


@input_error
def add_email(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Correct format: add-email [Contact name] [email]")

    name, email = args
    record = book.get(name)

    action = "updated" if record.email else "added"
    record.add_email(email)
    return f"Email {action}"


EDITABLE_FIELDS = {
    "name": lambda book, record, value: book.rename(record.name.value, value),
    "address": lambda book, record, value: record.add_address(value),
    "email": lambda book, record, value: record.add_email(value),
    "birthday": lambda book, record, value: record.add_birthday(value),
}


@input_error
def edit_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Correct format: edit [Contact name] [name|address|email|birthday] [new value]")

    name, field, *value_parts = args
    field = field.lower()
    if field not in EDITABLE_FIELDS:
        raise ValueError(f"Unknown field '{field}'. Use: {', '.join(EDITABLE_FIELDS)}")

    # names are one word: a name with a space could never be typed as a command argument
    if field == "name" and len(value_parts) != 1:
        raise ValueError("Contact name must be a single word")

    record = book.get(name)

    EDITABLE_FIELDS[field](book, record, " ".join(value_parts))
    return f"Contact {field} updated"
