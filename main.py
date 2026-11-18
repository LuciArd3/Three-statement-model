from models import BalanceSheet , IncomeStatement , CashFlowStatement
from ratios import compute_ratios
from reports import report_bs , report_is , report_cfs , report_ratios

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

    assert all(s.difference() == 0 for s in aapl_bs + aapl_is + aapl_cfs)

    for i_s , cfs in zip(aapl_is, aapl_cfs):
        assert i_s.year == cfs.year
        assert i_s.net_income == cfs.net_income , f"{i_s.year}: net income differs between the IS and the CFS"
    assert aapl_cfs[1].beginning_cash == aapl_cfs[0].ending_cash, "2026 beginning cash != 2025 ending cash!"

    ratios= []
    for i , (bs, curr_is) in enumerate(zip(aapl_bs , aapl_is)):
        prev_is = aapl_is[i-1] if i > 0 else None
        ratios.append(compute_ratios(bs , curr_is , prev_is))

    for r in ratios : 
        report_ratios(r)

    assert ratios[0].revenue_growth is None
    assert abs(ratios[1].revenue_growth - 0.1506) < 0.0005
    assert abs(ratios[0].gross_margin - 0.4691) < 0.0005
    assert abs(ratios[1].gross_margin - 0.4879) < 0.0005
    assert abs(ratios[0].tax_rate - 0.1561) < 0.0005
    assert abs(ratios[1].tax_rate - 0.1699) < 0.0005
    assert abs(ratios[1].receivable_days - 33.4) < 0.05
    
    zero_bs = BalanceSheet(2030, 0, 0, 0, 0, 0, 0, 0)
    zero_is = IncomeStatement(2030, 0, 0, 0, 0, 0, 0)
    z = compute_ratios(zero_bs, zero_is, zero_is)
    assert z.revenue_growth is None and z.gross_margin is None and z.tax_rate is None