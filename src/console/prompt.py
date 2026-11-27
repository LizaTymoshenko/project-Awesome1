from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter


def format_hint(text: str, hints: dict[str, str]) -> str:
    """Format of the command being typed, shown under the input line."""
    words = text.split()
    return hints.get(words[0].lower(), "") if words else ""


def create_command_input(hints: dict[str, str]):
    """Return input() replacement: Tab completes command names, arrow keys browse history.

    hints: command name -> its format, e.g. {"add": "add [Contact name] [phone number]"}.
    """
    session = PromptSession(
        completer=NestedCompleter.from_nested_dict({name: None for name in hints}),
        complete_while_typing=True,
        bottom_toolbar=lambda: format_hint(session.default_buffer.text, hints),
    )
    return session.prompt
