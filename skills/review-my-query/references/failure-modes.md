# Failure modes — review-my-query

Load when running the engine (loop step 3). Two layers: **conformance** (does the code implement each pinned fork of `kpi-contract.md`?) and the **taxonomy** below (the classic analytics defects). Comprehensive thinking, lean output: hunt all of it; record only the findings that bite.

## Severity rubric — grade by ship-impact, not by taste
- **Blocking** — ships a wrong number. A conformance breach (the code computes a different thing than the contract pins) or a correctness bug that is wrong *now*. Escalates to `open-questions.md`.
- **Latent** — correct today, will break under conditions: an unhandled edge, an SCD that will move, late-arriving data, a magic filter that will rot, a NULL path not yet hit.
- **Advisory** — correct and robust, but unclear or unmaintainable: naming, structure, a missing comment on a non-obvious choice.

Each finding records: **location · failure mode · what wrong result it produces · fix direction.** The fix direction is words, optionally one *tiny* illustrative fragment — never a finished, drop-in query.

## The taxonomy (the engine)
Not every mode applies to every object. Run the list, keep the ones that bite.

**Grain & cardinality**
- Fan-out (1-to-many) join silently multiplying rows → sums and counts overstated.
- Aggregation at the wrong grain; double-counting; missing dedup; accidental cross join.
- Denominator/numerator built from misaligned populations → rows silently dropped or mismatched.

**Filter & context**
- Filter at the wrong stage (WHERE vs HAVING vs the join's ON) → rows kept/dropped at the wrong time.
- Filter that silently drops NULLs (`col <> 'x'` excludes NULL `col`).
- Measure / `CALCULATE` filter-context and calc-group interaction overriding or stacking unexpectedly.
- Hardcoded magic filter with no documented reason → silently edits the number; provenance lost.

**NULL & type**
- `NOT IN (subquery with NULLs)` returns nothing; `COUNT(col)` vs `COUNT(*)`; `AVG` ignoring NULLs.
- Division by zero / NULL with no guard; implicit casts that truncate or round.

**Time**
- Timezone: truncating UTC when the report is in a local/reporting zone → boundary rows land in the wrong period.
- Period off-by-one; calendar vs fiscal; as-of date vs transaction date; DST.
- Late-arriving data not restated (or restated when it should be frozen).

**Set logic**
- `UNION` (dedups, often unintended) vs `UNION ALL`; `EXCEPT`/`INTERSECT` NULL handling.
- Anti-join via `NOT IN` vs `NOT EXISTS` (NULL trap) vs `LEFT JOIN ... IS NULL`.

**Dimensional / SCD**
- Slowly-changing dimension not handled — current attribute used where as-of was needed (or vice-versa).
- Point-in-time join wrong; late-binding dimension; many-to-many relationship ambiguity.

**Security / scope**
- RLS leakage or bypass; an aggregation that escapes row scope; a dev/sample account masking production RLS.

**Determinism / reproducibility**
- `TOP` / `LIMIT` without `ORDER BY`; window-function ties; unpinned `CURRENT_DATE` / `NOW()`; non-deterministic aggregation order.

> Two rules while hunting: a finding is a **departure from the contract or a real bug**, not your style preference; and an **unknown is a question for the user**, not a guess you write code around.

## Worked example — reviewing `vw_monthly_churn` against the locked contract
The inherited board-churn view (counts canceled logos / accounts active at month start) reviewed against a contract that pins **MRR-based NRR + gross revenue churn**, trials excluded, contraction included, fiscal US/Pacific, 5-business-day-then-freeze. The signature output:

```markdown
## Findings
| # | Location | Failure mode | What it produces | Severity | Fix direction |
|---|---|---|---|---|---|
| 1 | whole view | conformance: revenue unit — counts logos, contract pins MRR | a logo-churn number standing in for revenue retention; can look flat while MRR bleeds | Blocking | this can't be patched into NRR; rebuild against billing MRR per the contract (start-of-period cohort MRR, expansion/contraction/churn) |
| 2 | `WHERE s.status='active'` | conformance + filter: trials carry status='active'; contract excludes trials | denominator inflated with non-paying trials | Blocking | exclude trials by the real trial marker (confirm the field with the user) |
| 3 | `DATE_TRUNC('month', period_start/canceled_at)` | time: UTC truncation, contract pins fiscal US/Pacific | cancellations near month-end land in the wrong period | Blocking | truncate in the reporting timezone on the fiscal calendar before grouping |
| 4 | `active_start` CTE | grain: buckets by the month a period *started*, not "active at month start"; join then requires same month | denominator is "started this month"; prior-cohort cancellations silently drop → churn undercounted | Blocking | define the start cohort as a point-in-time membership test (active on the period's first instant), independent of the cancel month |
| 5 | `NOT IN (4471, 4472, 5012, 5013, 5014)` | filter: unexplained magic list ("no idea who these are") | silently removes accounts no one can identify; provenance lost | Latent | identify and document, or remove; if real, move to a documented exclusion table with a reason |
| 6 | `acct.plan_code <> 'internal'` | NULL: `NULL <> 'internal'` is NULL → falsy | accounts with a NULL plan_code silently dropped | Latent | decide intent; `plan_code IS DISTINCT FROM 'internal'` if NULLs should stay |
| 7 | no close rule | time/late data: contract pins 5-business-day-then-freeze | a backdated cancellation silently changes an already-reported month | Latent | apply the close-then-freeze rule from the contract |
| 8 | `1.0 * lost / start` | determinism: no zero guard | divide-by-zero / NULL on an empty cohort month | Advisory | guard the denominator, e.g. `NULLIF(..., 0)` |

## Verdict
- **Blocking:** 4 — must resolve before this feeds the board or gets defended (most fundamentally, it answers a different question than the contract).
- **Latent:** 3 — will distort or drift under real data.
- **Advisory:** 1.
- **Assumptions this review depends on:** trial marker field, fiscal-calendar definition, and the identity of the excluded account IDs all remain open (asked of the user; not assumed).
```

Note what the review does NOT do: it never rewrites the view, never writes the MRR rebuild, and never invents the trial flag or MRR column names to make a fix runnable. It locates, names, grades, and points — the user makes the change.
