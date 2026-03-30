import json
from db import get_connection

async def save_expense(date:str, merchant:str, category:str, total:float, items:list) -> dict:
    """Save an extracted expense to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (date, merchant, category, total, items) VALUES (?, ?, ?, ?, ?)",
        (date, merchant, category, total, json.dumps(items))
    )
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()
    return {
        "success": True, 
        "id": expense_id, 
        "message": f"Saved ${total:.2f} at {merchant}"
    }

async def get_expenses(start_date: str = None, end_date: str = None, category: str = None) -> list:
    """Query expenses. Optionally filter by date range or category."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT id, date, merchant, category, total, items FROM expenses WHERE 1=1"
    params = []

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY date DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": r[0], "date": r[1], "merchant": r[2], 
         "category": r[3], "total": r[4], "items": json.loads(r[5] or "[]")}
        for r in rows
    ]

async def get_summary(month: str) -> dict:
    """
    Get spending summary for a month.
    month format: YYYY-MM (e.g. '2026-03')
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT category, SUM(total) as total, COUNT(*) as count
           FROM expenses 
           WHERE date LIKE ?
           GROUP BY category
           ORDER BY total DESC""",
        (f"{month}%",)
    )
    rows = cursor.fetchall()
    conn.close()

    breakdown = [{"category": r[0], "total": round(r[1], 2), "transactions": r[2]} for r in rows]
    grand_total = sum(r["total"] for r in breakdown)

    return {"month": month, "total": round(grand_total, 2), "breakdown": breakdown}