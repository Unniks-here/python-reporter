import logging
from typing import List, Dict
from sqlalchemy import text
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font

from db import get_session

logger = logging.getLogger(__name__)

QUERY = text(
    """
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    WHERE stakeholder_email = :email
    GROUP BY region
    ORDER BY region
    """
)


def fetch_sales_by_region(email: str) -> List[Dict]:
    """Fetch aggregated sales data for a stakeholder."""
    logger.info("Fetching sales data for %s", email)
    with get_session() as session:
        result = session.execute(QUERY, {"email": email})
        rows = [{"region": r[0], "total_sales": r[1]} for r in result]
    return rows


def create_excel(data: List[Dict], path: str) -> None:
    """Generate an Excel report with totals and header styling."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Sales by Region"

    headers = ["Region", "Total Sales"]
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    total = 0
    for row in data:
        ws.append([row["region"], row["total_sales"]])
        total += row["total_sales"]

    ws.append(["Total", total])
    ws[f"A{ws.max_row}"].font = Font(bold=True)

    # Auto-width columns
    for column in range(1, ws.max_column + 1):
        length = max(len(str(cell.value)) for cell in ws[get_column_letter(column)]) + 2
        ws.column_dimensions[get_column_letter(column)].width = length

    wb.save(path)
    logger.info("Saved report to %s", path)
