from db import get_connection

async def set_budget(category: str, monthly_limit: float) -> dict:
    """Set a monthly spending budget for a category."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?) ON CONFLICT(category) DO UPDATE SET monthly_limit = ?",
        (category, monthly_limit, monthly_limit)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Budget for {category} set to ${monthly_limit:.2f}/month"}


async def check_budget(category: str, month: str) -> dict:
    """
    Check spending vs budget for a category this month.
    month format: YYYY-MM
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT monthly_limit FROM budgets WHERE category = ?", (category,))
    budget_row = cursor.fetchone()

    cursor.execute(
        "SELECT SUM(total) FROM expenses WHERE category = ? AND date LIKE ?",
        (category, f"{month}%")
    )
    spent_row = cursor.fetchone()
    conn.close()

    spent = spent_row[0] or 0.0
    if not budget_row:
        return {"category": category, "spent": round(spent, 2), "budget": None, "status": "no budget set"}

    limit = budget_row[0]
    remaining = limit - spent
    pct = (spent / limit) * 100

    status = "ok" if pct < 80 else ("warning" if pct < 100 else "over budget")

    return {
        "category": category,
        "month": month,
        "spent": round(spent, 2),
        "budget": limit,
        "remaining": round(remaining, 2),
        "percent_used": round(pct, 1),
        "status": status
    }