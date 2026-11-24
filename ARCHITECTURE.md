# Архітектура проєкту

**Це не готовий код** — лише угода команди. Кожен блок **сам** створює свої файли та реалізацію за цим планом.

## Структура репо (цільова)

```
project-Awesome1/
├── main.py                 # D: точка входу, імпорт модулів команд, load/save
├── personal_assistant/
│   ├── cli.py              # D: цикл, parse, @command, help, exit
│   ├── decorators.py       # D: input_error
│   ├── storage.py          # D: Path.home()/.personal_assistant (US-02)
│   ├── suggest.py          # D: US-13 difflib
│   ├── models.py           # спільне: Record, AddressBook
│   ├── contacts_core.py    # спільне: add, change, phone, delete
│   ├── notes.py            # A: Note, NoteBook
│   ├── notes_commands.py   # A: add-note, notes, search-note, …
│   ├── contacts_fields.py  # B: add-address, add-email, edit, all
│   ├── validators.py       # B: validate_email, validate_phone
│   └── search.py           # C: search, remove-phone, birthdays
├── CONTRACT.md
├── ARCHITECTURE.md
└── README.md
```

## Потік даних

```text
main → load_data() → (AddressBook, NoteBook)
     → run_cli(book, notebook)
         → parse рядка
         → handler(args, book, notebook) → str
         → print
     → save_data() на exit / Ctrl+C
```

## Порядок роботи

1. **День 0 (D):** перший PR — `main.py` + `cli.py` (цикл, `@command`, `help`, `exit`) без бізнес-логіки, плюс порожні `models.py` / `notes.py` з класами за `CONTRACT.md`, щоб решта не блокувалась.
2. **Паралельно:** A/B/C створюють **тільки свої** файли за таблицею в `CONTRACT.md` + один рядок імпорту в `main.py` (мержить D).
3. Кожна US-картка = своя гілка (`feature/us-03-address`) і свій PR.
4. US-02: один PR від D, імена класів з `CONTRACT.md` не змінювати.
5. Якщо через день після US-00a немає PR з `cli.py` — D пушить лише `cli.py` + `main.py`.

## Гілки

- `main` — стабільна інтеграція
- `feature/us-NN-назва` — одна картка Trello = одна гілка
