
from storage import save_data, load_data
from contact_handlers import add_contact, change_contact, show_phone, show_all_contacts, add_birthday, show_birthday, show_upcoming_birthdays, delete_contact, search_contacts

# for MacOS
try:
    import readline # parses arrow-up / arrow-down on input in console
except ImportError:
    pass
from note_handlers import add_note, show_notes, search_notes, edit_note, delete_note
from note_handlers import add_note, show_notes, search_notes, edit_note, delete_note, add_tag, remove_tag, search_tag, sort_notes

from command_handlers import execute_command, show_all_commands

# temp
import readline

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

            elif command == "help":
                print(show_all_commands())

            elif command == "search":
                print(search_contacts(args, book))

            else:
                print("Invalid command.")
    except (KeyboardInterrupt, EOFError):
        print("\nGood bye!")
    finally:
        save_data(book, notebook)


if __name__ == "__main__":
    main()