# Failure modes — review-my-query

Load when running the engine (loop step 3). Two layers: **conformance** (does the code implement each pinned fork of `kpi-contract.md`?) and the **taxonomy** below (the classic analytics defects). Comprehensive thinking, lean output: hunt all of it; record only the findings that bite.

## Severity rubric — grade by ship-impact, not by taste, and Blocking only when established
- **Blocking** — ships a wrong number you can demonstrate **from what's in hand**, with no plausible reading of the unseen schema under which the code is correct: a conformance breach (computes a different thing than the contract pins), an omitted contract-required transformation, or a logic error visible in the code itself. Escalates to `open-questions.md`.
- **Latent / verify** — real ship-impact that is **conditional**: either correct-today-will-break (an unhandled edge, an SCD that will move, late-arriving data, a magic filter that will rot, a NULL path not yet hit), *or* a potential defect that hinges on a fact you cannot see (a table's grain, a column's type/nullability, whether a `status` value includes trials). State the discriminating check and what it becomes if confirmed ("→ Blocking if …"). A resolve-before-ship item — but never graded Blocking on an assumption.
- **Advisory** — correct and robust, but unclear or unmaintainable: naming, structure, a missing comment on a non-obvious choice.

**The Blocking bar, sharply:** if whether the number is wrong depends on a schema fact you can't see — and there is a plausible world where the code conforms — it is **Latent / verify**, not Blocking. Over-blocking a conformant query (a wall of Blockings that are really "verify X") makes every real Blocking suspect; a clean query must be allowed to come back "conforms — no Blocking."

Each finding records: **location · failure mode · what wrong result it produces · fix direction.** The fix direction is words, optionally one *tiny* illustrative fragment — never a finished, drop-in query.

## The taxonomy (the engine)
Not every mode applies to every object. Run the list, keep the ones that bite.

**Grain & cardinality**
- Fan-out (1-to-many) join silently multiplying rows → sums and counts overstated.
- Aggregation at the wrong grain; double-counting; missing dedup; accidental cross join.
- Denominator/numerator built from misaligned populations → rows silently dropped or mismatched.
- **Non-additive measure re-aggregated below/across its valid grain** — a correct measure summed or sliced where its math doesn't hold. **Tell: it ties to the grand total but is wrong per-slice — a total tie-out does NOT clear it.**
  - *avg-of-ratios / average-of-averages* — sum the components and divide once at the slice; don't average the rates.
  - *COUNT(DISTINCT) summed across slices* — distinct counts don't add; anything spanning slices double-counts.
  - *semi-additive balance (MRR, headcount, inventory, AR) summed across time* — take period-end or average, don't sum months.
  Text tells: `SUM`/`AVG` wrapping a ratio or already-aggregated measure; `COUNT(DISTINCT)` in a summed subtotal; a measure used at a grain ≠ its definition. Read-only check: re-derive at the breakdown grain from summed components and compare to the slice. Blocking only when the code text shows it; otherwise Latent / verify + that check. When a KB exists, anchor to the additivity class `model-contract` pinned.

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
- Period off-by-one; calendar vs fiscal; as-of date vs transaction date.
- **DST / offset arithmetic:** a fixed `UTC±N` or hardcoded "+8h" offset instead of a named, DST-aware zone double-/zero-counts the repeated or skipped local hour at a transition, and is wrong for half the year. → does the code use a named timezone or a fixed offset?
- **Incremental watermark:** a high-watermark filter on load-time / `updated_at` drops rows whose *business event-time* predates the advanced watermark — late rows silently never loaded (distinct from the existing "loaded but not restated"). → is the watermark column the event-time grain the metric is keyed on? *(reads the predicate in the code, not the load schedule)*
- Late-arriving data not restated (or restated when it should be frozen) — incl. a query that recomputes a "frozen" period live instead of reading the frozen snapshot.

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
| 2 | `WHERE s.status='active'` | conformance/filter: contract excludes trials; this filter doesn't *explicitly* exclude them | **if** `status='active'` includes trials → denominator inflated with non-paying trials (wrong number); if trials carry a different status → conforms | Latent / verify (→ Blocking if confirmed) | confirm whether trials carry `status='active'`; if so, exclude by the real trial marker — don't assume either way |
| 3 | `DATE_TRUNC('month', period_start/canceled_at)` | time: UTC truncation, contract pins fiscal US/Pacific | cancellations near month-end land in the wrong period | Blocking | truncate in the reporting timezone on the fiscal calendar before grouping |
| 4 | `active_start` CTE | grain: buckets by the month a period *started*, not "active at month start"; join then requires same month | denominator is "started this month"; prior-cohort cancellations silently drop → churn undercounted | Blocking | define the start cohort as a point-in-time membership test (active on the period's first instant), independent of the cancel month |
| 5 | `NOT IN (4471, 4472, 5012, 5013, 5014)` | filter: unexplained magic list ("no idea who these are") | silently removes accounts no one can identify; provenance lost | Latent | identify and document, or remove; if real, move to a documented exclusion table with a reason |
| 6 | `acct.plan_code <> 'internal'` | NULL: `NULL <> 'internal'` is NULL → falsy | accounts with a NULL plan_code silently dropped | Latent | decide intent; `plan_code IS DISTINCT FROM 'internal'` if NULLs should stay |
| 7 | no close rule | time/late data: contract pins 5-business-day-then-freeze | a backdated cancellation silently changes an already-reported month | Latent | apply the close-then-freeze rule from the contract |
| 8 | `1.0 * lost / start` | determinism: no zero guard | divide-by-zero / NULL on an empty cohort month | Advisory | guard the denominator, e.g. `NULLIF(..., 0)` |
| 9 | emitted `churn_rate` (`1.0*lost/start`) | grain/additivity: a per-month ratio, non-additive across periods | correct per month, but averaging it to a quarter/year rate weights a 50-account month equally with a 5,000-account one → wrong blended rate; a grand-total tie-out won't catch it | Latent / verify (→ Blocking if a rollup averages the monthly rates) | flag the measure non-additive; for a period rate, sum `lost` and `start` across the window and divide once |

## Verdict
- **Blocking:** 3 — established from the code + contract (#1 wrong unit, #4 wrong cohort grain, #3 missing timezone handling); must resolve before this feeds the board or gets defended (most fundamentally, it answers a different question than the contract).
- **Latent / verify:** 5 — real impact, but each hinges on a fact not in hand (#2 trials-in-`active`, #5 the magic IDs, #6 NULL `plan_code`, #7 the close rule, #9 the non-additive rate-rollup); each carries its discriminating check and becomes Blocking once confirmed.
- **Advisory:** 1.
- **Assumptions this review depends on:** trial marker field, fiscal-calendar definition, and the identity of the excluded account IDs all remain open (asked of the user; not assumed) — which is exactly why #2 is graded Latent / verify, not Blocking. Asserting Blocking on an unconfirmed schema fact is the over-blocking failure mode.
```

Note what the review does NOT do: it never rewrites the view, never writes the MRR rebuild, and never invents the trial flag or MRR column names to make a fix runnable. It locates, names, grades, and points — the user makes the change.
