# US-00a — Контракт інтерфейсів (Personal Assistant, group-4)

Усі в команді погоджуються з цим документом **до** паралельної розробки.

## Сигнатура обробника команди

```python
Handler = Callable[[list[str], AddressBook, NoteBook], str]
```

- Функція **повертає** рядок для виводу; `print` робить лише CLI-цикл.
- Перший аргумент — аргументи команди **без** імені команди (спліт уже зроблений у циклі).

## Реєстрація команд

```python
from personal_assistant.cli import command

@command("add-note")
def cmd_add_note(args: list[str], book: AddressBook, notebook: NoteBook) -> str:
    ...
```

Нові команди додаються через декоратор. **Не змінюйте** парсинг і головний цикл без узгодження (власник блоку D).

## Моделі (атрибути)

| Клас | Атрибути / API |
|------|----------------|
| `Record` | `name: str`, `phones: list[str]`, `email: str \| None`, `address: str \| None`, `birthday: date \| None` |
| `AddressBook` | `dict[str, Record]`; методи: `add`, `delete`, `find`, `get_all`, `get_upcoming_birthdays` |
| `Note` | `id: int`, `text: str`, `tags: set[str]` |
| `NoteBook` | `add(text) -> Note`, `find_by_id`, `find_by_text`, `edit`, `delete`, `all` |

Імена класів і полів **не перейменовувати** без узгодження (інакше зламається US-02).

## Формат збереження (US-02)

**pickle**: `storage.py` зберігає кортеж `(AddressBook, NoteBook)` цілим об'єктом у `Path.home()/.personal_assistant/assistant.pkl`. Працює з будь-якими полями класів, тому блокам A/B/C не потрібно писати серіалізацію.

## Файли та власники

| Файл | Блок | Відповідальність |
|------|------|------------------|
| `personal_assistant/cli.py` | D | цикл, `help`, `exit`, реєстр, `input_error` |
| `personal_assistant/storage.py` | D | load/save у `Path.home()/.personal_assistant` |
| `personal_assistant/decorators.py` | D | `input_error` |
| `personal_assistant/models.py` | спільне | `Record`, `AddressBook` |
| `personal_assistant/contacts_core.py` | спільне | `add`, `change`, `phone`, `delete` (не чіпати без узгодження) |
| `personal_assistant/notes.py` | A | `Note`, `NoteBook`, теги |
| `personal_assistant/notes_commands.py` | A | `add-note`, `notes`, `search-note`, `edit-note`, `delete-note`, `add-tag` |
| `personal_assistant/contacts_fields.py` | B | `add-address`, `add-email`, `edit`, `all` |
| `personal_assistant/validators.py` | B | `validate_email`, `validate_phone` |
| `personal_assistant/search.py` | C | `search`, `birthdays`, `remove-phone` |
| `personal_assistant/suggest.py` | D | US-13 `difflib` (коли всі команди є) |

## Середовище

- Python **3.12+** (узгодити на US-00a; див. `.python-version`).
- `python -m venv .venv` → `pip install -r requirements.txt` (узгоджений **`rich`** для консолі).
- **Rich** — лише оформлення виводу; логіка команд без зміни сигнатури handler.
- **pytest / ruff** — опційно, `requirements-dev.txt`.
- Нові **runtime**-пакети — узгодження команди + PR у `requirements.txt`.

## Правила

1. Один PR = одна US-картка, свій файл.
2. Конфлікти в `cli.py` / `main.py` — мержить блок D.
3. Заглушки команд можна лишати з повідомленням «ще не реалізовано», головне — не ламати імпорти.