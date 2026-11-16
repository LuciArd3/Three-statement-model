from dataclasses import dataclass
from typing import Optional

@dataclass
class BalanceSheet:
    year: int
    cash: int
    receivables: int
    inventory: int
    ppe: int  
    payables: int
    debt: int
    equity: int
    other_assets: int = 0
    other_liabilities: int = 0

    def total_assets(self) -> int:
        return self.cash + self.receivables + self.inventory + self.ppe + self.other_assets

    def total_liabilities_and_equity(self) -> int:
        return self.payables + self.debt + self.other_liabilities + self.equity

    def difference(self) -> int:
        """Assets - (liabilities + equity). Must be 0."""
        return self.total_assets() - self.total_liabilities_and_equity()

@dataclass
class IncomeStatement:
    year : int
    revenue : int 
    cost_of_sales : int
    operating_expenses: int
    other_income : int
    tax : int 
    net_income : int

    def difference(self) -> int:
        return (self.revenue + self.other_income - self.cost_of_sales - self.operating_expenses - self.tax - self.net_income) 

@dataclass
class CashFlowStatement:
    year:int 
    net_income : int 
    beginning_cash : int
    operating : int
    investing : int
    financing : int
    ending_cash : int 
    fx_effect : int = 0 #apple does not present one but other companies might

    def difference(self) -> int:
        return (self.beginning_cash + self.operating + self.investing + self.financing + self.fx_effect - self.ending_cash)

@dataclass(frozen=True)
class Ratios :
    year : int 
    revenue_growth : Optional[float]
    gross_margin : Optional[float]
    opex_pct_revenue : Optional[float] #how much of each dollar of sales goes to running the company
    tax_rate : Optional[float]
    recivable_days : Optional[float]
    inventory_days : Optional[float]
    payable_days : Optional[float]



def safe_division(n : int , d : int ) -> Optional[float]: 
    """For handling the case when d is 0, avoiding a crash"""
    return None if d == 0 else n /d

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
        recivable_days= days_of(bs.receivables , curr_is.revenue),
        inventory_days= days_of(bs.inventory , curr_is.cost_of_sales),
        payable_days= days_of(bs.payables, curr_is.cost_of_sales)
    )


def days_of(balance : int, base:int ) -> Optional[float]:
    """Return balance as days of base (balance / base * 365)"""
    ratio = safe_division(balance,base)
    return None if ratio is None else ratio * 365


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

def report_cfs(cfs : CashFlowStatement):
    """The difference should be 0 for the numbers to tie"""
    diff = cfs.difference()
    status = "ties" if diff== 0 else f"OFF BY {diff}"
    print(f"{cfs.year}: ending cash={cfs.ending_cash} -> {status}")




if __name__ == "__main__":
    aapl_bs = [
        BalanceSheet(2025, cash=35934, receivables=39777, inventory=5718, ppe=49834, payables=69860, debt=90678, equity=73733,
                      other_assets= 359241 - (35934 + 39777 + 5718 + 49834) , other_liabilities= 285508 - 69860 - 90678),
        BalanceSheet(2026, cash=36305, receivables=43817, inventory=14541, ppe=52084, payables=82252, debt=78114, equity=112093,
                     other_assets= 404548 - (36305 + 43817 + 14541  + 52084) , other_liabilities=292455 - 82252 - 78114),
    ]

    aapl_is = [
        IncomeStatement(2025, revenue=416161 , cost_of_sales=220960 , operating_expenses=62151 , other_income=-321 , tax=20719, net_income=112010),
        IncomeStatement(2026, revenue=478834  , cost_of_sales=245232  , operating_expenses=75539, other_income=1174, tax=27062, net_income=132175)
    ]

    aapl_cfs =[
        CashFlowStatement(2025, net_income=112010 , beginning_cash=29943 , operating=111482, investing=15195 , financing=-120686, ending_cash=35934 ),
        CashFlowStatement(2026,net_income = 132175, beginning_cash=35934, operating=145097, investing=-17280, financing=-127446, ending_cash=36305 ),
    ]
    for bs in aapl_bs:
        report_bs(bs)

    for i_s in aapl_is:
        report_is(i_s)

    for cfs in aapl_cfs : 
        report_cfs(cfs)

    assert aapl_bs[0].difference() == 0 and aapl_bs[1].difference() == 0
    assert aapl_is[0].difference() == 0 and aapl_is[1].difference() == 0 
    assert aapl_cfs[0].difference() == 0 and aapl_cfs[1].difference() == 0 


    assert all(s.difference() == 0 for s in aapl_bs + aapl_is + aapl_cfs)

    for i_s , cfs in zip(aapl_is, aapl_cfs):
        assert i_s.year == cfs.year
        assert i_s.net_income == cfs.net_income , f"{i_s.year}: net income differs between the IS and the CFS"
        assert aapl_cfs[1].beginning_cash == aapl_cfs[0].ending_cash, "2026 beginning cash != 2025 ending cash!"

    ratios= []
    for i , (bs, curr_is) in enumerate(zip(aapl_bs , aapl_is)):
        prev = aapl_is[i-1] if i > 0 else None
        ratios.append(compute_ratios(bs , curr_is , prev_is))