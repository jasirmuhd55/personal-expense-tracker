# MyExpense — Personal Expense Tracker

A lightweight personal expense tracking web app built with **Python** and **FastAPI**.
Track your daily spending, view monthly summaries, and filter expenses — all from a clean local web interface.

---

## 📋 What It Does

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Add Expense** | Log an expense with title, amount, category, date, and an optional note |
| 2 | **View All Expenses** | See all expenses in a table, sorted by most recent date first |
| 3 | **Edit / Delete** | Update or remove any expense with instant feedback |
| 4 | **Monthly Summary** | View current month's total spend and a breakdown by category |
| 5 | **Filter & Search** | Filter by category, date range (from/to), and partial title match — filters can be combined |

**Supported categories:** Food · Transport · Shopping · Bills · Entertainment · Other

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | Python + FastAPI | Fast, modern, easy to structure |
| Database | SQLite (built-in `sqlite3`) | Zero setup, runs locally, no extra dependencies |
| Templates | Jinja2 | Server-side HTML rendering, clean separation |
| Frontend | HTML + CSS | Simple, no JavaScript frameworks needed |

---

## 📁 Project Structure

```
expense_tracker_fastapi/
│
├── app.py                        # Entry point → uvicorn app:app --reload
│
├── expense_tracker/
│   ├── config.py                 # Paths + category list (single source of truth)
│   ├── main.py                   # FastAPI app setup + DB init on startup
│   ├── validators.py             # Input validation (title, amount, category, date)
│   │
│   ├── database/
│   │   ├── connection.py         # SQLite connection with WAL mode enabled
│   │   └── schema.py             # Creates the expenses table on first run
│   │
│   └── routers/
│       └── expenses.py           # All routes: list, add, edit, delete
│
├── templates/
│   ├── index.html                # Main dashboard (list + add + filter + summary)
│   └── edit.html                 # Edit expense form
│
├── static/
│   └── style.css                 # All styling
│
├── expenses.db                   # Auto-created on first run (not in git)
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

> **Requirements:** Python 3.9 or higher

### Step 1 — Create a virtual environment

```bash
python -m venv venv
```

### Step 2 — Activate it

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bat
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Start the server

```bash
uvicorn app:app --reload
```

### Step 5 — Open in your browser

```
http://127.0.0.1:8000
```

> The SQLite database (`expenses.db`) and the `expenses` table are created **automatically** on first startup. No manual setup needed.

---

## ⚙️ Implementation Decisions

- **No ORM** — Used Python's built-in `sqlite3` with parameterized queries. Keeps the project simple, secure against SQL injection, and dependency-free.
- **Server-side rendering** — Jinja2 templates render HTML on the backend. No JavaScript framework is needed for this scope.
- **SQL aggregation** — Monthly totals and category breakdowns are computed directly in SQL using `SUM` and `GROUP BY`, keeping the Python code clean.
- **WAL mode** — SQLite is configured with `PRAGMA journal_mode=WAL` to prevent database locking issues under concurrent requests.
- **Single source of truth** — Categories are defined once in `config.py` and used in both the validator and the router — no duplication.
- **Parameterized filters** — All filter conditions (category, date range, title search) are built dynamically and passed as SQL parameters, never string-interpolated.

---

## ✅ Requirements Coverage

All five requirements from the assessment are fully implemented:

- [x] Add expense with title, amount, category, date (defaults to today), and optional note
- [x] View all expenses sorted by date descending, all fields shown
- [x] Edit and delete any expense
- [x] Monthly summary — total spend + category breakdown for the current month
- [x] Filter by category, date range, and partial title/note match

---

## ⏭️ What Was Skipped & Why

Nothing from the five core requirements was skipped.

The following were **intentionally left out** — either excluded by the spec or out of scope for a 2-hour assessment:

| Skipped | Reason |
|---------|--------|
| Authentication / multi-user | Explicitly excluded by spec |
| Deployment | Explicitly excluded by spec |
| Test suite | Explicitly excluded by spec |
| Multi-currency | Spec says "your local currency" — hardcoded to ₹ |
| ORM (SQLAlchemy etc.) | Built-in `sqlite3` is sufficient and simpler |

---

## 🎨 Frontend Note

My primary strength is **backend development**. I have a basic working knowledge of HTML and CSS. The frontend UI design and styling in this project was developed with the assistance of AI tools. All backend logic — routing, validation, database queries, and application structure — was written independently.

---

## ⚠️ Known Rough Edges

- **Flash messages via URL params** — Success/error messages are passed as query parameters (`?message=...`). Refreshing the page after an action replays the message. A proper session-based flash would fix this but adds complexity beyond the scope of this assessment.
- **No month navigation** — The monthly summary always shows the current calendar month. Navigating to past months was not part of the requirements.
- **No pagination** — All expenses load at once. Fine for personal use; a large dataset would benefit from pagination.
