from rich.console import Console
from rich.table import Table


def render_contacts_table(records) -> str:
    """Return the contacts as a rich table rendered to a string (handlers return str)."""
    table = Table(show_lines=True)
    for column in ("Name", "Phones", "Email", "Address", "Birthday"):
        table.add_column(column)

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
