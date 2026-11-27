from __future__ import annotations

from collections import UserDict
from collections.abc import Callable
from dataclasses import dataclass
from difflib import get_close_matches
from typing import Literal

from address_book.address_book import AddressBook
from helpers.decorators import COMMAND_ERROR_MESSAGE
from notebook.notes import NoteBook


# custom exception
class CommandFormatError(ValueError):
    """Base exception for incorect command format errors."""
    pass


@dataclass(frozen=True)
class CommandResult:
    success: bool
    message: str


@dataclass(frozen=True)
class Command:
    name: str
    format_spec: str
    description: str
    handler: Callable[..., str]
    cmd_type: Literal['address book', 'notebook', 'base', 'help']

    def execute(self, args, book: AddressBook, notebook: NoteBook, registry: CommandRegistry) -> CommandResult:
        """Executes the underlying function with the provided arguments."""
        message = None
        try:
            if self.cmd_type == 'address book':
                message = self.handler(args, book)
            elif self.cmd_type == 'notebook':
                message = self.handler(args, notebook)
            elif self.cmd_type == 'help':
                message = self.handler(registry)
            elif self.cmd_type == 'base':
                message = self.handler()
        except CommandFormatError:
            return CommandResult(success=False, message=f"Correct format: {self.format_spec}")
        except (ValueError, KeyError) as error:
            return CommandResult(success=False, message=str(error))
        except Exception:
            return CommandResult(success=False, message=COMMAND_ERROR_MESSAGE)

        return CommandResult(success=True, message=message)

    def __str__(self):
        return f"{self.format_spec}: {self.description}"


class CommandRegistry(UserDict):
    def register(self, command: Command) -> None:
        self.data[command.name] = command

    def find(self, command_name) -> Command:
        return self.data.get(command_name)

    def show_selected(self, selected: list) -> str:
        return '\n'.join([str(self.find(command)) for command in selected])
        
    def get_all_command_names(self) -> list:
        return list(self.data.keys())

    def get_close_commands(self, sample_command: str) -> list:
        return get_close_matches(sample_command, self.get_all_command_names(), n=1)

    def get_command_names_by_type(self, cmd_type) -> list:
        return [cmd_name for cmd_name, cmd in self.data.items() if cmd.cmd_type == cmd_type]

    def get_all_specs(self) -> dict:
        return {command.name: command.format_spec for command in self.values()}

