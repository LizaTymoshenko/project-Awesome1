# Архітектура

Консольний помічник: книга контактів і нотатки, дані зберігаються на диску між запусками.

## Структура

```
project-Awesome1/
├── main.py              # цикл команд: parse_input → execute_command → print
├── commands.py          # init_registry(): реєстр усіх команд (імʼя, формат, опис, обробник)
├── command_registry.py  # Command, CommandRegistry, CommandFormatError
├── command_handlers.py  # execute_command, підказка найближчої команди (difflib), help
├── base_handlers.py     # hello, exit / close (SessionEnd)
├── contact_handlers.py  # add, change, phone, delete, all, add-birthday, show-birthday, birthdays, search
├── field_handlers.py    # add-address, add-email, edit
├── note_handlers.py     # add-note, notes, search-note, edit-note, delete-note, add-tag, remove-tag, search-tag, sort-notes
├── address_book.py      # Field, Name, Phone, Birthday, Record, AddressBook
├── notes.py             # Note, NoteBook
├── validators.py        # validate_email
├── decorators.py        # input_error
├── console.py           # екрани і таблиці (rich): вітання, help, контакти, нотатки
├── storage.py           # збереження і завантаження даних
├── tests/               # pytest
└── requirements.txt     # rich
```

## Потік даних

```text
main → load_data() → (AddressBook, NoteBook)
     → цикл: parse_input → COMMANDS[команда](args, book, notebook) → str → print
     → save_data() на exit / Ctrl+C
```

## Команди

Кожен модуль з обробниками має словник `команда → функція`; `main.py` зливає їх у `COMMANDS`. Обробник має єдину сигнатуру `handler(args, book, notebook) -> str`: він повертає рядок, а виводить його лише цикл у `main.py`. Помилки вводу (`ValueError`, `KeyError`) обробляє декоратор `@input_error`.

## Дані

- `AddressBook` — словник `імʼя → Record`; `Record` містить `name`, `phones`, `birthday`, `email`, `address`.
- `NoteBook` — нотатки з унікальним `id`, текстом і тегами; не залежить від `AddressBook`.
- Збереження: `pickle` кортежу `(AddressBook, NoteBook)` у `Path.home()/.personal_assistant/assistant.pkl`; папка створюється автоматично, за відсутності файлу створюються порожні книги.

## Вивід

<<<<<<< HEAD
Таблиці будує `console.render_table(title, columns, rows)`: вона повертає рядок, тому обробники команд лишаються чистими функціями. Колонки й кольори задає кожен обробник.
=======
Увесь вивід будує `console.py`, кожна функція повертає рядок, тому обробники команд лишаються чистими функціями, а друкує їх результат лише цикл у `main.py`.

- `render_table(title, columns, rows)` — спільна кольорова таблиця з лініями між рядками; текст у комірках і заголовку екранується, щоб `[...]` не сприймалось як розмітка rich.
- `render_contacts_table(records)` — таблиця контактів (`all`, `search`).
- `render_notes_table(notes, title)` — таблиця нотаток: ID, текст, теги (`notes`, `search-note`, `search-tag`, `sort-notes`, у `sort-notes` окрема таблиця для кожного тегу).
- `render_welcome()` — панель-вітання при старті.
- `render_help_table(commands)` — `help`: панелі за групами (контакти, нотатки, загальні), команди з однаковим описом (`close` / `exit`) в одному рядку. Дані беруться з реєстру, тому нова команда зʼявляється в `help` сама.

Приклади виводу: [welcome-help](docs/screenshots/welcome-help.png), [contacts](docs/screenshots/contacts.png), [notes](docs/screenshots/notes.png).
>>>>>>> c266a37 (docs: ARCHITECTURE describes help, welcome and notes table from console.py)

## Залежності

Python 3.12+, `rich` (див. `requirements.txt`).
