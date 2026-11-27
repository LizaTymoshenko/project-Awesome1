# Архітектура

Консольний помічник: книга контактів і нотатки, дані зберігаються на диску між запусками.

## Структура

```text
project-Awesome1/
├── src/
│   ├── main.py       # запуск і цикл команд
│   ├── address_book/ # поля контакту, Record і AddressBook
│   ├── notebook/     # Note і NoteBook
│   ├── handlers/     # обробники команд і пошук схожих назв
│   ├── registry/     # Command, CommandRegistry та init_registry()
│   ├── console/      # таблиці, вітання, довідка й інтерактивний ввід
│   ├── helpers/      # перевірка email і декоратор input_error
│   └── storage/      # збереження й завантаження даних
├── tests/            # pytest
├── pyproject.toml    # залежності й налаштування pytest та Ruff
└── uv.lock           # зафіксовані версії залежностей
```

## Потік даних

```text
main → load_data() → (AddressBook, NoteBook)
     → init_registry() → підказки для вводу
     → цикл: parse_input → execute_command → Command.execute → print
     → save_data() при завершенні
```

## Команди

`init_registry()` реєструє назву, формат, опис, групу й обробник кожної команди. `Command.execute()` передає обробнику контактів `(args, book)`, обробнику нотаток — `(args, notebook)`, а `help` — реєстр. `hello`, `exit` і `close` викликаються без аргументів.

Обробники контактів і нотаток повертають рядок для виводу. `CommandFormatError` дає підказку з правильним форматом, а `@input_error` перетворює `ValueError` і `KeyError` на повідомлення користувачу.

## Дані

- `AddressBook` зберігає записи за імʼям. Поля `Record` — `name`, `phones`, `birthday`, `email`, `address`.
- `NoteBook` зберігає нотатки з унікальними ID, текстом і тегами.
- `storage.py` зберігає словник із ключами `book` і `notebook` через `pickle` у `~/.personal_assistant/assistant.pkl`. Запис спочатку йде в тимчасовий файл. Якщо файл неможливо прочитати, помічник відкладає його з розширенням `.corrupt` і починає з порожніх книг.

## Консоль

`console.py` будує таблиці контактів і нотаток, вітання та згруповану довідку `help` через `rich`. `prompt.py` використовує `prompt_toolkit` для автодоповнення, історії вводу й підказок формату з реєстру.

[Приклад вітання й довідки](docs/screenshots/welcome-help.png).
