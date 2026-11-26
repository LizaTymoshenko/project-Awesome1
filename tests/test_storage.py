from pathlib import Path

import pytest

import storage
from address_book import AddressBook, Record


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
    storage.save_data(book_with_bob())

    assert data_file.exists()
    loaded = storage.load_data()
    assert str(loaded.find("Bob").phones[0]) == "0501112233"
    assert loaded.find("Bob").email == "bob@mail.com"


def test_missing_file_gives_an_empty_book():
    assert storage.load_data().is_empty()


def test_save_leaves_no_temp_file_behind(data_file):
    storage.save_data(book_with_bob())
    assert list(data_file.parent.iterdir()) == [data_file]


@pytest.mark.parametrize("garbage", [b"this is not a pickle", b"garbage\n", b"", b"\x80\x04\x95"])
def test_corrupted_file_gives_an_empty_book_and_is_kept_aside(data_file, capsys, garbage):
    data_file.parent.mkdir(parents=True)
    data_file.write_bytes(garbage)

    assert storage.load_data().is_empty()

    assert not data_file.exists()
    assert data_file.with_suffix(".corrupt").read_bytes() == garbage
    assert "Could not read saved data" in capsys.readouterr().out


def test_file_without_the_book_is_treated_as_corrupted(data_file):
    import pickle

    data_file.parent.mkdir(parents=True)
    data_file.write_bytes(pickle.dumps({"something": "else"}))

    assert storage.load_data().is_empty()
    assert data_file.with_suffix(".corrupt").exists()
