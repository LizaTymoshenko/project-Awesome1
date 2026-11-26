from command_registry import Command, CommandRegistry
from contact_handlers import (
    add_contact, change_contact, show_phone, show_all_contacts, add_birthday, 
    show_birthday, show_upcoming_birthdays, delete_contact, search_contacts
)
from note_handlers import (
    add_note, show_notes, search_notes, edit_note, delete_note, 
    add_tag, remove_tag, search_tag, sort_notes
)

from field_handlers import add_address, add_email, edit_contact

registry = CommandRegistry()

## Contacts commands
add_command = Command(
    name='add', 
    format_spec='add [Contact name] [phone number]', 
    description='adds new contact to Address Book or add new phone to existing contact', 
    handler=add_contact,
    type='address book'
    )

change_contact_command = Command(
    name='change', 
    format_spec='change [Contact name] [Old phone] [New phone]', 
    description="changes contact's phone in Address Book", 
    handler=change_contact,
    type='address book'
    )

delete_contact_command = Command(
    name='delete', 
    format_spec='delete [Contact name]', 
    description="deletes contact from the Address Book", 
    handler=delete_contact,
    type='address book'
    )

show_phone_command = Command(
    name='phone', 
    format_spec='phone [Contact name]', 
    description="shows phone of the contact from the Address Book", 
    handler=show_phone,
    type='address book'
    )

show_all_command = Command(
    name='all', 
    format_spec='all', 
    description="shows all contacts from the Address Book", 
    handler=show_all_contacts,
    type='address book'
    )

add_birthday_command = Command(
    name='add-birthday', 
    format_spec='add-birthday [Contact name] DD.MM.YYYY in digits', 
    description="adds birthday to the contact from the Address Book", 
    handler=add_birthday,
    type='address book'
    )

show_birthday_command = Command(
    name='show-birthday', 
    format_spec='show-birthday [Contact name]', 
    description="shows birthday for the contact from the Address Book", 
    handler=show_birthday,
    type='address book'
    )

show_upcoming_birthdays_command = Command(
    name='birthdays',
    format_spec='birthdays | birthdays [N]',
    description="shows upcoming birthdays for N days ahead for the contacts from the Address Book (default N is 7)",
    handler=show_upcoming_birthdays,
    type='address book',
)

add_email_command = Command(
    name='add-email',
    format_spec='add-email [Contact name] [email]',
    description="adds email to the contact from the Address Book",
    handler=add_email,
    type='address book',
)

add_address_command = Command(
    name='add-address',
    format_spec='add-address [Contact name] [address]',
    description="adds address to the contact from the Address Book",
    handler=add_address,
    type='address book',
)

edit_command = Command(
    name='edit',
    format_spec='edit [Contact name] [name|address|email|birthday] [new value]',
    description="edits contact from the Address Book",
    handler=edit_contact,
    type='address book',
)

search_command = Command(
    name='search',
    format_spec='search [name|phone|e-mail]',
    description="searches contacts in the Address Book by name, phone or email",
    handler=search_contacts,
    type='address book',
)


## Notes commands

add_note_command = Command(
    name='add-note',
    format_spec='add-note [text]',
    description="adds note to personal assistant",
    handler=add_note,
    type='notebook',
)

show_note_command = Command(
    name='notes',
    format_spec='notes [text]',
    description="shows all notes from the personal assistant",
    handler=show_notes,
    type='notebook',
)

search_notes_command = Command(
    name='search-note',
    format_spec='search-note [text]',
    description="finds notes with the specified text",
    handler=search_notes,
    type='notebook',
)

edit_note_command = Command(
    name='edit-note',
    format_spec='edit-note [id] [new text]',
    description="edits note specified by id (replaces with new text)",
    handler=edit_note,
    type='notebook',
)

delete_note_command = Command(
    name='delete-note',
    format_spec='delete-note [id]',
    description="deletes note specified by id",
    handler=delete_note,
    type='notebook',
)

add_tag_command = Command(
    name='add-tag',
    format_spec='add-tag [note id] [tag1] [tag2] ...',
    description="adds tag(s) to a note specified by id",
    handler=add_tag,
    type='notebook',
)

remove_tag_command = Command(
    name='remove-tag',
    format_spec='remove-tag [note id] [tag]',
    description="removes tag from a note specified by id",
    handler=remove_tag,
    type='notebook',
)

search_tag_command = Command(
    name='search-tag',
    format_spec='search-tag [tag]',
    description="searches note(s) by a tag",
    handler=search_tag,
    type='notebook',
)

sort_notes_command = Command(
    name='sort-notes',
    format_spec='sort-notes',
    description="prints notes grouped and sorted by tags",
    handler=sort_notes,
    type='notebook',
)


## Register

all_commands = [
    # Contacts 
    add_command, change_contact_command,
    delete_contact_command, show_phone_command,
    show_all_command, add_birthday_command,
    show_birthday_command, show_upcoming_birthdays_command,
    add_email_command, add_address_command, 
    edit_command, search_command,
    # Notes
    add_note_command, show_note_command,
    search_notes_command, edit_note_command,
    delete_note_command, add_tag_command,
    remove_tag_command, search_tag_command,
    sort_notes_command
                ]

for command in all_commands:
    registry.register(command)