from rich import box
from rich.console import Console
from rich.table import Table


def render_contacts_table(records) -> str:
    """Return the contacts as a rich table rendered to a string (handlers return str)."""
    table = Table(
        title="Contacts",
        box=box.ROUNDED,
        header_style="bold white on blue",
        border_style="bright_black",
        row_styles=["", "dim"],
    )
    table.add_column("Name", style="bold cyan")
    table.add_column("Phones", style="green")
    table.add_column("Email", style="magenta")
    table.add_column("Address", style="yellow")
    table.add_column("Birthday", style="bright_blue")

    for record in records:
        table.add_row(
            str(record.name),
            "\n".join(str(phone) for phone in record.phones) or "-",
            record.email or "-",
            record.address or "-",
            str(record.birthday or "-"),
        )

    console = Console()
    with console.capture() as capture:
        console.print(table)
    return capture.get().rstrip("\n")
