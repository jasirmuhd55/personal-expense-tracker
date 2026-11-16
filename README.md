# MyExpense

Personal expense management application built with Python, FastAPI, SQLite, HTML, and CSS.

## Features

1. Add expenses with title, amount, category, date, and optional note.
2. View expenses sorted by date, newest first.
3. Edit and delete expenses.
4. View the current month's total and category-wise breakdown.
5. Filter by category, date range, and partial title match. Filters can be combined.

Categories: Food, Transport, Shopping, Bills, Entertainment, Other.

## Technologies

- Python
- FastAPI
- SQLite using Python's built-in `sqlite3`
- HTML and CSS
- Jinja2 templates

## Project structure

```text
expense_tracker_fastapi/
├── app.py                    # Backward-compatible Uvicorn entry point
├── expense_tracker/
│   ├── __init__.py
│   ├── config.py             # Project paths and expense categories
│   ├── main.py               # FastAPI app setup and startup
│   ├── validators.py         # Expense input validation
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py     # SQLite connection helper
│   │   └── schema.py         # Database table initialization
│   └── routers/
│       ├── __init__.py
│       └── expenses.py       # Expense pages and CRUD routes
├── expenses.db          # Created automatically on first run
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   └── edit.html
└── static/
    └── style.css
```

The SQLite file remains in the project root so an existing `expenses.db` keeps
working. Python code is grouped under `expense_tracker/`; templates and static
assets stay separate because they are served directly by FastAPI.

## Run locally

Open a terminal in this project folder.

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate it

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the local server

```bash
uvicorn app:app --reload
```

Open the application:

```text
http://127.0.0.1:8000
```

The SQLite database and expenses table are initialized automatically when the application starts.

## Implementation decisions

- FastAPI handles HTTP routes and form submissions.
- Jinja2 renders HTML pages on the server.
- SQLite stores the expense records locally in `expenses.db`.
- Python's built-in `sqlite3` module is used instead of an ORM to keep the project straightforward.
- Parameterized SQL statements are used for database values.
- Monthly totals and category breakdowns are calculated in SQL using `SUM` and `GROUP BY`.
- No deployment is required; the application runs on the local computer.

## Scope and limitations

- Single-user local application.
- No authentication or multi-user support.
- No cloud deployment.
- No additional functionality beyond the five requested requirements.
- The local development server is intended for this practical assessment, not production hosting.

## What was skipped and why

Nothing from the five core requirements was skipped. The following items were intentionally left out because they were either explicitly excluded by the spec or out of scope for a 2-hour assessment:

- **Authentication / multi-user support** — excluded by spec.
- **Deployment** — excluded by spec; the app runs locally.
- **Test suite** — excluded by spec.
- **Multi-currency support** — excluded by spec; the currency symbol is hardcoded to ₹ (Indian Rupee).
- **ORM (e.g. SQLAlchemy)** — not needed; Python's built-in `sqlite3` with parameterized queries is sufficient and keeps the dependency list minimal.

## Known rough edges

- Flash messages (success/error) are passed as URL query parameters, so refreshing the redirected page replays the message. A session-based flash system (e.g. via `starlette.middleware.sessions`) would avoid this but adds complexity beyond the scope of this assessment.
- The monthly summary always shows the **current calendar month**. There is no way to navigate to past months' summaries; that would require additional UI and was not part of the requirements.
- No pagination on the expense list. For a small personal tracker this is fine, but a large dataset would need it.
