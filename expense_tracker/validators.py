from datetime import date

from .config import CATEGORIES


def validate_expense(title, amount_text, category, expense_date, note):
    title = title.strip()
    note = (note or "").strip()

    if not title:
        return None, "Title is required."

    try:
        amount = float(amount_text)
    except (TypeError, ValueError):
        return None, "Amount must be a valid number."

    if amount <= 0:
        return None, "Amount must be greater than zero."

    if category not in CATEGORIES:
        return None, "Please select a valid category."

    try:
        date.fromisoformat(expense_date)
    except (TypeError, ValueError):
        return None, "Please enter a valid date."

    return {
        "title": title,
        "amount": amount,
        "category": category,
        "date": expense_date,
        "note": note,
    }, None
