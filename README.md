# Three-statement model (US equities)

A learning project: a Python model that links a company's income statement,
balance sheet and cash flow statement, built step by step from real 10-K data.

## Status
- [x] Step 1: balance sheet by hand, with a check that assets = liabilities + equity
- [x] Step 2: income statement and cash flow statement
- [ ] Step 3: history ratios (growth, margins, working capital)
- [ ] Step 4: income statement forecast
- [ ] Step 5: balance sheet forecast, cash derived from the cash flow statement
- [ ] Step 6: scenarios, tests, report

## How to run
```
python step1_simple.py
```
Expected output: one line per year, each ending in "balances".

## Design notes
- Money is stored as integers in US$ millions, so there is no floating-point drift.
- Every step ends with a check that can fail (for example, the balance sheet must balance).
- Data is typed from the company's 10-K (Item 8, Financial Statements).

## Data and disclaimer
Figures come from Apple filings on sec.gov. This is an educational project,
not financial advice.

## What I learned
- (add one or two lines after each step)