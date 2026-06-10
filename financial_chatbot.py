"""Rule-based financial analysis chatbot prototype.

This script answers a small set of predefined questions using 10-K data
compiled for Microsoft, Tesla, and Apple for fiscal years 2023-2025.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DATA_FILE = Path(__file__).with_name("financial_10k_data.csv")
LATEST_YEAR = 2025
PREVIOUS_YEAR = 2024

MONEY_COLUMNS = {
    "revenue": "Total Revenue",
    "net income": "Net Income",
    "assets": "Total Assets",
    "liabilities": "Total Liabilities",
    "cash flow": "Cash Flow from Operating Activities",
}


def load_financial_data(path: Path = DATA_FILE) -> list[dict[str, object]]:
    """Load financial rows from the CSV and convert numeric columns."""
    rows: list[dict[str, object]] = []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["Fiscal Year"] = int(row["Fiscal Year"])
            for column in MONEY_COLUMNS.values():
                row[column] = int(row[column])
            rows.append(row)
    return rows


def format_money(value: int | float) -> str:
    """Format dollar values in billions for readable chatbot responses."""
    return f"${value / 1_000_000_000:,.2f} billion"


def format_percent(value: float) -> str:
    return f"{value:,.2f}%"


def company_names(rows: list[dict[str, object]]) -> list[str]:
    return sorted({str(row["Company"]) for row in rows})


def find_company(query: str, rows: list[dict[str, object]]) -> str | None:
    query_lower = query.lower()
    for company in company_names(rows):
        if company.lower() in query_lower:
            return company
    return None


def find_year(query: str) -> int:
    for year in (2025, 2024, 2023):
        if str(year) in query:
            return year
    return LATEST_YEAR


def get_row(rows: list[dict[str, object]], company: str, year: int) -> dict[str, object]:
    for row in rows:
        if row["Company"] == company and row["Fiscal Year"] == year:
            return row
    raise ValueError(f"No data found for {company} in {year}.")


def pct_change(previous: int | float, current: int | float) -> float:
    return ((current - previous) / previous) * 100


