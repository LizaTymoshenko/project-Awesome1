from address_book import AddressBook, Record
from decorators import input_error


@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Correct format: add-address [Contact name] [address]")

    name, *address_parts = args
    record = book.find(name)

    action = "updated" if record.address else "added"
    record.add_address(" ".join(address_parts))
    return f"Address {action}"


@input_error
def add_email(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Correct format: add-email [Contact name] [email]")

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


@input_error
def edit_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Correct format: edit [Contact name] [name|address|email|birthday] [new value]")

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
