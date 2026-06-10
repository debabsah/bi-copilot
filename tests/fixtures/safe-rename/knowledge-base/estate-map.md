# Estate Map — orders slice  [Understand]
_Drawn 2026-06-08, by D. Chen. **Derived from:** ddl.sql (06-08) · landscape.md (06-08)._
_Coverage: 5 nodes · 3 evidenced edges · 0 unverified · 1 island._

ORDERS → vw_orders_paid (join, ddl) · ORDERS → vw_daily_rev (SELECT *, ddl) →
rev_summary (ddl).

| Edge | Kind | Evidence | Status |
|---|---|---|---|
| ORDERS → vw_orders_paid | join | ddl.sql | evidenced |
| ORDERS → vw_daily_rev | view (SELECT *) | ddl.sql | evidenced |
| vw_daily_rev → rev_summary | view | ddl.sql | evidenced |
| finance_export → ? | — | none | **island — no documented connection; ask Finance what feeds their monthly export** |
