from rich import box
from rich.console import Console, Group
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
        header_style="bold #ffffff on #1f6feb",
        border_style="bright_black",
        show_lines=True,  # a line between rows: multi-line cells must not run into the next row
        padding=(0, 2),
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
    # two colors only: the name stands out, everything else is blue
    columns = [
        ("Name", "bold cyan"),
        ("Phones", "bold bright_blue"),
        ("Email", "bold bright_blue"),
        ("Address", "bold bright_blue"),
        ("Birthday", "bold bright_blue"),
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


HELP_GROUPS = {
    "address book": ("Contacts", "cyan"),
    "notebook": ("Notes", "magenta"),
    "base": ("General", "yellow"),
    "help": ("General", "yellow"),
}


def render_help_table(commands) -> str:
    """One panel per group (contacts, notes, general); command name, its arguments and description in columns."""
    grouped = {}
    for command in commands:
        grouped.setdefault(HELP_GROUPS[command.cmd_type], []).append(command)

    panels = []
    for group_key in dict.fromkeys(HELP_GROUPS.values()):  # fixed order: contacts, notes, general
        group = grouped.get(group_key, [])
        if not group:
            continue
        title, color = group_key
        # padding bottom 1: one empty line under every command (Table.grid ignores it)
        grid = Table(box=None, show_header=False, padding=(0, 3, 1, 0), pad_edge=False)
        grid.add_column(style=f"bold {color}", no_wrap=True)
        grid.add_column(style="italic dim", max_width=24, overflow="fold")  # long formats wrap here, not in the description
        grid.add_column(overflow="fold")
        # aliases (exit / close) share one row
        aliases = {}
        for command in group:
            aliases.setdefault(command.description, []).append(command)
        for description, same in aliases.items():
            names = " / ".join(command.name for command in same)
            _, _, arguments = same[0].format_spec.partition(" ")
            grid.add_row(escape(names), escape(arguments), escape(description))
        panels.append(Panel(grid, title=f"[bold {color}]{title}", title_align="left", border_style=color, padding=(1, 2)))
    return _render(Group(*panels))
