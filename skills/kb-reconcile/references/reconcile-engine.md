# reconcile-engine — the drift taxonomy, the paste-back protocol, the honesty constraint

Load this when running the loop. It is the engine behind the SKILL.md body: how to name each kind of drift, how to write a check the user runs, and the mechanical rule that keeps the report honest.

## 1. The drift taxonomy (the engine)

Every finding is one of these. Name it, run its read-only check, take its action. The first seven are catchable read-only (against the KB and the code/definitions on hand); the last row is NOT — only a paste-back re-derivation reaches it.

| Drift | What it is | Read-only check | If found |
|---|---|---|---|
| Contradiction | two files disagree on a status/decision/number | cross-file compare; cite both `file:line` | flag; `[needs decision]` if no precedence |
| Partial-update | a change landed in some files, not the dependents | headline-vs-source-of-record compare (e.g. brief says closed, contract says `[needs decision]`) | flag the un-updated files; suggest propagation |
| Decision-violated | a later artifact breaks a logged decision | check artifacts against `decisions.md` | flag; Blocking if it ships a wrong number |
| Qualifier-erosion | a directional / `[needs decision]` claim re-cited bare | trace each cited status back to its origin | restore the qualifier |
| Status-rot | open list lists closed items or omits real ones | reconcile `open-questions.md` against the timeline + decisions | correct the status |
| Expired-verdict | a carried/consumed verdict whose `Re-audit when:` condition has since been met, or whose evidence post-dates it | compare each carried verdict's date + re-audit condition against the timeline and later artifacts | flag stale; recommend re-audit before the verdict is used again |
| Map-staleness | an `estate-map.md` whose derived-from set predates changes to those files (or new topology in the record) | compare the map's derived-from dates against the current files + timeline | flag stale; recommend re-running map-my-estate |
| Term-drift | a term the contracts pin precisely (or pin in two variants) used unqualified or inconsistently across artifacts — a brief saying "churn" where the contract distinguishes logo vs revenue churn; "active customer" used against its house-vocabulary meaning | collect the pinned vocabulary (kpi-contracts, house vocabulary, model-contract conformed terms); flag each artifact using a defined term in a way the definition doesn't support or doesn't disambiguate | flag with both readings; recommend the artifact qualify the term (or kpi-contract pin the missing variant) — two people agreeing while meaning different numbers is the failure this catches |
| Broken-provenance | a claim cites a source that is absent/renamed | resolve every citation | mark `unverified`; flag the dangling ref |
| Unsourced-number | a quantitative claim with no checkable source on hand | look for the cited artifact in the tree | mark `unverified`; write the paste-back check |
| Staleness / garbage-in / derivation-error | the KB is internally consistent but wrong vs the data | NOT read-only catchable | write the paste-back check (only re-derivation reaches it) |

The taxonomy derives from the KB failure-mode map: the read-only-catchable types (contradiction, decision-violated, qualifier-erosion, partial-update, status-rot, broken-provenance, unsourced-claim) are the ones an audit against the record and the code can reach; staleness-vs-source, garbage-in, and derivation-error need the run.

## 2. The paste-back protocol (the only path to "verified")

The tool never executes or connects. For any quantitative claim with no checkable source on hand, you do not bless it — you write the exact check the user runs against the source, and they paste the result back. The paste-back IS the run.

A written check has four parts:
1. **The claim** — restated with its `file:line`, e.g. "NRR = 108% this quarter (`findings-brief.md:11`)."
2. **The source to run against** — the system of record, named: the billing warehouse, the GL export, the dbt model, the specific table.
3. **The exact query/script** — runnable, not a sketch; or, where it must be manual, the precise numbered steps. Use the locked definition from `kpi-contract.md` so the check computes the contracted metric, not a lookalike.
4. **What confirms vs contradicts** — the decision rule, stated before the run: "confirms if the result is 108% +/- rounding; contradicts otherwise."

On the pasted result:
- Restate the result **verbatim**, label its source ("ran against billing MRR, 2026-Q2 cohort"), and mark the claim `verified` or `contradicted`.
- The run wins. If it contradicts the KB, the KB is stale/wrong — suggest the fix; do not split the difference.
- **Never relabel a user-run number as "verified by me."** You verified that the claim matches a run the user performed; say exactly that.
- A check the user has not yet run leaves the claim `unverified`, not "probably fine."

Keep the asks few and high-value: stakes-rank first (loop step 1), write checks only for the load-bearing unsourced numbers, and batch them so one paste-back round clears several.

## 3. The honesty constraint (mechanical — the load-bearing part)

This is the gate that consumption mode lacks. It is not a tone; it is a rule on the output:

