from address_book.address_book import AddressBook
from console.console import render_help_table
from helpers.decorators import input_error
from notebook.notes import NoteBook
from registry.command_registry import CommandRegistry


@input_error
def execute_command(command: str, args: list|tuple, book: AddressBook, notebook: NoteBook, registry: CommandRegistry) -> str:
    cmd = registry.find(command)
    if cmd is None:
        close_commands = show_close_matches(command, args, registry)
        if close_commands:
            return successful_match_response(close_commands, registry)
        return unsuccessful_match_response()

    result = cmd.execute(args, book, notebook, registry)
    if result.success:
        return result.message

    close_commands = show_close_matches(command, args, registry)
    if close_commands and command not in close_commands:
        suggestion = successful_match_response(close_commands, registry)
        return f"{result.message}\n{suggestion}"

    return result.message


# finds close commands
def show_close_matches(in_command: str, args: list|tuple, registry: CommandRegistry) -> list:
    # first search - with 2 console arguments, it will cover composite commands like add-email etc.
    if len(args) > 0:
        sample_command = in_command + args[0]
        close_commands = registry.get_close_commands(sample_command)
        if not close_commands:
            close_commands = registry.get_close_commands(in_command)
    else:
        close_commands = registry.get_close_commands(in_command)

    return close_commands


def show_all_commands(registry: CommandRegistry):
    return render_help_table(registry.values())


# possible responses
def help_response() -> str:
    return "Please type 'help' to see all available commands."

def successful_match_response(close_commands: list, registry: CommandRegistry) -> str:
    return 'Possibly you wanted to enter this command:\n' + registry.show_selected(close_commands)

def unsuccessful_match_response() -> str:
    return f"Invalid command. {help_response()}"
