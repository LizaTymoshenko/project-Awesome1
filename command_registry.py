from dataclasses import dataclass
from collections import UserDict
from typing import Callable
from decorators import input_error

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

    @input_error
    def execute(self, *args, **kwargs):
        """Executes the underlying function with the provided arguments."""
        try:
            return self.handler(*args, **kwargs)
        except CommandFormatError:
            raise ValueError(f"Correct format: {self.format_spec}")

    def __str__(self):
        return f"{self.format_spec}: {self.description}"


class CommandRegistry(UserDict):
    def register(self, command: Command):
        self.data[command.name] = command

    def find(self, command_name):
        command = self.data.get(command_name)
        if command is None:
            raise ValueError(f"Command '{command_name}' not found.")
        return command
    
    def delete(self, name):
        self.find(name)  # raises if the contact does not exist
        self.data.pop(name)

    def show_all(self):
        if not self.data:
            return "Command registry is empty."
        else:
            return "\n".join([str(command) for command in self.data.values()])

