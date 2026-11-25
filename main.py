
from storage import save_data, load_data
from contact_handlers import add_contact, change_contact, show_phone, show_all_contacts, add_birthday, show_birthday, show_upcoming_birthdays, delete_contact, search_contacts

# for MacOS
try:
    import readline # parses arrow-up / arrow-down on input in console
except ImportError:
    pass
from note_handlers import add_note, show_notes, search_notes, edit_note, delete_note
from note_handlers import add_note, show_notes, search_notes, edit_note, delete_note, add_tag, remove_tag, search_tag, sort_notes

from commands import registry

def parse_input(user_input):

    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args




def main():
    book, notebook = load_data()
    print("Welcome to the assistant bot!")
    try:

        while True:
            user_input = input("Enter a command: ")
            if not user_input.strip():
                continue
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, book))

            elif command == "change":
                print(change_contact(args, book))

            elif command == "phone":
                print(show_phone(args, book))

            elif command == "all":
                print(show_all_contacts(args, book))

            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))

            elif command == "birthdays":
                print(show_upcoming_birthdays(args, book))

            elif command == "add-address":
                print(add_address(args, book))

            elif command == "add-email":
                print(add_email(args, book))

            elif command == "edit":
                print(edit_contact(args, book))

            elif command == "delete":
                print(delete_contact(args,book))

            elif command == "search":
                print(search_contacts(args, book))

            # notes
            elif command == "add-note":
                print(add_note(args,notebook))
            elif command == "notes":
                print(show_notes(args, notebook))
            elif command == "search-note":
                print(search_notes(args, notebook))
            elif command == "edit-note":
                print(edit_note(args,notebook))
            elif command == "delete-note":
                print(delete_note(args,notebook))
            elif command == "add-tag":
                print(add_tag(args,notebook))
            elif command == "remove-tag":
                print(remove_tag(args,notebook))
            elif command == "search-tag":
                print(search_tag(args,notebook))
            elif command == "sort-notes":
                print(sort_notes(args,notebook))
            else:
                print("Invalid command.")
    except (KeyboardInterrupt, EOFError):
        print("\nGood bye!")
    finally:
        save_data(book, notebook)


if __name__ == "__main__":
    main()