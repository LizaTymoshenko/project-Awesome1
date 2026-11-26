from command_registry import Command, CommandRegistry
from contact_handlers import (
    add_contact, change_contact, show_phone, show_all_contacts, add_birthday, 
    show_birthday, show_upcoming_birthdays, delete_contact, search_contacts
)
from field_handlers import add_address, add_email, edit_contact

registry = CommandRegistry()

add_command = Command('add', 
                      'add [Contact name] [phone number]', 
                      'adds new contact to Address Book or add new phone to existing contact', 
                      add_contact)

change_contact_command = Command('change', 
                                 'change [Contact name] [Old phone] [New phone]', 
                                 "changes contact's phone in Address Book", 
                                 change_contact)

delete_contact_command = Command('delete', 
                                 'delete [Contact name]', 
                                 "deletes contact from the Address Book", 
                                 delete_contact)

show_phone_command = Command('phone', 
                            'phone [Contact name]', 
                            "shows phone of the contact from the Address Book", 
                            show_phone)

show_all_command = Command('all', 
                            'all', 
                            "shows all contacts from the Address Book", 
                            show_all_contacts)


add_birthday_command = Command('add-birthday', 
                            'add-birthday [Contact name] DD.MM.YYYY in digits', 
                            "adds birthday to the contact from the Address Book", 
                            add_birthday)

show_birthday_command = Command('show-birthday', 
                            'show-birthday [Contact name]', 
                            "shows birthday for the contact from the Address Book", 
                            show_birthday)

show_upcoming_birthdays_command = Command('birthdays', 
                                    'birthdays | birthdays [N]', 
                                    "shows upcoming birthdays for N days ahead for the contacts from the Address Book (default N is 7)", 
                                    show_upcoming_birthdays)


add_email_command = Command('add-email', 
                            'add-email [Contact name] [email]', 
                            "adds email to the contact from the Address Book", 
                            add_email)

add_address_command = Command('add-address', 
                            'add-address [Contact name] [address]', 
                            "adds address to the contact from the Address Book", 
                            add_address)

edit_command = Command('edit', 
                            'edit [Contact name] [name|address|email|birthday] [new value]', 
                            "edits contact from the Address Book", 
                            edit_contact)

search_command = Command('search', 
                            'search [name|phone|e-mail]', 
                            "searches contacts in the Address Book by name, phone or email", 
                            search_contacts)


registry.register(add_command)
registry.register(change_contact_command)
registry.register(delete_contact_command)
registry.register(show_phone_command)
registry.register(show_all_command)
registry.register(add_birthday_command)
registry.register(show_birthday_command)
registry.register(show_upcoming_birthdays_command)
registry.register(add_email_command)
registry.register(add_address_command)
registry.register(edit_command)
registry.register(search_command)

