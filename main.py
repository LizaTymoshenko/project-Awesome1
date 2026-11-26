from storage import save_data, load_data
from command_handlers import execute_command, show_all_commands

# for MacOS
try:
    import readline # parses arrow-up / arrow-down on input in console
except ImportError:
    pass


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

            else:
                print(execute_command(command, args, book, notebook))

    except (KeyboardInterrupt, EOFError):
        print("\nGood bye!")
    finally:
        save_data(book, notebook)


if __name__ == "__main__":
    main()