from handlers.base_handlers import close_bot, hello
from handlers.command_handlers import show_all_commands
from handlers.contact_handlers import (
    add_birthday,
    add_contact,
    change_contact,
    delete_contact,
    remove_phone,
    search_contacts,
    show_all_contacts,
    show_birthday,
    show_phone,
    show_upcoming_birthdays,
)
from handlers.field_handlers import add_address, add_email, edit_contact
from handlers.note_handlers import (
    add_note,
    add_tag,
    delete_note,
    edit_note,
    remove_tag,
    search_notes,
    search_tag,
    show_notes,
    sort_notes,
)
from registry.command_registry import Command, CommandRegistry


def init_registry():
    # Init
    registry = CommandRegistry()

    # Base commands
    close_command = Command(
        name='close',
        format_spec='close',
        description='closes bot',
        handler=close_bot,
        cmd_type='base'
    )

    exit_command = Command(
        name='exit',
        format_spec='exit',
        description='closes bot',
        handler=close_bot,
        cmd_type='base'
    )

    hello_command = Command(
        name='hello',
        format_spec='hello',
        description='says hello',
        handler=hello,
        cmd_type='base'
    )


    help_command = Command(
        name='help',
        format_spec='help',
        description='shows all available commands',
        handler=show_all_commands,
        cmd_type='help'
    )

    ## Contacts commands
    add_command = Command(
        name='add', 
        format_spec='add [Contact name] [phone number]', 
        description='adds new contact to Address Book or add new phone to existing contact', 
        handler=add_contact,
        cmd_type='address book'
        )

    change_contact_command = Command(
        name='change', 
        format_spec='change [Contact name] [Old phone] [New phone]', 
        description="changes contact's phone in Address Book", 
        handler=change_contact,
        cmd_type='address book'
        )

    delete_contact_command = Command(
        name='delete', 
        format_spec='delete [Contact name]', 
        description="deletes contact from the Address Book", 
        handler=delete_contact,
        cmd_type='address book'
        )

    show_phone_command = Command(
        name='phone', 
        format_spec='phone [Contact name]', 
        description="shows phone of the contact from the Address Book", 
        handler=show_phone,
        cmd_type='address book'
        )

    show_all_command = Command(
        name='all', 
        format_spec='all', 
        description="shows all contacts from the Address Book", 
        handler=show_all_contacts,
        cmd_type='address book'
        )

    add_birthday_command = Command(
        name='add-birthday', 
        format_spec='add-birthday [Contact name] DD.MM.YYYY in digits', 
        description="adds birthday to the contact from the Address Book", 
        handler=add_birthday,
        cmd_type='address book'
        )

    show_birthday_command = Command(
        name='show-birthday', 
        format_spec='show-birthday [Contact name]', 
        description="shows birthday for the contact from the Address Book", 
        handler=show_birthday,
        cmd_type='address book'
        )

    show_upcoming_birthdays_command = Command(
        name='birthdays',
        format_spec='birthdays [N]',
        description="shows upcoming birthdays for N days ahead for the contacts from the Address Book (default N is 7)",
        handler=show_upcoming_birthdays,
        cmd_type='address book',
    )

    add_email_command = Command(
        name='add-email',
        format_spec='add-email [Contact name] [email]',
        description="adds email to the contact from the Address Book",
        handler=add_email,
        cmd_type='address book',
    )

    add_address_command = Command(
        name='add-address',
        format_spec='add-address [Contact name] [address]',
        description="adds address to the contact from the Address Book",
        handler=add_address,
        cmd_type='address book',
    )

    edit_command = Command(
        name='edit',
        format_spec='edit [Contact name] [name|address|email|birthday] [new value]',
        description="edits contact from the Address Book",
        handler=edit_contact,
        cmd_type='address book',
    )

    remove_phone_command = Command(
            name='remove-phone',
            format_spec='remove-phone [Contact name] [phone number]',
            description="removes specified phone number of the contact from the Address Book",
            handler=remove_phone,
            cmd_type='address book',
        )

    search_command = Command(
        name='search',
        format_spec='search [name|phone|e-mail]',
        description="searches contacts in the Address Book by name, phone or email",
        handler=search_contacts,
        cmd_type='address book',
    )


    ## Notes commands

    add_note_command = Command(
        name='add-note',
        format_spec='add-note [text]',
        description="adds note to personal assistant",
        handler=add_note,
        cmd_type='notebook',
    )

    show_note_command = Command(
        name='notes',
        format_spec='notes',
        description="shows all notes from the personal assistant",
        handler=show_notes,
        cmd_type='notebook',
    )

    search_notes_command = Command(
        name='search-note',
        format_spec='search-note [text]',
        description="finds notes with the specified text",
        handler=search_notes,
        cmd_type='notebook',
    )

    edit_note_command = Command(
        name='edit-note',
        format_spec='edit-note [id] [new text]',
        description="edits note specified by id (replaces with new text)",
        handler=edit_note,
        cmd_type='notebook',
    )

    delete_note_command = Command(
        name='delete-note',
        format_spec='delete-note [id]',
        description="deletes note specified by id",
        handler=delete_note,
        cmd_type='notebook',
    )

    add_tag_command = Command(
        name='add-tag',
        format_spec='add-tag [note id] [tag1] [tag2] ...',
        description="adds tag(s) to a note specified by id",
        handler=add_tag,
        cmd_type='notebook',
    )

    remove_tag_command = Command(
        name='remove-tag',
        format_spec='remove-tag [note id] [tag]',
        description="removes tag from a note specified by id",
        handler=remove_tag,
        cmd_type='notebook',
    )

    search_tag_command = Command(
        name='search-tag',
        format_spec='search-tag [tag]',
        description="searches note(s) by a tag",
        handler=search_tag,
        cmd_type='notebook',
    )

    sort_notes_command = Command(
        name='sort-notes',
        format_spec='sort-notes',
        description="prints notes grouped and sorted by tags",
        handler=sort_notes,
        cmd_type='notebook',
    )


    ## Register

    all_commands = [
        # Contacts 
        add_command, change_contact_command,
        delete_contact_command, show_phone_command,
        show_all_command, add_birthday_command,
        show_birthday_command, show_upcoming_birthdays_command,
        add_email_command, add_address_command, 
        edit_command, remove_phone_command, search_command,
        # Notes
        add_note_command, show_note_command,
        search_notes_command, edit_note_command,
        delete_note_command, add_tag_command,
        remove_tag_command, search_tag_command,
        sort_notes_command,
        # base
        close_command, exit_command, hello_command, help_command
                    ]

    for command in all_commands:
        registry.register(command)

    return registry
