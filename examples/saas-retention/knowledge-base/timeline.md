# Timeline  (append-only, newest at bottom)
_End of each session, append: what happened, decided, next, blocked. Drop external events with date + source._

## 2026-05-18  [Understand]
- happened: oriented on the inherited retention estate (read `vw_monthly_churn` and
  Dana's `metrics_notes.md` as text; no database touched). Stood up this KB.
- decided: classified as an inherited estate; do not trust the logo view as revenue retention.
- next: validate the real decision behind the "churn dashboard" before rebuilding.
- blocked / waiting on: nothing yet.
- note: Dana's handoff flags that the view and Finance retention "never line up";
  recorded as a data-quality caveat and an open question.

## 2026-05-20  [Define]
- happened: interrogated Priya's dashboard request; ran decision-backwards, the XY
  split, and the delta. Verdict reframe. Wrote `requirements-brief.md`.
- decided: build NRR + gross revenue churn + early-life churn by cohort, not logo
  churn plus a decorative curve. Updated `purpose.md` to the confirmed goal and closed
  the "what decision rides on this" open question.
- next: lock the metric definitions before any build.
- blocked / waiting on: whose NRR definition is authoritative, and how it reconciles
  to Finance (open for Finance + RevOps).

## 2026-05-22  [Define / Design]
- happened: pinned the metric definitions; walked the fork checklist; locked
  `kpi-contract.md` v1.0 (NRR + gross revenue churn).
- decided: billing MRR is the source of record; pinned base, window, grain,
  contraction, trials, timezone, and late-data handling.
- next: build the cohort model from the locked contract.
- blocked / waiting on: two `[needs decision]` forks open, the Finance reconciliation
  bridge and the win-back cohort rule.

## 2026-05-28  [Build / Validate]
- happened: reviewed the inherited `vw_monthly_churn` view (as text, not run) against
  the locked contract. Walked each pinned fork, then the failure-mode taxonomy. Wrote
  `query-review.md`: 8 findings, 4 Blocking.
- decided: retire the view as a board-number source; it implements neither contracted
  metric (it is logo churn, not MRR retention). Build NRR fresh from billing.
- next: build the NRR cohort model from the contract; resolve the cohort-grain bug
  before it ships.
- blocked / waiting on: the trial marker field, the grain of `subscriptions`, and the
  identity of the five excluded accounts (all open, asked of the owner).
- note: the review confirms at the code level why the view never lined up with Finance,
  finding #1, logos vs dollars. The forward reconciliation bridge stays a contract `[needs decision]`.

## 2026-06-01  [Validate]
- happened: rehearsed the board readout vs a data/method skeptic (ex-CFO). Harvested
  the locked contract and `query-review.md` as ammunition. Wrote `defense-sheet.md`.
- decided: not ready; hold the recommendation pending the Finance reconciliation and
  an early-life cohort cut.
- next: close the reconciliation [needs decision] with Finance + RevOps; build the
  cohort cut; rehearse again.
- blocked / waiting on: Finance + RevOps sign-off (blocking the 2026-06-10 board meeting).
- event: board meeting scheduled 2026-06-10 (per Priya's request).

## 2026-06-02  [Deliver]
- happened: composed the board findings brief from the KB (contract, query-review,
  defense-sheet, open-questions). Wrote `findings-brief.md`.
- decided: brief the board honestly, lead with the "not yet" verdict, present NRR 108%
  as directional (not reconciled), and keep the two open items visible rather than
  smoothing them into a confident story.
- next: close the Finance reconciliation and build the early-life cohort cut, then update
  the brief and re-rehearse before the 2026-06-10 meeting.
- blocked / waiting on: Finance + RevOps reconciliation; the early-life cohort cut.

## 2026-06-05  [Operate]
- happened: the internal exec dashboard (still fed by the board-retired `vw_monthly_churn`)
  printed ~11% monthly logo churn vs the usual ~4%; an exec asked if churn is spiking.
  Triaged it against the KB (`query-review.md`, `kpi-contract.md`, `data-quality.md`) and
  wrote `triage.md`.
- decided: working call is a measurement artifact, not a real trend; gave a calibrated
  holding line and did NOT hand the exec a confirmed cause. The code suspects are the
  defects `query-review.md` already graded (the grain bug, trials), now the first place to look.
- next: decompose `accounts_start` vs `accounts_lost` (this month vs a normal month) to
  confirm the grain bug as the cause; the real fix is the NRR rebuild, not a patch.
- blocked / waiting on: the one decomposition check (user to run). Nothing computed here.
- note: this Operate-phase spike is the 2026-05-28 retire decision proving itself in
  production. No new open question; the defects are already open.

```markdown
## 2026-06-04 — worth-knowing session 1 (Priya Sharma, VP CS)

- **Trigger:** Priya asked "what can our data tell us?" with 6 months to annual budget decision.
- **Outcome:** Question Charter created with 6 candidates (5 Q1–Q5 from stated goals; Q6 the mandatory unasked testing the acquisition-vs-onboarding framing).
- **Key constraint surfaced:** Four of six candidates are blocked on unverified cross-source join keys (new `open-questions.md` entry added). Q5 (ROI quantification) remains blocked on NRR definition and Finance reconciliation (pre-existing open question).
- **Conviction logged:** Priya "convinced onboarding is our problem" — Q6 chartered as the disconfirming test; no finding delivered.
- **Elicitation gap:** Shorter-cadence CS allocation decisions not yet explored.
- **Next steps:** (1) Join-key check with RevOps (gates Q2/Q3/Q4/Q6). (2) `kpi-contract` to lock NRR definition and GL reconciliation (gates Q5). (3) Priya accepts/declines/reshapes candidates → charter updated in place on re-fire.
```


## 2026-06-08 — audit-my-assumptions: billing_export_daily register created (10 rows, 4 gating TRUNKs incl. A9: does the extract share Finance's source? — the Act-I reconciliation gap would re-inherit into the mart). Verdict: do not build past A3/A9 without owners. by: Marcus
# Timeline  [Understand]
_Append-only. Newest on top._

## 2026-06-09 — Estate map drawn: retention reporting data flow
by: Marcus Okafor (request); drawn from landscape.md + vw_monthly_churn.sql + Marcus verbal 2026-06-09
Result: 14 nodes · 9 evidenced edges · 1 unverified edge · 5 gaps logged to open-questions.md · 4 fabricated edges refused logged to catches.md
Next: open-questions.md gaps → groundwork interviews; Board Deck vs Finance Quarterly Deck definition reconciliation → model-contract
## 2026-06-05 — Q1 exploration opened

- **Event:** Exploration Log opened for Q1 (first-90-day churn disproportionality).
- **By:** Marcus Okafor (analyst). Routed from question charter by Priya.
- **Status:** Pre-registered; no data examined. 6 cuts written; awaiting paste-back.
- **Log:** `exploration-log.md`
- **Blocks on:** D2 and D3 definition confirmations (Cuts 2a, 2b) before hypothesis cuts run.

## 2026-06-12 — Q1 results graded (explore-my-data session 2)
- H1 (first-90-day disproportionality): +17.2pp over flat-hazard on n=327 — **Exploratory — found**; hold-out Check 1 pre-registered (sub-cohort caveat stated; gold-standard prospective check pinned for 2026-09). H2 (Starter tier): grade PENDING — per-tier flat-hazard columns missing from paste-back. H3 (vintage): **dead end, recorded**.
- Charter sync: Q1 status → Exploratory-found, awaiting hold-out. by: Marcus

## 2026-06-10 — model-contract: retention mart designed
- fct_account_month (one row per account per month-end) + dim_account / dim_plan_tier / dim_month; source grains GATED on A10 + subscriptions profile; dim_account.segment marked unreliable until the estate map's [unverified] CRM edge is confirmed. Build blocked past A3/A9 per the register. by: Marcus

## 2026-06-15 — change-impact: billing_export_v2 blast radius — NOT safe to ship; 3 SILENT-DRIFTs (event_type rename = the board-grade one: movement filters return 0 rows, NRR=100%), 2 UNKNOWNs, 6 pre-flight checks written; post-change tie-out routed to prove-my-parity (strata: tier x cohort x region). by: Marcus
- **2026-06-24** — NRR parity proof completed: v1 vs v2, Jul-2025..Jun-2026. Verdict: **PARITY**. Nine in-scope strata all within ±0.50 pp; offsetting_error=False; residuals fully classified (0.00 pp unexplained). `by: Marcus Okafor / BI assistant`. See parity-proof.md.

## 2026-07-06 — audit-my-experiment: onboarding pilot gated
- SRM clean (χ² p≈.81). BLOCKING: 7 weekly peeks on a 10-week plan — nominal p=.049 does not survive sequential correction; "the write-up cannot proceed." Latent: 30-day activation is a PROXY — 90-day churn (the decision metric) unmeasured. What clears it: run to week 10 + pre-registered churn guardrail + MME pinned to CS-team breakeven. by: Marcus

## 2026-07-08 — audit-my-forecast: Finance churn forecast — intervals BLOCKING
- Point forecast beats naive 2.1× (pass). Interval coverage 6/12=50% vs 80% nominal — all misses are upper-bound breaches (the understaffing side). Plan may use the point path; nobody plans against the bands until recalibrated. by: Marcus

## 2026-07-13 — review-my-dashboard: do not ship as-is (4 Blocking / 1 Latent / 3 Advisory)
- The summed-distinct "YTD" card; "all customers" title over a Starter-excluded default; "live" over a Monday extract; "(validated)" on the gated pilot — removed, claim routed back to experiment-audit. by: Marcus

## 2026-07-17 — status-truth: steering status AMBER, pressure recorded
- "Keep it green" recorded, not obeyed. Greens with criteria (parity, mart design); ambers with owners (pilot gate, forecast intervals, A3/A9); the September budget narrative protected by honesty, not color. by: Marcus

## 2026-07-20 — kb-reconcile: pre-readout audit of the whole record
- 3 Blocking drifts: the NRR/Finance open question still labeled "blocking the 2026-06-10 meeting" (40 days past, outcome unrecorded); estate-map predates billing_export_v2 by five weeks (re-run routed); dashboard "do not ship" absent from the exec-facing ledger. Parity verdict standing but re-audit fires at Jul close. Advisory: record the June board outcome before the August deck. by: Marcus
