# Test specification — the test-design-from-contract mode (model-contract)

Load when the design locks or returns with "what tests should we add?". The spec PROJECTS
the locked design — each pinned modelling fork already implies its check. A spec for the
user's stack; never DDL, never runnable tests.

## The derivation table (pinned fork → test)

| Design element | Derived test | Typical stack form |
|---|---|---|
| Fact grain (declared) | uniqueness/PK at the declared grain | dbt `unique` on grain keys |
| Source-grain gate result | row-count ratio source→fact within expected bounds | custom assert (no silent fan-out/loss) |
| Each dimension relationship | referential integrity fact→dim; orphan policy as pinned | dbt `relationships` + orphan assert |
| SCD type per dimension | as-of behavior: a changed entity reads correctly at both dates | custom as-of query pair |
| Conformance claims | the conformed dim agrees across marts (name, keys, members) | cross-mart comparison |
| Additivity rules | totals recompute at total grain for non/semi-additive measures | total-vs-sum assert |
| Late-arriving / early-fact policy | the pinned handling holds (placeholder keys, backfill) | targeted assert on the policy |
| Null/default member policy | unknown-member key present and used as pinned | not_null + default-member check |

## The artifact section (appended to the model contract, versioned with it)

```markdown
## Test specification (derived v<N> — from design v<N>, <date>)
_A spec, not code. Each line cites the design fork it projects. This table doubles as the
build's acceptance criteria — done = every line implemented and green._

| # | Test | From fork | Stack form (suggested) | Implemented? |
|---|---|---|---|---|
```

Composition: lives INSIDE `knowledge-base/model-contract.md`; re-derive when the design
re-versions; a `change-impact` assessment that touches a tested element should cite the
spec line it would invalidate.
