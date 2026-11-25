
from field_handlers import add_address, add_email, edit_contact
from storage import save_data, load_data
from contact_handlers import add_contact, change_contact, show_phone, show_all_contacts, add_birthday, show_birthday, show_upcoming_birthdays, delete_contact
import readline # parses arrow-up / arrow-down on input in console

def parse_input(user_input):

    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args




def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    try:

        while True:
            user_input = input("Enter a command: ")
            if not user_input.strip():
                continue
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book)
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

            else:
                print("Invalid command.")
    finally:
        save_data(book)


if __name__ == "__main__":
    main()