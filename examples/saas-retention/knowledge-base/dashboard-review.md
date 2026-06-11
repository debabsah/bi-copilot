# Dashboard Review — Retention Dashboard, all pages, as-of 2026-07-13  [Validate]
_Reviewed 2026-07-13, by BI assistant. Serves: exec team, Thursday board/leadership view.
Reviewed from: six measure definitions as text, KPI contract v1.0 (NRR only).
**Coverage boundary:** visual-level filter wiring and cross-filter interactions not verified
(BI tool not opened); RLS rules not provided — unreviewable; mart logic in `fct_account_month`
(whether `current_mrr` correctly encodes expansion/contraction/churn) is review-my-query
territory, not reviewed here; activation-lift statistical methodology is unreviewable from a
bar-chart description — route to `audit-my-experiment`._

## Verdict
**Do not ship as-is** — 4 Blocking · 1 Latent · 3 Advisory.
Most urgent room-facing risk: "NRR by cohort" silently excludes Starter at the default state
while the title reads "all customers" — the exec team will read a filtered view as
company-wide NRR.

## Findings register
| # | Layer | Finding | Grade | Evidence | Fix direction |
|---|---|---|---|---|---|
| 1 | Semantic | **Card 2 'Active accounts YTD'** — measure is `SUM` of monthly distinct-active-account counts. Distinct counts are non-additive: summing monthly `DISTINCTCOUNT` values double-counts any account active in more than one month. An account active for 7 months YTD appears 7 times. The card shows a person-month total, not a YTD distinct account count. | **Blocking** | "sum over months of monthly distinct active account count" | Recompute at YTD grain: `DISTINCTCOUNT(account_id)` over the full YTD date range. Do not sum monthly values. |
| 2 | State + Presentation | **Chart 'NRR by cohort'** — default filter: `plan_tier IN (Growth, Enterprise)`. Starter excluded because "it makes the chart noisy." Title reads "NRR by cohort — all customers." The default is a silent population claim; the title makes that population explicit and wrong. The NRR contract explicitly warns that hiding cohorts hides early-life churn — the decision's whole point. | **Blocking** | Default filter text; title text "all customers"; contract: "Misleading: blending all cohorts into one company-wide NRR hides early-life churn" | Either retitle to "NRR by cohort — Growth + Enterprise" with a visible filter callout, or change the default to include all tiers. Do not ship with a "all customers" title over a Starter-excluded view. |
| 3 | State | **Dashboard subtitle "live"** — data source is a weekly extract refreshed Mondays. On Thursday, the extract is ≥3 days old; up to 6 days stale in the worst case. "Live" implies real-time or near-real-time; it is materially false here. | **Blocking** | "weekly extract refreshed Mondays"; subtitle text "live" | Replace subtitle with "As of [last Monday's date]" or "Weekly refresh — last updated [date]." |
| 4 | Presentation | **Chart 'Activation lift from onboarding pilot'** title: "Onboarding pilot: +6.5pp activation (validated)." "(validated)" is a causal/methodological claim. A bar chart showing 28.6% vs 35.1% shows a difference; it cannot show that the difference is causally validated. Future viewers — and anyone who screenshots this — will read it as unconditionally proven. | **Blocking** | Title text "(validated)"; visual described as a two-bar chart | Remove "(validated)" from the title now. Route the methodology claim to `audit-my-experiment` before any form of the validated label is restored. |
| 5 | Semantic | **Ratio measures (NRR, Gross churn %) are non-additive.** If any future view adds a cross-cohort total or roll-up that sums or averages per-cohort NRR values rather than recomputing the ratio at aggregate grain, the total will be wrong. Not observed in current definitions but structurally at risk when the dashboard is extended (e.g., a "Total" row added to the cohort chart). | Latent | Ratio measure type; absence of described total does not rule one out | When adding any total/subtotal to a ratio measure, recompute the ratio at aggregate grain — never aggregate the ratio values themselves. |
| 6 | Contract | **'Gross churn %'** stated as "contract formula, monthly grain" — verify the implemented formula against kpi-contract.md v1.0's gross-revenue-churn clause line by line before ship; "matches the contract" is a claim, not a check. | Advisory | kpi-contract.md v1.0 (gross revenue churn clause) | Walk the formula against the locked clause; any mismatch routes to `review-my-query`. | |
| 7 | Contract | **Card 2 'Active accounts YTD'** has no locked KPI contract. Once the additivity error (finding #1) is fixed, the definition still floats. | Advisory | KB: no contract entry for Active Accounts | Stub a KPI contract for Active Accounts YTD. |
| 8 | Contract | **NRR contract has an open unresolved decision:** "Finance + RevOps to confirm the exact bridge [to GL revenue] and sign off on which retention number the board sees." If an exec asks for GL reconciliation on Thursday, no bridge is documented. | Advisory | KPI contract v1.0 caveats / Reconciliation section | Resolve the bridge decision with Finance + RevOps before the board meeting; document in the contract. |

## Contract conformance
| Displayed metric | Contract | Conforms? |
|---|---|---|
| NRR (trailing 12) | KPI Contract v1.0, 2026-05-22 | Yes — formula structure matches; mart logic out of scope for this review |
| Active accounts YTD | NONE — finding #7 | No — non-additive (finding #1); no contract |
| Gross churn % | NONE — finding #6 | Unverifiable — no locked contract |
| NRR by cohort | KPI Contract v1.0, 2026-05-22 | No — default filter violates "all customers" title claim (finding #2) |
| Activation lift (onboarding pilot) | NONE | No — title claim "(validated)" unsupported by visual (finding #4) |

## What passed
- **Card 1 'NRR (trailing 12)'** — formula `sum(current_mrr)/sum(base_mrr)` over in-scope cohorts matches the contract formula and is computed at aggregate grain. Passes as described; mart-level correctness is out of scope here.
- **Card 3 'Gross churn %'** — described as using the contract formula at monthly grain; no additivity failure in the scalar view. Structurally plausible; blocked only by the missing contract, not the measure definition itself.
- **NRR by cohort chart, per-cohort bars** — each cohort's NRR is its own correctly computed ratio. The per-cohort bars are fine; only the population claim in the title and the default filter state fail.
