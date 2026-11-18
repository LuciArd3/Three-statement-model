from models import BalanceSheet , IncomeStatement , CashFlowStatement , Ratios
from typing import Optional

def report_bs(bs: BalanceSheet) -> None:
    """The difference should be 0 for the numbers to tie"""
    diff = bs.difference()
    status = "balances" if diff == 0 else f"OFF BY {diff}"
    print(f"{bs.year}: Total_assets={bs.total_assets()}  Liabilities+Equity={bs.total_liabilities_and_equity()}  -> {status}")

def report_is(i_s: IncomeStatement) -> None:
    """The difference should be 0 for the numbers to tie"""
    diff = i_s.difference()
    status = "ties" if diff == 0 else f"OFF BY {diff}"
    print(f"{i_s.year}: net income={i_s.net_income} -> {status}")

def report_cfs(cfs : CashFlowStatement) -> None:
    """The difference should be 0 for the numbers to tie"""
    diff = cfs.difference()
    status = "ties" if diff== 0 else f"OFF BY {diff}"
    print(f"{cfs.year}: ending cash={cfs.ending_cash} -> {status}")

def pct(x: Optional[float]) -> str:
    """Format a ratio as a percentage"""
    return "n/a" if x is None else f"{x:.1%}"

def num(x: Optional[float]) -> str:
    """Format a number with one decimal"""
    return "n/a" if x is None else f"{x:.1f}"

def report_ratios(r: Ratios) -> None:
    print(f"{r.year}: growth:{pct(r.revenue_growth)}  gross margin:{pct(r.gross_margin)}  "
          f"opex:{pct(r.opex_pct_revenue)}  tax rate:{pct(r.tax_rate)}  "
          f"receivable days:{num(r.receivable_days)}  inventory days:{num(r.inventory_days)}  "
          f"payable days:{num(r.payable_days)}")