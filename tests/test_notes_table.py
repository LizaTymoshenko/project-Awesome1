import pytest

from console import render_notes_table
from note_handlers import search_notes, search_tag, show_notes, sort_notes
from notes import NoteBook


@pytest.fixture
def notebook():
    notebook = NoteBook()
    notebook.add_note("Buy milk", ["food", "shop"])
    notebook.add_note("Weekly report", ["work"])
    notebook.add_note("Call mom")
    return notebook


def test_table_shows_headers_text_and_tags(notebook):
    table = render_notes_table(notebook.get_all_notes())

    for part in ["Notes", "ID", "Text", "Tags", "Buy milk", "food, shop", "work"]:
        assert part in table


def test_note_without_tags_shows_dash():
    notebook = NoteBook()
    notebook.add_note("Call mom")

    table = render_notes_table(notebook.get_all_notes())

    assert "Call mom" in table
    assert "-" in table


def test_show_notes_empty_notebook():
    assert show_notes([], NoteBook()) == "No notes yet"


def test_show_notes_lists_every_note(notebook):
    table = show_notes([], notebook)

    for text in ["Buy milk", "Weekly report", "Call mom"]:
        assert text in table


def test_search_notes_finds_by_part_of_text(notebook):
    table = search_notes(["MILK"], notebook)

    assert "Buy milk" in table
    assert "Weekly report" not in table


def test_search_notes_nothing_found(notebook):
    assert search_notes(["xyz"], notebook) == "No notes found"


def test_search_tag_finds_exact_tag(notebook):
    table = search_tag(["WORK"], notebook)

    assert "Weekly report" in table
    assert "Buy milk" not in table


def test_search_tag_nothing_found(notebook):
    assert search_tag(["wor"], notebook) == "No notes found"


def test_sort_notes_groups_in_alphabetical_order_untagged_last(notebook):
    text = sort_notes([], notebook)

    assert text.index("#food") < text.index("#shop") < text.index("#work") < text.index("No tag")


def test_sort_notes_note_with_two_tags_is_in_both_groups(notebook):
    text = sort_notes([], notebook)

    assert text.count("Buy milk") == 2


def test_sort_notes_empty_notebook():
    assert sort_notes([], NoteBook()) == "No notes yet"