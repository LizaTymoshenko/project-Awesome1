# Архітектура проєкту

**Це не готовий код** — лише угода команди. Структура **плоска**, основа — PR з `address_book.py`, `contact_handlers.py`, `storage.py`. Кожен блок створює і розширює **свої** файли за цим планом.

## Структура репо (цільова)

```
project-Awesome1/
├── main.py                 # цикл, parse_input, злиття словників команд, load/save
├── decorators.py           # input_error
├── address_book.py         # Field, Name, Phone, Birthday, Record, AddressBook
├── contact_handlers.py     # add, change, phone, delete, all, add-birthday, show-birthday, birthdays
├── storage.py              # A: Path.home()/.personal_assistant (US-02)
├── notes.py                # A: Note, NoteBook
├── note_handlers.py        # A: add-note, notes, search-note, …
├── field_handlers.py       # B: add-address, add-email, edit
├── validators.py           # B: validate_email, validate_phone
├── search_handlers.py      # C: search, remove-phone, birthdays [N]
├── suggest.py              # D: US-13 difflib
├── CONTRACT.md
├── ARCHITECTURE.md
└── README.md
```

## Потік даних

```text
main → load_data() → (AddressBook, NoteBook)
     → цикл: parse_input → COMMANDS[команда](args, book, notebook) → str → print
     → save_data() на exit / Ctrl+C
```

`COMMANDS` збирається в `main.py` зі словників модулів: `{**CONTACT_COMMANDS, **NOTE_COMMANDS, ...}`.

## Порядок роботи

1. **Основа (PR #2):** `address_book.py`, `contact_handlers.py`, `storage.py`, `main.py` + реєстр словниками і єдина сигнатура `handler(args, book, notebook)`. Після мержа решта стартує.
2. **Паралельно:** кожен блок створює **тільки свої** файли за таблицею в `CONTRACT.md` + один імпорт і один `**` у `main.py`.
3. Кожна US-картка = своя гілка (`feature/us-03-address`) і свій PR.
4. US-02 робить власник блоку A разом з нотатками; імена класів з `CONTRACT.md` не змінювати.

## Гілки

- `main` — стабільна інтеграція (захищена)
- `feature/назва` / `bugfix/назва` — одна картка Trello = одна гілка
