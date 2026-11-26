from storage import save_data, load_data
from command_handlers import execute_command
from base_handlers import SessionEnd
from console import render_welcome

from commands import init_registry
from prompt import create_command_input

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
    registry = init_registry()
    read_command = create_command_input({command.name: command.format_spec for command in registry.values()})
    print(render_welcome())
    try:

        while True:
            user_input = read_command("Enter a command: ")
            if not user_input.strip():
                continue
            command, *args = parse_input(user_input)

            print(execute_command(command, args, book, notebook, registry))

    except (KeyboardInterrupt, EOFError, SessionEnd):
        print("\nGood bye!")
    finally:
        save_data(book, notebook)


if __name__ == "__main__":
    main()