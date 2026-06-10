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


def revenue_response(rows: list[dict[str, object]], query: str) -> str:
    company = find_company(query, rows) or "Apple"
    year = find_year(query)
    row = get_row(rows, company, year)
    return (
        f"In fiscal {year}, {company} reported total revenue of "
        f"{format_money(row['Total Revenue'])}."
    )


def net_income_change_response(rows: list[dict[str, object]], query: str) -> str:
    company = find_company(query, rows) or "Microsoft"
    current = get_row(rows, company, LATEST_YEAR)
    previous = get_row(rows, company, PREVIOUS_YEAR)
    current_value = current["Net Income"]
    previous_value = previous["Net Income"]
    change = current_value - previous_value
    change_pct = pct_change(previous_value, current_value)
    direction = "increased" if change >= 0 else "decreased"
    return (
        f"{company}'s net income {direction} from {format_money(previous_value)} "
        f"in {PREVIOUS_YEAR} to {format_money(current_value)} in {LATEST_YEAR}. "
        f"That is a change of {format_money(abs(change))}, or "
        f"{format_percent(abs(change_pct))}."
    )


def cash_flow_response(rows: list[dict[str, object]], query: str) -> str:
    company = find_company(query, rows) or "Microsoft"
    year = find_year(query)
    row = get_row(rows, company, year)
    return (
        f"In fiscal {year}, {company}'s cash flow from operating activities was "
        f"{format_money(row['Cash Flow from Operating Activities'])}."
    )


def highest_revenue_response(rows: list[dict[str, object]], query: str) -> str:
    year = find_year(query)
    year_rows = [row for row in rows if row["Fiscal Year"] == year]
    top = max(year_rows, key=lambda row: row["Total Revenue"])
    return (
        f"In fiscal {year}, {top['Company']} had the highest revenue among the "
        f"three companies at {format_money(top['Total Revenue'])}."
    )


def strongest_growth_response(rows: list[dict[str, object]]) -> str:
    growth_results: list[tuple[str, float]] = []
    for company in company_names(rows):
        start = get_row(rows, company, 2023)["Total Revenue"]
        end = get_row(rows, company, 2025)["Total Revenue"]
        growth_results.append((company, pct_change(start, end)))

    company, growth = max(growth_results, key=lambda item: item[1])
    return (
        f"From 2023 to 2025, {company} had the strongest total revenue growth "
        f"among the three companies, increasing by {format_percent(growth)}."
    )


def trends_response() -> str:
    return (
        "Main trend summary: Microsoft showed the most consistent growth across "
        "revenue, net income, and operating cash flow. Apple remained the largest "
        "revenue generator and delivered a strong profitability rebound in 2025. "
        "Tesla's revenue was relatively flat and its net income declined sharply, "
        "showing the greatest profitability pressure among the three companies."
    )


