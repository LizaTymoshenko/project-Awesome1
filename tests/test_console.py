from command_registry import Command
from console import render_help_table, render_welcome


def test_welcome_points_to_help_and_exit():
    text = render_welcome()
    assert "Personal Assistant" in text
    assert "help" in text and "exit" in text


def test_help_table_shows_name_arguments_and_description_of_every_command():
    commands = [
        Command("add", "add [Contact name] [phone number]", "adds new contact", print, "address book"),
        Command("all", "all", "shows all contacts", print, "address book"),
    ]

    text = render_help_table(commands)

    assert "add" in text
    assert "[Contact name]" in text  # long arguments wrap, so check the first part only
    assert "adds new contact" in text
    assert "shows all contacts" in text


def test_help_table_groups_commands_by_kind():
    commands = [
        Command("add-note", "add-note [text]", "adds note", print, "notebook"),
        Command("add", "add [Contact name]", "adds contact", print, "address book"),
        Command("exit", "exit", "closes bot", print, "base"),
    ]

    text = render_help_table(commands)

    assert text.index("Contacts") < text.index("Notes") < text.index("General")


def test_help_command_shows_the_registered_commands():
    from command_handlers import show_all_commands
    from commands import init_registry

    registry = init_registry()
    text = show_all_commands(registry)

    for command in registry.values():
        assert command.name in text  # the long format column may wrap, the name starts the line


def test_square_brackets_in_text_are_shown_not_treated_as_markup():
    from console import render_table

    text = render_table("T", [("Col", "")], [["add [phone number]"]])

    assert "add [phone number]" in text
