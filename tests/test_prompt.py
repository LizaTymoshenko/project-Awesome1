from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.document import Document

from prompt import format_hint

HINTS = {"add": "add [Contact name] [phone number]", "add-email": "add-email [Contact name] [email]", "all": "all"}


def completions(text):
    completer = NestedCompleter.from_nested_dict({name: None for name in HINTS})
    return [c.text for c in completer.get_completions(Document(text), None)]


def test_command_names_are_completed_by_their_first_letters():
    assert sorted(completions("ad")) == ["add", "add-email"]
    assert completions("al") == ["all"]


def test_nothing_is_completed_after_the_command_name():
    assert completions("add Bob 05") == []


def test_hint_shows_the_format_of_the_typed_command():
    assert format_hint("add-email Bob", HINTS) == "add-email [Contact name] [email]"
    assert format_hint("ADD", HINTS) == "add [Contact name] [phone number]"


def test_no_hint_for_empty_or_unknown_input():
    assert format_hint("", HINTS) == ""
    assert format_hint("blah", HINTS) == ""
