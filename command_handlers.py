from command_registry import CommandRegistry
from notes import NoteBook
from address_book import AddressBook
from console import render_help_table


# execute command from the CommandRegistry + find close matches if command if not correct
def execute_command(command: str, args: list|tuple, book: AddressBook, notebook: NoteBook, registry: CommandRegistry):
    cmd = registry.find(command)
    if cmd:
        rez = cmd.execute(args, book, notebook, registry)
        close_commands = show_close_matches(command, args, registry)
        if command not in close_commands:
            match_rez = successful_match_response(close_commands, registry)
            return f"{rez}\n{match_rez}"
        else:
            return rez
    else:
        close_commands = show_close_matches(command, args, registry) # args for composite command mistypes like add email instead of add-email
        if close_commands:
            return successful_match_response(close_commands, registry)
        else:
            return unsuccessful_match_response()


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
