# test-spec-derivation fixture (answer key)

Demo target for the test-design-from-contract MODE (kpi-contract host). Every pinned
clause implies a check; the mode's value is the FORM — a spec where each line cites its
clause, doubling as acceptance criteria.

## PASS
- A test-spec table derived clause-by-clause: uniqueness at (customer_id, month);
  population exclusions (trial/internal/test); the 30-day reactivation window asserted;
  UTC month-boundary check; freshness/closure at T+2 per the 48h late rule; not_null
  customer_id + the null-end_date-means-active assertion; the 0.5% CRM reconciliation
  (prove-my-parity's discipline); a re-derive note tied to Re-audit when.
- Each line CITES the contract clause it projects; framed as spec the user implements
  (dbt/GE/SQL asserts) — NEVER runnable code; appended as a versioned section of the
  contract; named as the build's acceptance criteria.

## FAIL
- Runnable dbt YAML/SQL written out; tests invented beyond the contract; or a generic
  test list that doesn't cite clauses.
