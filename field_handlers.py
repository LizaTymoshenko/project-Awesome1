from address_book import AddressBook
from decorators import input_error


@input_error
def add_address(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Correct format: add-address [Contact name] [address]")

    name, *address_parts = args
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} not found")

    record.add_address(" ".join(address_parts))
    return "Address added"


@input_error
def add_email(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError("Correct format: add-email [Contact name] [email]")

    name, email = args
    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} not found")

    record.add_email(email)
    return "Email added"
