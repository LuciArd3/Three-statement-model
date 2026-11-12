from dataclasses import dataclass

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
        """Assets minus (liabilities + equity). Must be 0."""
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


def report(bs: BalanceSheet) -> None:
    diff = bs.difference()
    status = "balances" if diff == 0 else f"OFF BY {diff}"
    print(f"{bs.year}: Total_assets={bs.total_assets()}  Liabilities+Equity={bs.total_liabilities_and_equity()}  -> {status}")

def report_is(i_s: IncomeStatement) -> None:
    diff = i_s.difference()
    status = "ties" if diff == 0 else f"OFF BY{diff}"
    print(f"{i_s.year}: net income={i_s.net_income} -> {status}")


if __name__ == "__main__":
    aapl = [
        BalanceSheet(2025, cash=35934, receivables=39777, inventory=5718, ppe=49834, payables=69860, debt=90678, equity=73733,
                      other_assets= 359241 - (35934 + 39777 + 5718 + 49834) , other_liabilities= 285508 - 69860 - 90678),
        BalanceSheet(2026, cash=36305, receivables=43817, inventory=14541, ppe=52084, payables=82252, debt=78114, equity=112093,
                     other_assets= 404548 - (36305 + 43817 + 14541  + 52084) , other_liabilities=292455 - 82252 - 78114),
    ]

    aapl_income = [
        
    ]
    for bs in aapl:
        report(bs)

    assert aapl[0].difference() == 0 and aapl[1].difference() == 0