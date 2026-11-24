# US-00a — Контракт інтерфейсів (Personal Assistant, group-4)

Усі в команді погоджуються з цим документом **до** паралельної розробки. Структура **плоска**, без пакета: основа — PR з `address_book.py`, `contact_handlers.py`, `storage.py`.

## Сигнатура обробника команди

```python
def handler(args: list[str], book: AddressBook, notebook: NoteBook) -> str: ...
```

- Функція **повертає** рядок для виводу; `print` робить лише цикл у `main.py`.
- `args` — аргументи **без** імені команди (спліт робить `main.py`).
- Навіть якщо обробнику не потрібен `notebook`, параметр лишається: сигнатура єдина.
- Помилки вводу обробляє декоратор `@input_error` з `decorators.py`.

## Реєстр команд

Кожен модуль з обробниками має свій словник `команда → функція`:

```python
# note_handlers.py
NOTE_COMMANDS = {
    "add-note": add_note,
    "notes": show_notes,
}
```

`main.py` один раз зливає словники у `COMMANDS = {**CONTACT_COMMANDS, **NOTE_COMMANDS, ...}`. Нова команда у вже підключеному модулі = **один рядок у словнику цього модуля**, `main.py` не міняється. Новий модуль = один імпорт і один `**` у `main.py`. Декоратор `@command` не використовуємо: зі словником нічого не зникне, якщо модуль забули імпортувати.

Перший аргумент циклу `main.py` береться з `COMMANDS`; невідома команда → підказка (`suggest.py`, US-13) або `help`.

## Моделі

| Клас | Атрибути / API |
|------|----------------|
| `Record` | `name: Name`, `phones: list[Phone]`, `birthday: Birthday \| None`; блок B додає `email`, `address` (`str \| None`) |
| `AddressBook` | `UserDict[str, Record]`; методи `add_record`, `find`, `delete`, `is_empty`, `get_upcoming_birthdays` |
| `Note` | `id: int`, `text: str`, `tags: set[str]` |
| `NoteBook` | `add(text) -> Note`, `find_by_id`, `find_by_text`, `edit`, `delete`, `all` |

Імена класів, полів і методів **не перейменовувати** без узгодження: від них залежать збереження (pickle) і чужі блоки. Нове поле — додавай з значенням за замовчуванням (`None`), щоб не зламати вже збережені дані.

## Файли та власники

| Файл | Блок | Відповідальність |
|------|------|------------------|
| `main.py` | спільне | цикл, `parse_input`, злиття словників, load/save |
| `decorators.py` | спільне | `input_error` |
| `address_book.py` | спільне | `Field`, `Name`, `Phone`, `Birthday`, `Record`, `AddressBook` |
| `contact_handlers.py` | спільне | `add`, `change`, `phone`, `delete`, `all`, `add-birthday`, `show-birthday`, `birthdays` |
| `storage.py` | A (з нотатками) | `Path.home()/.personal_assistant`, зберігає `(book, notebook)` (US-02) |
| `notes.py` | A | `Note`, `NoteBook` |
| `note_handlers.py` | A | `add-note`, `notes`, `search-note`, `edit-note`, `delete-note`, `add-tag`, `search-tag`, `sort-notes` |
| `field_handlers.py` | B | `add-address`, `add-email`, `edit` |
| `validators.py` | B | `validate_email`, `validate_phone` |
| `search_handlers.py` | C | `search`, `remove-phone`, `birthdays [N]` |
| `suggest.py` | D | US-13 `difflib` |

Файли, яких ще немає, створює їхній власник у своєму PR.

## Формат збереження (US-02)

**pickle**: `storage.py` зберігає кортеж `(AddressBook, NoteBook)` цілим об'єктом у `Path.home()/.personal_assistant/assistant.pkl`. Працює з будь-якими полями класів, тому іншим блокам не потрібно писати серіалізацію.

## Середовище

- Python **3.12+** (див. `.python-version`).
- `python -m venv .venv` → `pip install -r requirements.txt` (узгоджений **`rich`** для консолі).
- **Rich** — лише оформлення виводу; логіка команд без зміни сигнатури handler.
- **pytest / ruff** — опційно, `requirements-dev.txt`.
- Нові **runtime**-пакети — узгодження команди + PR у `requirements.txt`.

## Правила

1. Один PR = одна US-картка, свої файли.
2. Конфлікти в `main.py` — мержить власник блоку, який першим пушить; інші роблять rebase.
3. Заглушки команд можна лишати з повідомленням «ще не реалізовано», головне — не ламати імпорти.
