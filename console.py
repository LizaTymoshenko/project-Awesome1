from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table


def render_table(title: str, columns: list[tuple[str, str]], rows: list[list[str]]) -> str:
    """Render a colored table to a string (handlers return str, main.py prints).

    columns: (header, rich style) pairs; rows: one list of cell strings per row.
    """
    table = Table(
        title=title,
        box=box.ROUNDED,
        header_style="bold white on blue",
        border_style="bright_black",
        row_styles=["", "dim"],
    )
    for header, style in columns:
        table.add_column(header, style=style)
    for row in rows:
        # escape: text like "[phone number]" or an address "[home]" must not be read as rich markup
        table.add_row(*(escape(cell) for cell in row))

    return _render(table)


def _render(renderable) -> str:
    console = Console()
    with console.capture() as capture:
        console.print(renderable)
    return capture.get().rstrip("\n")


def render_contacts_table(records) -> str:
    columns = [
        ("Name", "bold cyan"),
        ("Phones", "green"),
        ("Email", "magenta"),
        ("Address", "yellow"),
        ("Birthday", "bright_blue"),
    ]
    rows = [
        [
            str(record.name),
            "\n".join(str(phone) for phone in record.phones) or "-",
            record.email or "-",
            record.address or "-",
            str(record.birthday or "-"),
        ]
        for record in records
    ]
    return render_table("Contacts", columns, rows)

def render_notes_table(notes, title: str = "Notes") -> str:
    columns = [
        ("ID", "bold cyan"),
        ("Text", ""),
        ("Tags", "bold bright_blue"),
    ]
    rows = [
        [
            str(note.note_id),
            note.text,
            ", ".join(sorted(note.tags)) or "-",
        ]
        for note in notes
    ]
    return render_table(title, columns, rows)

def render_welcome() -> str:
    text = "[bold]Personal Assistant[/bold]\nContacts, birthdays and notes in one place.\nType [bold green]help[/bold green] to see all commands, [bold red]exit[/bold red] to quit."
    return _render(Panel(text, box=box.ROUNDED, border_style="blue", expand=False, padding=(1, 4)))


def render_help_table(commands) -> str:
    columns = [("Command", "bold green"), ("Description", "white")]
    rows = [[command.format_spec, command.description] for command in commands]
    return render_table("Available commands", columns, rows)
