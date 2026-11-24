# project-Awesome1 — Персональний помічник (group-4)

Команда: Neoversity · дошка Trello **Personal Assistant group-4**.

## Старт проєкту

1. Прочитати **[CONTRACT.md](./CONTRACT.md)** — обов'язкові інтерфейси.
2. Прочитати **[ARCHITECTURE.md](./ARCHITECTURE.md)** — структура модулів, потік даних, формат збереження.
3. Кожен обирає блок A / B / C / D у Trello і працює у **своїх** файлах (таблиця в `CONTRACT.md`).
4. Усім **однаково** налаштувати середовище (нижче).

> У репозиторії **немає готового коду** — лише документація та конфіги. Файли з [ARCHITECTURE.md](./ARCHITECTURE.md) створює кожен у **своєму** блоці за [CONTRACT.md](./CONTRACT.md).

## Середовище (`.venv` + `pip`)

На **US-00a** зафіксуйте версію Python (у репо є `.python-version` — зараз `3.12`; можна змінити на `3.14`, якщо всім зручно).

**macOS / Linux:**

```bash
cd project-Awesome1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
```

| Файл | Що встановлюється |
|------|-------------------|
| `requirements.txt` | **`rich`** — гарний вивід у консоль (кольори, таблиці, панелі). |
| `requirements-dev.txt` | Опційно: `pytest`, `ruff`. |

Усі ставлять **`pip install -r requirements.txt`**, щоб `rich` був у кожного.

### Rich — «красива консоль»

**[Rich](https://github.com/Textualize/rich)** — бібліотека для CLI: кольоровий текст, таблиці контактів, рамки з помилками.  
**Не обов’язково для ТЗ** (можна лишити `print`), але ментори дозволяють.

Домовитись на **US-00a**:

- хто веде стиль виводу (один модуль `console.py` або функція в `main.py`);
- команди все одно **повертають `str`**, а Rich використовується в одному місці при `print` (щоб блоки A/B/C не ламали одне одного).

Опційно: `pip install -r requirements-dev.txt` → `pytest`, `ruff`.

**Не комітити** `.venv/` — він у `.gitignore`.

## Мінімум після US-00a

| Хто | Що з'являється в `main` першим |
|-----|----------------------------------|
| **основа** | `main.py`, `address_book.py`, `contact_handlers.py`, `storage.py` (PR #2) |
| **A** | `notes.py`, `note_handlers.py`, потім `storage.py` (Path.home) |
| **B** | `field_handlers.py`, `validators.py` |
| **C** | `search_handlers.py` |
| **D** | `suggest.py` |

## Запуск (коли з'явиться `main.py`)

```bash
python3 main.py
```

## Корисні посилання

- ТЗ (Google Sheets) — чек-лист на картці **Фінал** у Trello
- User stories — картки US-01 … US-13

## Ліцензія / здача

Перед здачею — прогін чек-лістів «ТЗ: основні / додаткові» на картці **Фінал**.