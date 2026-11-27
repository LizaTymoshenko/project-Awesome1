from console.console import render_welcome
from console.prompt import create_command_input
from handlers.base_handlers import SessionEnd
from handlers.command_handlers import execute_command
from registry.commands import init_registry
from storage.storage import load_data, save_data


def parse_input(user_input):

    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args


def main():
    book, notebook = load_data()
    registry = init_registry()
    read_command = create_command_input(registry.get_all_specs())
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