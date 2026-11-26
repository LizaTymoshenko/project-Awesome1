from pathlib import Path

import pytest

import storage
from address_book import AddressBook, Record
from notes import NoteBook


@pytest.fixture(autouse=True)
def data_file(tmp_path, monkeypatch):
    path = tmp_path / ".personal_assistant" / "assistant.pkl"  # folder does not exist yet
    monkeypatch.setattr(storage, "DATA_FILE", path)
    return path


def book_with_bob():
    book = AddressBook()
    bob = Record("Bob")
    bob.add_phone("0501112233")
    bob.add_email("bob@mail.com")
    book.add_record(bob)
    return book


def test_default_location_is_in_the_user_home_folder():
    assert Path.home() / ".personal_assistant" in storage.DEFAULT_DATA_FILE.parents


def test_save_creates_the_folder_and_load_restores_the_data(data_file):
    storage.save_data(book_with_bob(), NoteBook())

    assert data_file.exists()
    loaded, _ = storage.load_data()
    assert str(loaded.find("Bob").phones[0]) == "0501112233"
    assert loaded.find("Bob").email == "bob@mail.com"


def test_notes_and_their_ids_survive_a_restart():
    notebook = NoteBook()
    notebook.add_note("Buy milk", ["home"])
    notebook.add_note("Call mom")
    notebook.delete_note(1)
    storage.save_data(AddressBook(), notebook)

    _, loaded = storage.load_data()

    assert loaded.find_note(2).text == "Call mom"
    assert loaded.add_note("New").note_id == 3  # ids are not reused after restart


def test_missing_file_gives_an_empty_book_and_notebook():
    book, notebook = storage.load_data()
    assert book.is_empty()
    assert notebook.data == {}


def test_save_leaves_no_temp_file_behind(data_file):
    storage.save_data(book_with_bob(), NoteBook())
    assert list(data_file.parent.iterdir()) == [data_file]


@pytest.mark.parametrize("garbage", [b"this is not a pickle", b"garbage\n", b"", b"\x80\x04\x95"])
def test_corrupted_file_gives_an_empty_book_and_is_kept_aside(data_file, capsys, garbage):
    data_file.parent.mkdir(parents=True)
    data_file.write_bytes(garbage)

    book, notebook = storage.load_data()
    assert book.is_empty() and notebook.data == {}

    assert not data_file.exists()
    assert data_file.with_suffix(".corrupt").read_bytes() == garbage
    assert "Could not read saved data" in capsys.readouterr().out


def test_file_without_the_book_is_treated_as_corrupted(data_file):
    import pickle

    data_file.parent.mkdir(parents=True)
    data_file.write_bytes(pickle.dumps({"something": "else"}))

    book, _ = storage.load_data()
    assert book.is_empty()
    assert data_file.with_suffix(".corrupt").exists()


def test_file_saved_without_notes_keeps_the_contacts(data_file):
    import pickle

    data_file.parent.mkdir(parents=True)
    data_file.write_bytes(pickle.dumps({"book": book_with_bob()}))

    book, notebook = storage.load_data()

    assert book.find("Bob").email == "bob@mail.com"
    assert notebook.data == {}
    assert not data_file.with_suffix(".corrupt").exists()
