# Exploration Log — Q1: First-90-day churn disproportionality  [Understand]

_Opened 2026-06-05 by Marcus Okafor (analyst). Updated 2026-06-12 (grades + confirmation checks)._
_Charter candidate: Q1._
_Decision it serves: Fund-onboarding decision (exec team, annual, ~December 2026)._
_Population: All subscriptions with start_date ≥ 2023-01-01._
_Window: 2023-01 through present._
_Grain: One row per subscription period; MRR as recorded on the subscription row at churn._
_Finding-bar: Gap ≥ 10pp (Gate 2 confirmed by Priya 2026-06-12, before Cut 3 was run)._
_Read-only: cuts written here; Marcus runs and pastes results back. Nothing computed in this log._

---

## Gates

**Gate 1 — do NOT touch `vw_monthly_churn`.** KB `query-review.md` Blocking #4.

**Gate 2 — CONFIRMED.** THRESHOLD for H1: **10pp**, confirmed by Priya before Cut 3 was run.

**Gate 3 — CONFIRMED.**
- D2 (exclude < 7 days): 0.4% of churned MRR (< 2% threshold) → **locked.**
- D3 (each subscription row independent): 1.1% of rows with 2+ subscriptions (< 5% threshold) → **locked.**

---

## Hypothesis ledger

| # | Question / hypothesis | Registered | Status |
|---|---|---|---|
| H1 | First-90-day churned MRR exceeds flat-hazard benchmark by ≥ 10pp | **pre** (2026-06-05) | **Exploratory — found** (2026-06-12) |
| H2 | Disproportionality concentrated in ≥ 1 plan tier | **pre** (2026-06-05) | **Pending** — per-tier flat_hazard column missing from paste |
| H3 | Disproportionality concentrated in ≥ 1 cohort vintage | **pre** (2026-06-05) | **Dead end** (2026-06-12) |
| D1 | Metric: MRR churn | **pre** — locked by `kpi-contract` v1.0 | locked |
| D2 | Exclude lifetime < 7 days | **pre** | **locked** |
| D3 | Each subscription row independent | **pre** | **locked** |

---

## Cut log

**5 cuts examined** (Cuts 1–5; Cut 6 pending). **3 hypothesis cuts** (Cuts 3–5).
At α ≈ .05, **≈ 0.15 false hits expected** across 3 hypothesis cuts.

| # | Cut | Type | Result summary |
|---|---|---|---|
| 1 | Shape check | Setup | 2,114 rows; 388 churned; MRR sane, no negatives; 61 rows lifetime < 7 days. Plan tiers: Starter / Growth / Enterprise, no NULLs. |
| 2a | Trial scope (D2) | Setup | 61 short-lifetime rows = 0.4% of churned MRR. D2 default holds; locked. |
| 2b | Win-back scope (D3) | Setup | 23 re-subscribed accounts = 1.1% of rows. D3 default holds; locked. |
| 3 | Overall first-90-day vs flat-hazard (H1) | Hypothesis | actual = 31.4% ($412k / $1.31M), flat_hazard = 14.2%, **gap = +17.2pp**, n = 327 churned subs after D2. H1 threshold met. |
| 4 | First-90-day by plan_tier (H2) | Hypothesis | Starter 58% / $239k / n=201; Growth 29% / $120k / n=97; Enterprise 13% / $53k / n=29. "Starter = 31% of TOTAL MRR base." **Per-tier flat_hazard and total_churned_mrr columns missing — formal grade pending.** |
| 5 | First-90-day by cohort vintage (H3) | Hypothesis | 2024H2 +2pp vs other vintages; within noise on available bases. H3 dead end. |
| 6 | Cross-tab: plan_tier × cohort vintage | Hypothesis (interaction) | **Not yet run.** |

---

## Findings

| Finding | Grade | Basis | Confirmation path |
|---|---|---|---|
| **H1:** Overall first-90-day churned MRR disproportionate. Actual 31.4% vs flat-hazard 14.2%; gap +17.2pp on $1.31M / n=327. Pre-registered threshold met by +7.2pp. | **Exploratory — found** | Pre-registered question. 3 hypothesis cuts; ≈ 0.15 false hits expected — magnitude makes noise alone unlikely, but label stands until hold-out. | **Check 1** (2025-vintage sub-cohort; see below) |
| **H2:** Starter overrepresented in early churn. Starter = 58% of first-90-day MRR vs 31% of total churned MRR base — directionally large. Cannot formally grade without per-tier flat_hazard. Note: Enterprise n=29 (at the n<30 floor — do not headline regardless of gap). | **Pending** | Per-tier flat_hazard column needed. Once provided, grade will be post-hoc (pattern was visible in paste before grading) and labeled accordingly. | Requires full Cut 4 output; then **Check 2** (pre-specified before it is run). |
| **H3:** No vintage concentration. 2024H2 +2pp — well below 10pp threshold, within noise. | **Dead end** | Recorded. Do not re-examine by looking for a vintage where a tier effect holds — that is post-hoc dredging. Cut 6 tests the interaction only, not H3 again. | None. Record and move on. |

