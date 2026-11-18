from dataclasses import dataclass
from typing import Optional
from models import BalanceSheet , IncomeStatement, Ratios

def safe_division(n : int , d : int ) -> Optional[float]: 
    """For handling the case when d is 0, avoiding a crash"""
    return None if d == 0 else n /d

def days_of(balance : int, base:int ) -> Optional[float]:
    """Return balance as days of base (balance / base * 365)"""
    ratio = safe_division(balance,base)
    return None if ratio is None else ratio * 365

def compute_ratios(bs : BalanceSheet, curr_is : IncomeStatement, prev_is :Optional[IncomeStatement]) ->Ratios:
    """For turning the statements of a year into ratios that can be used for forecasting"""
    if bs.year != curr_is.year :
        raise ValueError(f"years do not match: balance sheet {bs.year}, income statement {curr_is.year}")

    pretax_profit = curr_is.revenue - curr_is.cost_of_sales - curr_is.operating_expenses + curr_is.other_income

    growth : Optional[float]= None
    if prev_is is not None and prev_is.revenue != 0 : 
        growth = curr_is.revenue / prev_is.revenue - 1  

    return Ratios(
        year=curr_is.year, 
        revenue_growth=growth, 
        gross_margin=safe_division(curr_is.revenue - curr_is.cost_of_sales , curr_is.revenue),
        opex_pct_revenue= safe_division(curr_is.operating_expenses , curr_is.revenue),
        tax_rate=safe_division(curr_is.tax, pretax_profit),
        receivable_days= days_of(bs.receivables , curr_is.revenue),
        inventory_days= days_of(bs.inventory , curr_is.cost_of_sales),
        payable_days= days_of(bs.payables, curr_is.cost_of_sales)
    )