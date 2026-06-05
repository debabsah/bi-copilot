# conformant-query fixture (answer key — never inline into a cold run)

PRECISION / CLEAN CONTROL for review-my-query. `vw_gross_revenue_churn.sql` CONFORMS to
`kpi-contract.md` (Gross Revenue Churn: MRR not logos, cancel + downgrade in the numerator,
start-of-period MRR denominator, trials excluded via `plan_type='paid'`, fiscal US/Pacific,
5-business-day close freeze, billing source, governed exclusions TABLE — not a magic literal list).

Hard negatives (look like defects, are correct):
- the **numerator's** governed-exclusions filter is applied STRUCTURALLY: `revenue_lost` is the right
  side of `LEFT JOIN` from `cohort_mrr` (which already excludes `governed_exclusions`), so only cohort
  accounts' losses are summed. A reviewer who misses this may wrongly flag the numerator as "unfiltered
  vs the denominator" — that is the planted FALSE-POSITIVE trap.
- the `CASE … * -1` loss flip — looks error-prone; the signs are right (deltas stored negative).
- `NOT IN (SELECT account_id FROM governed_exclusions)` — mimics the magic-list defect but is a
  governed, reasoned, owned table. The only fair flag here is an **Advisory**: verify
  `governed_exclusions.account_id` is non-nullable (else `NOT IN` returns no rows).

PASS: concludes **conforms, no Blocking**; at most an Advisory (NOT-IN nullability / readability /
the redundant period predicate). FALSE POSITIVE = inventing a Blocking defect, or flagging the
verbose-but-correct timezone conversion or the governed exclusions as wrong.
