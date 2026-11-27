from address_book.address_book import AddressBook, Record
from registry.command_registry import CommandFormatError


def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise CommandFormatError

    name, *address_parts = args
    record = book.find(name)

    action = "updated" if record.address else "added"
    record.add_address(" ".join(address_parts))
    return f"Address {action}"


def add_email(args, book: AddressBook):
    if len(args) != 2:
        raise CommandFormatError

    name, email = args
    record = book.find(name)

    action = "updated" if record.email else "added"
    record.add_email(email)
    return f"Email {action}"


# setters that only need the record and the new value; "name" is handled by the book itself
RECORD_SETTERS = {
    "address": Record.add_address,
    "email": Record.add_email,
    "birthday": Record.add_birthday,
}
EDITABLE_FIELDS = ["name", *RECORD_SETTERS]


def edit_contact(args, book: AddressBook):
    if len(args) < 3:
        raise CommandFormatError

    name, field, *value_parts = args
    field = field.lower()
    if field not in EDITABLE_FIELDS:
        raise ValueError(f"Unknown field '{field}'. Use: {', '.join(EDITABLE_FIELDS)}")

    value = " ".join(value_parts)
    if field == "name":
        # names are one word: a name with a space could never be typed as a command argument
        if len(value_parts) != 1:
            raise ValueError("Contact name must be a single word")
        book.rename(name, value)
    else:
        RECORD_SETTERS[field](book.find(name), value)
    return f"Contact {field} updated"
