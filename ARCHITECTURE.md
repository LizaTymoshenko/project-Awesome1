# Архітектура

Консольний помічник: книга контактів і нотатки, дані зберігаються на диску між запусками.

## Структура

```
project-Awesome1/
├── main.py                 # цикл команд, parse_input, злиття словників команд, load/save
├── decorators.py           # input_error: помилки вводу → повідомлення користувачу
├── address_book.py         # Field, Name, Phone, Birthday, Record, AddressBook
├── contact_handlers.py     # add, change, phone, delete, all, add-birthday, show-birthday, birthdays
├── field_handlers.py       # add-address, add-email, edit
├── search_handlers.py      # search, remove-phone, birthdays [N]
├── validators.py           # validate_email
├── notes.py                # Note, NoteBook
├── note_handlers.py        # add-note, notes, search-note, edit-note, delete-note, add-tag, search-tag, sort-notes
├── console.py              # render_table: кольорові таблиці (rich)
├── storage.py              # збереження і завантаження даних
├── suggest.py              # підказка найближчої команди (difflib)
└── requirements.txt        # rich
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

Таблиці будує `console.render_table(title, columns, rows)`: вона повертає рядок, тому обробники команд лишаються чистими функціями. Колонки й кольори задає кожен обробник.

## Залежності

Python 3.12+, `rich` (див. `requirements.txt`).
