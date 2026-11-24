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
