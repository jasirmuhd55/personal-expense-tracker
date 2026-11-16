from datetime import date

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..config import CATEGORIES, TEMPLATES_PATH
from ..database import get_db_connection
from ..validators import validate_expense

router = APIRouter()
templates = Jinja2Templates(directory=str(TEMPLATES_PATH))


@router.get("/")
def index(
    request: Request,
    category: str = "",
    from_date: str = "",
    to_date: str = "",
    title: str = "",
    message: str = "",
    message_type: str = "",
):
    today = date.today()
    current_month = today.strftime("%Y-%m")

    for label, value in (("From date", from_date), ("To date", to_date)):
        if value:
            try:
                date.fromisoformat(value)
            except ValueError:
                return RedirectResponse(
                    url="/?message=" + label.replace(" ", "%20") + "%20is%20invalid.&message_type=error",
                    status_code=303,
                )

    if from_date and to_date and from_date > to_date:
        return RedirectResponse(
            url="/?message=From%20date%20cannot%20be%20later%20than%20To%20date.&message_type=error",
            status_code=303,
        )

    conditions = []
    parameters = []

    if category:
        if category not in CATEGORIES:
            return RedirectResponse(
                url="/?message=Invalid%20category%20filter.&message_type=error",
                status_code=303,
            )
        conditions.append("category = ?")
        parameters.append(category)

    if from_date:
        conditions.append("date >= ?")
        parameters.append(from_date)

    if to_date:
        conditions.append("date <= ?")
        parameters.append(to_date)

    if title.strip():
        conditions.append("title LIKE ?")
        parameters.append(f"%{title.strip()}%")

    query = "SELECT * FROM expenses"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY date DESC, id DESC"

    with get_db_connection() as connection:
        expenses = connection.execute(query, parameters).fetchall()
        monthly_total = connection.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date LIKE ?",
            (current_month + "%",),
        ).fetchone()[0]
        category_totals = connection.execute(
            """
            SELECT category, SUM(amount) AS total
            FROM expenses
            WHERE date LIKE ?
            GROUP BY category
            ORDER BY category
            """,
            (current_month + "%",),
        ).fetchall()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "expenses": expenses,
            "categories": CATEGORIES,
            "selected_category": category,
            "from_date": from_date,
            "to_date": to_date,
            "title_filter": title,
            "monthly_total": monthly_total,
            "category_totals": category_totals,
            "current_month": today.strftime("%B %Y"),
            "message": message,
            "message_type": message_type,
            "today": today.isoformat(),
        },
    )


@router.post("/add")
def add_expense(
    title: str = Form(...),
    amount: str = Form(...),
    category: str = Form(...),
    expense_date: str = Form(..., alias="date"),
    note: str = Form(""),
):
    data, error = validate_expense(title, amount, category, expense_date, note)
    if error:
        return RedirectResponse(
            url="/?message=" + error.replace(" ", "%20") + "&message_type=error",
            status_code=303,
        )

    with get_db_connection() as connection:
        connection.execute(
            """
            INSERT INTO expenses (title, amount, category, date, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (data["title"], data["amount"], data["category"], data["date"], data["note"]),
        )

    return RedirectResponse(
        url="/?message=Expense%20added%20successfully.&message_type=success",
        status_code=303,
    )


@router.get("/edit/{expense_id}")
def edit_expense_page(request: Request, expense_id: int, message: str = "", message_type: str = ""):
    with get_db_connection() as connection:
        expense = connection.execute(
            "SELECT * FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()

    if expense is None:
        return RedirectResponse(
            url="/?message=Expense%20not%20found.&message_type=error",
            status_code=303,
        )

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "expense": expense,
            "categories": CATEGORIES,
            "message": message,
            "message_type": message_type,
        },
    )


@router.post("/edit/{expense_id}")
def update_expense(
    expense_id: int,
    title: str = Form(...),
    amount: str = Form(...),
    category: str = Form(...),
    expense_date: str = Form(..., alias="date"),
    note: str = Form(""),
):
    data, error = validate_expense(title, amount, category, expense_date, note)
    if error:
        return RedirectResponse(
            url=f"/edit/{expense_id}?message=" + error.replace(" ", "%20") + "&message_type=error",
            status_code=303,
        )

    with get_db_connection() as connection:
        existing = connection.execute(
            "SELECT id FROM expenses WHERE id = ?", (expense_id,)
        ).fetchone()
        if existing is None:
            return RedirectResponse(
                url="/?message=Expense%20not%20found.&message_type=error",
                status_code=303,
            )
        connection.execute(
            """
            UPDATE expenses
            SET title = ?, amount = ?, category = ?, date = ?, note = ?
            WHERE id = ?
            """,
            (data["title"], data["amount"], data["category"],
             data["date"], data["note"], expense_id),
        )

    return RedirectResponse(
        url="/?message=Expense%20updated%20successfully.&message_type=success",
        status_code=303,
    )


@router.post("/delete/{expense_id}")
def delete_expense(expense_id: int):
    with get_db_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM expenses WHERE id = ?", (expense_id,)
        )

    if cursor.rowcount == 0:
        message = "Expense%20not%20found."
        message_type = "error"
    else:
        message = "Expense%20deleted%20successfully."
        message_type = "success"

    return RedirectResponse(
        url=f"/?message={message}&message_type={message_type}",
        status_code=303,
    )
