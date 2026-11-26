import os
import pickle
from pathlib import Path

from address_book import AddressBook

DEFAULT_DATA_FILE = Path.home() / ".personal_assistant" / "assistant.pkl"
DATA_FILE = DEFAULT_DATA_FILE  # tests point this at a temp folder


def save_data(book):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    # write to a temp file first: Ctrl+C in the middle of a dump must not corrupt the saved data
    temp_file = DATA_FILE.with_suffix(".tmp")
    with open(temp_file, "wb") as f:
        pickle.dump({"book": book}, f)
    os.replace(temp_file, DATA_FILE)


def load_data():
    try:
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)["book"]
    except FileNotFoundError:
        return AddressBook()
    except Exception:
        # unpickling garbage can raise almost anything (UnpicklingError, ValueError, EOFError, ...),
        # so catch broadly here only; keep the unreadable file aside so the next save does not destroy it
        corrupt_file = DATA_FILE.with_suffix(".corrupt")
        os.replace(DATA_FILE, corrupt_file)
        print(f"Could not read saved data, starting with an empty book. The old file is kept as {corrupt_file}")
        return AddressBook()
