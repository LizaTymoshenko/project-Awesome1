from dataclasses import dataclass
from collections import UserDict
from typing import Callable, Literal
from difflib import get_close_matches

from decorators import input_error
from address_book import AddressBook
from notes import NoteBook


# custom exception
class CommandFormatError(ValueError):
    """Base exception for incorect command format errors."""
    pass


@dataclass(frozen=True)
class Command:
    name: str
    format_spec: str
    description: str
    handler: Callable[...]
    type: Literal['address book', 'notebook']

    @input_error
    def execute(self, args, book: AddressBook, notebook: NoteBook):
        """Executes the underlying function with the provided arguments."""
        try:
            if self.type == 'address book':
                return self.handler(args, book)
            else:
                return self.handler(args, notebook)
        except CommandFormatError:
            raise ValueError(f"Correct format: {self.format_spec}")

    def __str__(self):
        return f"{self.format_spec}: {self.description}"


class CommandRegistry(UserDict):
    def register(self, command: Command):
        self.data[command.name] = command

    def find(self, command_name):
        return self.data.get(command_name)

    def show_all(self):
        if not self.data:
            return "Command registry is empty."
        else:
            return "\n".join([str(command) for command in self.data.values()])

    def show_selected(self, selected: list) -> str:
        return '\n'.join([str(self.find(command)) for command in selected])
        
    def get_all_command_names(self):
        return list(self.data.keys())

    def get_close_commands(self, sample_command: str) -> list:
        return get_close_matches(sample_command, self.get_all_command_names(), n=1)

