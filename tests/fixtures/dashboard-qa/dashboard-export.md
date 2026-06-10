# Customer Health — export (pages, measures, filters), as of 2026-06-10

## Page filters (defaults)
- FiscalYear = "FY2025" (default; user-changeable)
- Region = All

## Measures
- [Net Revenue] = SUM(orders[amount])                       -- card + monthly trend
- [Active Customers] = DISTINCTCOUNT(orders[customer_id])   -- per-region table, WITH TOTAL ROW (table total = sum of region rows)
- [Avg Deal Size] = AVERAGE(rep_summary[avg_deal_per_rep])  -- card; rep_summary is one row per rep
- [Churn %] = DIVIDE([Churned], [OpeningCustomers])         -- trend tile

## Visuals
- Trend tile titled "Churn improving steadily": line chart of [Churn %], visual-level
  filter Month IN (Mar, Apr, May 2026). (Jan 2026 spiked to 9.1%; Feb 7.2%; Mar 6.8%;
  Apr 6.5%; May 6.3%; full-year view shows the level still above last year's 5.1%.)
- Region table: [Active Customers] by region with a grand-total row.
- Cards: [Net Revenue], [Avg Deal Size]. Subtitle on both: "Live data".

## Dataset
- Import mode extract, last refresh 2026-06-02 (weekly schedule).

## knowledge-base/kpi-contract.md (excerpt)
- Net Revenue v1.2 (LOCKED): SUM of orders.amount, all fiscal years available unless the
  view says otherwise; DECIMAL(12,2).
- Active Customers v1.0 (LOCKED): distinct customers with >=1 order in window; explicitly
  NON-ADDITIVE across regions (customers buy in multiple regions).
