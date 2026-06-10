# Financial Analysis Chatbot Documentation

## Overview

This project is a simplified rule-based financial chatbot prototype. It answers a small set of predefined questions using financial data extracted from the 2023-2025 10-K filings of Microsoft, Tesla, and Apple.

The chatbot does not use a machine learning model. Instead, it uses straightforward Python logic to match a user question to a supported financial query and then calculates the answer from `financial_10k_data.csv`.

## Files Included

- `financial_chatbot.py`: Main command-line chatbot script.
- `financial_10k_data.csv`: Source financial dataset from the 10-K extraction task.
- `chatbot_test_results.txt`: Sample chatbot test run with expected responses.
- `chatbot_documentation.md`: This documentation file.

## How to Run

Run the chatbot interactively:

```bash
python3 financial_chatbot.py
```

Run the built-in demonstration questions:

```bash
python3 financial_chatbot.py --demo
```

## Supported Questions

The chatbot can answer predefined questions such as:

- What is Apple's total revenue in 2025?
- How has Microsoft's net income changed over the last year?
- What is Tesla's operating cash flow in 2024?
- Which company had the highest revenue in 2025?
- Which company had the strongest revenue growth?
- What are the main financial trends?

The chatbot also supports `help`, which prints example questions and available companies.

## How It Works

1. The script loads `financial_10k_data.csv`.
2. It converts fiscal year and financial metric columns into numeric values.
3. It checks the user's question for keywords such as `revenue`, `net income`, `cash flow`, `highest`, `growth`, and `trends`.
4. It selects the matching response function.
5. It returns a formatted answer using values from the dataset.

For example, a revenue question looks up the selected company and fiscal year, then formats the answer in billions of dollars.

## Data Used

The dataset includes these companies:

- Microsoft
- Tesla
- Apple

The dataset includes these fiscal years:

- 2023
- 2024
- 2025

The dataset includes these financial metrics:

- Total Revenue
- Net Income
- Total Assets
- Total Liabilities
- Cash Flow from Operating Activities

## Limitations

- The chatbot only answers predefined financial questions.
- It does not understand every possible natural-language question.
- It does not fetch live financial data.
- It uses historical 10-K data only.
- It does not provide investment advice.
- It is a prototype designed for learning chatbot logic, not a production financial assistant.

## Summary

This chatbot demonstrates how financial analysis can be turned into a simple conversational interface. A more advanced version could add natural-language processing, richer company comparisons, live data retrieval, and source citations for each answer.
