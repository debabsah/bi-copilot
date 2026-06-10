# KPI Contract — Net Revenue v1.2 (LOCKED 2026-05-20, owner: Finance)  [Define]

- Input: `ORDERS.amount`, **DECIMAL(12,2) — cents precision is contractual** (rebate
  calculations depend on sub-dollar amounts; pinned by Finance after the 2025 rounding
  incident).
- Aggregation: SUM by order_date via rev_summary.
- Re-audit when: any change to the input column's type, source, or filter.