- **Numbers come only from a run.** Reading bytes is never verification. A figure you read in the KB is `unverified` until a paste-back run confirms it, full stop.
- **No "clean / consistent / reconciles" without showing the checks THIS run.** The report must list what was checked. Every audited claim ends in exactly one state: `reconciled` / `drifted` / `unverified` / `[needs decision]` / `N-A` (with the reason). A silent skip is a failure of the audit, not a pass.
- **Coherence is not truth.** A uniformly wrong record reads as consistent. Internal consistency lets you clear contradictions; it never clears an unsourced number.

If you catch yourself writing "looks consistent" or "the 108% is supported" without a run behind it, stop — that is the exact failure the skill exists to prevent.

## 4. Worked example — the Meridian drifted KB

Run the loop on a KB whose headline docs were updated to "reconciliation closed / NRR board-ready" while the contract of record was not. (This is the `tests/fixtures/drifted-kb/` fixture; the baseline-vs-skill RED is recorded in `tests/BEHAVIORAL.md`.)

**Step 1 — scope by stake.** The load-bearing claim is the board headline: "NRR = 108%, reconciled to Finance, board-ready." A board readout rides on it. Audit it first.

**Step 2 — internal reconcile (the Blocking catch).** The narrative files say closed:
- `findings-brief.md:6` — "the headline NRR is now reconciled to Finance (closed 2026-06-03: the gap is definitional, not an error)."
- `findings-brief.md:34` — "NRR-to-Finance reconciliation | **Closed 2026-06-03** | ... signed off."
- `findings-brief.md:39` — "the **NRR number is board-ready**."

The source of record they cite says open:
- `kpi-contract.md:42` — "Reconciliation to Finance | known bridge / unknown | **[needs decision]**."
- `kpi-contract.md:19` — "**[needs decision: Finance + RevOps to confirm the exact bridge and sign off ...]**."

That is **partial-update drift**: the closure landed in the story files but never in the contract (or in `query-review.md`, which still flags the Finance-vs-NRR gap as unanswered). Cross-file compare, both `file:line` quoted. Because the files cannot tell you whether 06-03 was genuinely signed off (and only the contract left stale) or whether "closed" is aspirational, you cannot adjudicate — grade it **Blocking**, action `[needs decision: confirm the 06-03 sign-off, then propagate to kpi-contract.md or back out the brief edit]`.

**Step 3/4 — source reconcile + mark unverifiable.** The 108% cites `kpi-contract v1.0` as support, but a contract is a definition — it holds no measured value. There is no billing/GL/MRR artifact in the tree. So **108% is an unsourced-number**: mark it `unverified` and write the check —

> Claim: NRR = 108% this quarter, up from 102% a year ago (`findings-brief.md:11`).
> Source: billing MRR warehouse, account grain, trailing 12 months (the locked definition, `kpi-contract.md`).
> Run: compute start-of-period cohort billing MRR and end-of-period MRR for the same cohort (expansion minus contraction minus churn); NRR = end / start. Same query for the prior-year cohort for the 102%.
> Confirms if the result is 108% (+/- rounding); contradicts otherwise.

**Step 6/7 — grade + emit.** One Blocking partial-update drift, one unverified headline number, plus the standing open item (first-90-day cohort, on which the funding recommendation depends — already open in the KB, do not re-flag as drift). Write `reconcile.md` (your only output); in it, recommend the escalations as actions — the `open-questions.md` entry for the Blocking row, the `timeline.md` line, the cross-refs — for the user to apply. Edit none of the audited files.

**Graded reconcile.md excerpt:**

```markdown
## Drift (graded)
| # | Claim (file:line) | Drift type | Evidence | Grade | Suggested action |
|---|---|---|---|---|---|
| 1 | NRR reconciliation "closed 2026-06-03 / board-ready" (findings-brief.md:6,34,39) | partial-update | kpi-contract.md:19,42 still "[needs decision]"; query-review.md still flags the gap | Blocking | confirm 06-03 sign-off, then propagate the closure to kpi-contract.md, or back out the brief edit -- [needs decision: which is true] |

## Unverified (no checkable source on hand) -- run and paste back
- NRR = 108% (findings-brief.md:11): run the cohort billing-MRR NRR query above against the billing warehouse; confirms if 108%, contradicts otherwise. No GL/billing artifact is in the tree, so this cannot be checked read-only.

## Verdict
The board headline does not hold on the files present: its reconciliation status contradicts the contract it cites (Blocking), and the 108% has no source here (unverified). Nothing above was computed by reading; the number is unverified pending the paste-back run.
```

The difference from the consumption baseline is the mode-switch: the baseline read the same files and handed over "108%, board-ready"; the audit assumed each claim wrong until it reconciled, found the contract contradicting its own headline, and refused to bless a number with no run behind it.
