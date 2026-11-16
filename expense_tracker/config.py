from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "expenses.db"
TEMPLATES_PATH = PROJECT_ROOT / "templates"
STATIC_PATH = PROJECT_ROOT / "static"

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]