Grades: **Exploratory — found** · **Robust pattern** · **Dead end** · **Confirmed** (hold-out only).
Nothing is Confirmed. Re-running these cuts does not confirm anything.

---

## Confirmation checks

### Check 1 — H1 hold-out (pre-specified 2026-06-12, before it is run)

**Pre-registered threshold:** gap ≥ 10pp on ≥ 30 churned subs.

**Confirmation cohort:** 2025-vintage starters (`start_date` 2025-01-01 – 2025-12-31).

**Limitation — state explicitly:** the 2025 vintage was included in the generating data (Cut 3). This is a sub-cohort check, not a truly unseen hold-out. Grade on paste-back: gap ≥ 10pp and n ≥ 30 → H1 moves to **Confirmed** (sub-cohort caveat noted in the brief); gap < 10pp or n < 30 → remains Exploratory — found.

```sql
WITH churned AS (
    SELECT
        mrr_amount,
        (end_date::date - start_date::date) AS lifetime_days
    FROM subscriptions
    WHERE start_date >= '2025-01-01'
      AND start_date <= '2025-12-31'
      AND end_date IS NOT NULL
      AND (end_date::date - start_date::date) >= 7
)
SELECT
    COUNT(*)                                                        AS n_churned_subs,
    ROUND(SUM(mrr_amount), 0)                                       AS total_churned_mrr,
    ROUND(SUM(CASE WHEN lifetime_days <= 90
                   THEN mrr_amount ELSE 0 END), 0)                  AS first_90d_churned_mrr,
    ROUND(
        SUM(CASE WHEN lifetime_days <= 90 THEN mrr_amount ELSE 0 END)
        * 100.0 / NULLIF(SUM(mrr_amount), 0),
    1)                                                              AS first_90d_pct_actual,
    ROUND(
        SUM(
            LEAST(90.0, lifetime_days::float)
            / NULLIF(lifetime_days::float, 0)
            * mrr_amount
        )
        * 100.0 / NULLIF(SUM(mrr_amount), 0),
    1)                                                              AS first_90d_pct_flat_hazard
FROM churned;
```

**Gold-standard prospective check (September 2026):** Re-run the identical Check 1 query restricted to `start_date >= '2026-06-12'` once 90 days of churn accumulate on new cohorts. Pre-registered threshold: same — gap ≥ 10pp on ≥ 30 churned subs. This is the only truly unseen hold-out.

---

### Check 2 — H2 (tier) hold-out

**Not yet writeable.** Requires:
1. Full Cut 4 output: `plan_tier`, `total_churned_mrr`, `first_90d_pct_actual`, `first_90d_pct_flat_hazard` per tier.
2. Formal post-hoc grade on the generating data.

Once pasted, the confirmation check will pre-specify a tier-level threshold and hold-out cohort before it is run.

---

### Cut 6 — still to run

Pre-registered; run when ready. Reading rule for the cross-tab: **state n_churned_subs for every cell before reporting any percentage; suppress or flag cells with n < 30.** Do not use Cut 6 to re-examine H3 (dead end); it tests the plan_tier × vintage interaction only.

---

## Routing

| Condition | Route |
|---|---|
| Check 1 paste-back gap ≥ 10pp, n ≥ 30 | H1 Confirmed → `brief-my-findings` |
| H2 graded + Check 2 confirmed | H2 Confirmed → `brief-my-findings` |
| Any "onboarding investment causes early churn reduction" claim | `audit-my-experiment` — observational cuts cannot carry causation |
| A number looks wrong in Cut 4 or Cut 6 output | `triage-my-number` |
| Tier definition or flat-hazard computation disputed | `kpi-contract` |

**Charter sync:** Q1 — Exploratory — found (H1). Record outcome in `timeline.md` once confirmed or dead-ended; `worth-knowing` syncs from there.
```

---

Here's the read on each item:

**Definitions: both locked.** D2 (trials) = 0.4% of churned MRR, well under the 2% wire. D3 (win-backs) = 1.1% of accounts, well under 5%. Proceed was correct.

**H1: Exploratory — found.** Gap of +17.2pp against a pre-registered 10pp bar, on a $1.31M / 327-sub base. Three hypothesis cuts examined; ≈ 0.15 false hits expected — the magnitude makes noise alone a poor explanation, but the label holds until Check 1 comes back. Check 1 (2025-vintage query above) is pre-specified with the same 10pp / n≥30 bar. Note the caveat: 2025 data was in the generating query, so this is a sub-cohort check, not a clean hold-out. The gold-standard prospective check is September 2026 cohorts.

**H2: Can't formally grade yet.** The paste gave the composition of first-90-day MRR (58% / 29% / 13%), not the within-tier first_90d_pct_actual vs flat_hazard gap the Cut 4 query was designed to return. The directional picture is suggestive — Starter is 58% of first-90-day MRR but 31% of total churned MRR — but the formal gap requires the `first_90d_pct_flat_hazard` and `total_churned_mrr` columns per tier. Enterprise n=29 is at the n<30 floor regardless; don't headline it even if the gap is large. **Paste the full Cut 4 output and I'll grade H2 and write Check 2 before it's run.**

