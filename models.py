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
    receivable_days : Optional[float]
    inventory_days : Optional[float]
    payable_days : Optional[float]