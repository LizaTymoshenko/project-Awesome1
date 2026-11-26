import pickle

import pytest

from address_book import AddressBook, Record
from command_registry import CommandFormatError
from contact_handlers import show_all_contacts
from field_handlers import add_address, add_email, edit_contact


@pytest.fixture
def book():
    book = AddressBook()
    record = Record("Bob")
    record.add_phone("0501112233")
    book.add_record(record)
    return book


# US-03: add-address, add-email, all

def test_add_address_keeps_spaces(book):
    assert add_address(["Bob", "Kyiv,", "Main", "st", "1"], book) == "Address added"
    assert book.find("Bob").address == "Kyiv, Main st 1"


def test_replacing_address_says_updated(book):
    add_address(["Bob", "Kyiv"], book)
    assert add_address(["Bob", "Lviv"], book) == "Address updated"
    assert book.find("Bob").address == "Lviv"


def test_add_email_and_replace(book):
    assert add_email(["Bob", "bob@mail.com"], book) == "Email added"
    assert add_email(["Bob", "b2@mail.com"], book) == "Email updated"
    assert book.find("Bob").email == "b2@mail.com"


@pytest.mark.parametrize("handler", [add_address, add_email])
def test_unknown_contact_raises(book, handler):
    with pytest.raises(ValueError, match="Contact Nobody not found"):
        handler(["Nobody", "value"], book)


def test_missing_arguments_raise_format_error(book):
    with pytest.raises(CommandFormatError):
        add_address(["Bob"], book)

    with pytest.raises(CommandFormatError):
        add_email(["Bob"], book)


def test_all_shows_every_field(book):
    add_email(["Bob", "bob@mail.com"], book)
    add_address(["Bob", "Kyiv", "1"], book)
    book.find("Bob").add_birthday("01.02.1990")

    line = show_all_contacts([], book)

    for part in ["Bob", "0501112233", "bob@mail.com", "Kyiv 1", "01.02.1990"]:
        assert part in line


def test_all_has_a_column_per_field_and_dash_for_empty_values(book):
    table = show_all_contacts([], book)

    for header in ["Name", "Phones", "Email", "Address", "Birthday"]:
        assert header in table

    assert table.count("-") >= 3  # email, address, birthday are empty


def test_record_saved_before_new_fields_still_loads():
    old = Record.__new__(Record)
    old.__dict__.update(name="Old", phones=[], birthday=None)  # no email/address

    loaded = pickle.loads(pickle.dumps(old))

    assert loaded.email is None
    assert loaded.address is None


# US-04: email validation on add and edit

def test_invalid_email_is_not_saved_on_add(book):
    add_email(["Bob", "bob@mail.com"], book)

    with pytest.raises(ValueError, match="Invalid email"):
        add_email(["Bob", "bob@"], book)

    assert book.find("Bob").email == "bob@mail.com"


def test_invalid_email_is_not_saved_on_edit(book):
    add_email(["Bob", "bob@mail.com"], book)

    with pytest.raises(ValueError, match="Invalid email"):
        edit_contact(["Bob", "email", "bob@"], book)

    assert book.find("Bob").email == "bob@mail.com"


# US-05: edit

def test_edit_name_moves_record_to_new_key(book):
    assert edit_contact(["Bob", "name", "Robert"], book) == "Contact name updated"
    assert "Bob" not in book
    assert str(book.find("Robert").name) == "Robert"
    assert [str(phone) for phone in book.find("Robert").phones] == ["0501112233"]


def test_edit_name_to_existing_contact_is_rejected(book):
    book.add_record(Record("Ann"))

    with pytest.raises(ValueError, match="Contact Ann already exists"):
        edit_contact(["Bob", "name", "Ann"], book)

    assert "Bob" in book


def test_edit_name_must_be_single_word(book):
    with pytest.raises(ValueError, match="single word"):
        edit_contact(["Bob", "name", "Anna", "Maria"], book)

    assert "Bob" in book


def test_edit_address_and_email(book):
    edit_contact(["Bob", "address", "Kyiv", "1"], book)
    edit_contact(["Bob", "email", "bob@mail.com"], book)

    assert book.find("Bob").address == "Kyiv 1"
    assert book.find("Bob").email == "bob@mail.com"


@pytest.mark.parametrize("date", ["31.02.1990", "1990-02-01", "01.01.2999"])
def test_edit_birthday_rejects_bad_dates(book, date):
    with pytest.raises(ValueError, match=r"Invalid date|future"):
        edit_contact(["Bob", "birthday", date], book)

    assert book.find("Bob").birthday is None


def test_edit_birthday_valid(book):
    assert edit_contact(["Bob", "birthday", "01.02.1990"], book) == "Contact birthday updated"
    assert str(book.find("Bob").birthday) == "01.02.1990"


def test_edit_unknown_field_and_contact(book):
    with pytest.raises(ValueError, match="Unknown field"):
        edit_contact(["Bob", "nickname", "x"], book)

    with pytest.raises(ValueError, match="Contact Nobody not found"):
        edit_contact(["Nobody", "email", "a@b.com"], book)


def test_edit_with_missing_arguments_raises_format_error(book):
    with pytest.raises(CommandFormatError):
        edit_contact(["Bob"], book)


# console.render_table is shared by contacts and (later) notes

def test_render_table_shows_title_headers_and_cells():
    from console import render_table

    table = render_table(
        "Notes",
        [("ID", "cyan"), ("Text", "")],
        [["1", "Buy milk"], ["2", "Call Bob"]],
    )

    for part in ["Notes", "ID", "Text", "Buy milk", "Call Bob"]:
        assert part in table


# AddressBook.find raises instead of returning None

def test_find_and_delete_unknown_contact_raise(book):
    with pytest.raises(ValueError, match="Contact Nobody not found"):
        book.find("Nobody")

    with pytest.raises(ValueError, match="Contact Nobody not found"):
        book.delete("Nobody")