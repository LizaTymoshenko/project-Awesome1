# Персональний помічник

Консольний бот: книга контактів і нотатки. Дані зберігаються на диску, тож бота можна перезапускати без втрати даних. Структура модулів і потік даних описані в [ARCHITECTURE.md](./ARCHITECTURE.md).

## Встановлення і запуск

Потрібен Python 3.12+.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python3 main.py
```

`requirements.txt` ставить `rich` (кольорові таблиці). Для тестів і лінтера: `pip install -r requirements-dev.txt`, запуск `python -m pytest`.

## Команди

| Команда | Що робить |
|---------|-----------|
| `add [імʼя] [телефон]` | створює контакт або додає телефон |
| `change [імʼя] [старий] [новий]` | змінює телефон |
| `phone [імʼя]` | показує телефони контакту |
| `delete [імʼя]` | видаляє контакт |
| `all` | показує всі контакти таблицею |
| `add-address [імʼя] [адреса]` | додає адресу |
| `add-email [імʼя] [email]` | додає email (формат перевіряється) |
| `edit [імʼя] [name\|address\|email\|birthday] [значення]` | змінює поле контакту |
| `add-birthday [імʼя] DD.MM.YYYY` | додає день народження |
| `show-birthday [імʼя]` | показує день народження |
| `birthdays` | дні народження найближчого тижня |
| `hello`, `exit` / `close` | привітання, вихід із збереженням |

## Як додати команду

Обробник має єдину сигнатуру і **повертає рядок**: друкує його лише цикл у `main.py`.

```python
@input_error
def my_command(args: list[str], book: AddressBook) -> str:
    ...
    return "Готово"
```

- `args` — аргументи без імені команди.
- `@input_error` (`decorators.py`) перетворює `ValueError` і `KeyError` на повідомлення користувачу.
- Команда підключається в `main.py`. Для таблиць використовуйте `console.render_table(title, columns, rows)`: вона повертає рядок.

## Дані

Контакти зберігаються через `pickle` (`storage.py`). Поля контакту: `name`, `phones`, `email`, `address`, `birthday`. Нові поля додавайте зі значенням за замовчуванням `None`, щоб раніше збережені дані продовжували завантажуватись.
