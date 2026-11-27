import main
import pytest
from address_book.address_book import AddressBook, Record
from handlers import command_handlers
from handlers.command_handlers import execute_command
from helpers.decorators import COMMAND_ERROR_MESSAGE
from notebook.notes import NoteBook
from registry.command_registry import Command
from registry.commands import init_registry


@pytest.mark.parametrize(
    ("args", "error_message"),
    [
        (["email"], "Correct format: add [Contact name] [phone number]"),
        (["email", "Bob", "bob@example.com"], "phone has to be 10 digit characters long"),
    ],
)
def test_failed_add_suggests_add_email(args, error_message):
    book = AddressBook()
    response = execute_command("add", args, book, NoteBook(), init_registry())

    assert response.startswith(f"{error_message}\nPossibly you wanted to enter this command:\n")
    assert "add-email [Contact name] [email]" in response
    assert book.is_empty()


@pytest.mark.parametrize(
    ("command", "args", "expected_message"),
    [
        ("add", ["email", "0501234567"], "Contact added"),
        ("search", ["Bob"], "Nothing found"),
    ],
)
def test_success_skips_suggestion_lookup(monkeypatch, command, args, expected_message):
    def unexpected_lookup(*args):
        pytest.fail("Successful commands should skip suggestion lookup")

    monkeypatch.setattr(command_handlers, "show_close_matches", unexpected_lookup)

    assert execute_command(command, args, AddressBook(), NoteBook(), init_registry()) == expected_message


def test_invalid_birthday_days_return_validation_message():
    book = AddressBook()
    book.add_record(Record("Bob"))
    response = execute_command("birthdays", ["-1"], book, NoteBook(), init_registry())

    assert response == "Number of days should be positive integer."


def test_failure_without_alternative_shows_only_the_error():
    response = execute_command("add", [], AddressBook(), NoteBook(), init_registry())

    assert response == "Correct format: add [Contact name] [phone number]"


def test_unknown_command_still_gets_suggestions():
    response = execute_command("add-emal", [], AddressBook(), NoteBook(), init_registry())

    assert response.startswith("Possibly you wanted to enter this command:\n")
    assert "add-email [Contact name] [email]" in response


def test_unexpected_handler_error_returns_text():
    def broken_handler():
        raise RuntimeError("Internal error")

    command = Command("broken", "broken", "Broken command", broken_handler, "base")
    registry = init_registry()
    registry.register(command)

    assert execute_command("broken", [], AddressBook(), NoteBook(), registry) == COMMAND_ERROR_MESSAGE


def test_cli_continues_after_unexpected_command_error(monkeypatch, capsys):
    commands = iter(["add", "hello", "exit"])
    monkeypatch.setattr(main, "create_command_input", lambda hints: lambda prompt: next(commands))
    monkeypatch.setattr(main, "load_data", lambda: (AddressBook(), NoteBook()))

    def broken_lookup(*args):
        raise RuntimeError("Lookup failed")

    monkeypatch.setattr(command_handlers, "show_close_matches", broken_lookup)
    monkeypatch.setattr(main, "save_data", lambda book, notebook: None)

    main.main()

    assert capsys.readouterr().out.splitlines()[-4:] == [
        COMMAND_ERROR_MESSAGE,
        "How can I help you?",
        "",
        "Good bye!",
    ]
