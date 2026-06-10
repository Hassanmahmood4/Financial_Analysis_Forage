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


