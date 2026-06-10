# Test specification — the test-design-from-contract mode (kpi-contract)

Load when the contract locks or a locked contract returns with "what tests should we
add?". The spec is a PROJECTION of the contract — every pinned fork already implies its
check; nothing here invents requirements the contract doesn't carry. It is a spec the
user implements (dbt tests, Great Expectations, SQL asserts) — never runnable code.

## The derivation table (pinned fork → test)

| Contract element | Derived test | Typical stack form |
|---|---|---|
| Declared grain | uniqueness at that grain | dbt `unique` on the grain key(s) |
| Pinned population / filters | row-class exclusion check (test rows, statuses, internal) | `accepted_values` / not-exists assert |
| Pinned enums & statuses | accepted-values per column | dbt `accepted_values` |
| Null/zero policy | not-null where pinned; explicit zero-vs-null assertion | `not_null` + a custom assert |
| Date basis & timezone | boundary-day check (rows land in the pinned day) | custom SQL assert on the boundary hour |
| Late-data rule | freshness threshold derived from the rule | dbt `freshness` / max(loaded_at) assert |
| Source-of-record reconciliation | periodic tie-out within the pinned tolerance | scheduled comparison (prove-my-parity's discipline) |
| Unit/currency & precision | type/precision assertion (the contract's DECIMAL is contractual) | schema test on type/scale |
| Versioning trigger (`Re-audit when:`) | a change-detection note: which schema/source changes must re-fire this spec | CI schema-diff note |

## The artifact section (appended to the contract, versioned with it)

```markdown
## Test specification (derived v<N> — from contract v<N>, <date>)
_A spec, not code. Each line cites the contract clause it projects; implement in your
stack and check off. Re-derive when the contract re-versions._

| # | Test | From clause | Stack form (suggested) | Implemented? |
|---|---|---|---|---|
| 1 | unique (customer_id, month) | grain | dbt unique | [ ] |
| … | | | | |

Acceptance criteria note: this table IS the build's acceptance checklist — the build is
done when every line is implemented and green.
```

Composition: lives INSIDE `knowledge-base/kpi-contract.md` (no new artifact, no new write
target); re-versions with the contract; a spec line that a later `review-my-query` finding
contradicts is a contract-conformance finding, cited both ways.
