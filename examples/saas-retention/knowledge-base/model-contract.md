# Model Contract: Retention Mart  (v1.0-draft, 2026-06-10)
_Phase: [Design]. Anchored to kpi-contract.md v1.0 (2026-05-22)._
_Open gates and [needs decision] forks are in open-questions.md._

---

## Business process / decision served
Monthly NRR and Gross Revenue Churn for the board readout, sliced by plan tier,
signup cohort, and region.  Locked metric definitions in `kpi-contract.md`; this
contract designs the structure those metrics compute against.  Consumers: board deck
(replacing the logo-churn vw_monthly_churn pull) and any downstream mart that
conforms to the same account and date dims.

---

## Target grain
**One row per account per calendar month-end.**
Fact type: **periodic snapshot.**

_Rationale:_ NRR is an "as-of month-end" balance measure.  A transaction grain forces
point-in-time MRR reconstruction on every query.  An account/month snapshot lets the
NRR query filter to a trailing-12 window and aggregate directly.  KPI contract pins
"account grain underneath"; subscription-level detail is available in the source
event log for diagnostics but is not the reporting grain.

---

## Sources + gated grain

| Source | Claimed grain | Keys / dup risk | Gate status |
|---|---|---|---|
| `billing_export_daily` | one row per (account_id, event_date, event_type) | (account_id, event_date, event_type) | **GATE — assumed per A10 check; design is conditional on A10 confirmation. If sub-event rows exist, ETL aggregation logic changes.** |
| `subscriptions` | one row per subscription (inferred from vw_monthly_churn SQL) | subscription_id; >1 sub per account possible | **GATE — not profiled; fan-out risk if account has multiple active subscriptions simultaneously. Must confirm before build.** |
| `accounts` | one row per account (assumed) | account_id; source system undocumented | Not profiled; source system unknown (estate-map gap). Duplicate account_ids would double-count MRR. |
| `crm_accounts_sync` | nightly Solidus sync (evidenced) | account_id | **[unverified edge per estate-map]** — does a job write CRM fields into `accounts`, or is this a runtime join? Until confirmed, `dim_account.segment` is unreliable. |

The two **GATE** rows are the blocking conditions.  The logical star below is correct
IF those grains are confirmed.  Do not begin dbt authoring until both are closed.

---

## Fork log

Every row is pinned, `[needs decision: owner]`, or "N/A because ___".
A silent skip is the bug this contract exists to prevent.

| Fork | Options | Pinned choice | Why it matters |
|---|---|---|---|
| `billing_export_daily` grain (gate) | one-row-per-(account, event_date, event_type) / sub-event rows | Assumed confirmed by A10 — **verify before build** | Sub-event rows fan out MRR sums; wrong grain = wrong NRR numerator |
| `subscriptions` grain (gate) | one-row-per-subscription / per-status-change-event | Assumed one-per-subscription — **not profiled** | Multi-row-per-subscription fans out account MRR on join |
| `accounts` grain | one-row-per-account | Assumed — source system undocumented | Duplicate accounts = double-counted MRR |
| Target fact grain | account/month · subscription/month | **account/month** | KPI contract: "account grain underneath." Sub grain needs rollup on every query; wrong grain forces rebuild. |
| Fact type | transaction · periodic snapshot · accumulating snapshot | **periodic snapshot** | NRR and gross churn are "as-of" balance metrics; transaction grain forces reconstruction on every query |
| MRR additivity | additive · semi-additive · non-additive | **semi-additive (not over time)** | Summing mrr_amount across months double-counts; per KPI contract. Sum across accounts and plans is valid. |
| Movement measures | pre-computed on fact · derived at query time | **pre-computed on fact** (recommended) | Board NRR query is simpler and faster; trade-off is ETL logic to derive period-over-period from billing events. See fork brief below. |
| `dim_account` SCD | type 1 overwrite · type 2 history rows | **type 2** | KPI contract hard requirement: "segment changes must not re-write historical NRR by segment." Non-negotiable. |
| `dim_plan` SCD | type 1 · type 2 | **[needs decision: Analytics + RevOps]** | If "NRR by plan tier" must show the plan the account held *at the time*, type 2. If current plan label is acceptable, type 1. |
| Win-backs / reactivations | rejoin original cohort · start as new customer | **[needs decision: RevOps — A3 may govern this]** | Changes the NRR denominator for returning accounts. KPI contract v1.0 left this open; A3 resolution may close it. |
| Reconciliation to Finance GL | bridge formula defined · undefined | **[needs decision: Finance + RevOps — A9 may govern this]** | Board WILL compare billing MRR to Finance GL; an unexplained gap sinks the number. KPI contract left this open. |
| Late cancellations | restate forever · 5-business-day close, then freeze | **5-business-day close, then freeze** | Per KPI contract v1.0; keeps a reported quarter stable. |
| Cohort identification | first_active_month_key attribute on dim_account · separate dim_cohort | **first_active_month_key on dim_account** (recommended) | Enables cohort slicing at query time without a separate table; trailing-12 window applied as filter in the NRR metric query |
| CRM segment on dim_account | load from accounts (trusting unverified CRM sync) · hold until edge confirmed | **[needs decision: confirm estate-map unverified edge first]** | Segment is a KPI dimension slice; wrong segment attribution silently breaks by-segment NRR |
| `account_status` | degenerate dim on fact · separate dim_status | **degenerate dim on fact** | Low cardinality (active / paused / churned), no descriptive attributes — fits on the fact; dim_status adds no value |
| Junk dimension | N/A | N/A — no low-cardinality flag cluster identified at this scope | — |
| Role-playing date dim | separate dims for snapshot_month vs first_active_month · aliases on one dim | **one conformed dim_date, role-played via two FK aliases** | Standard practice; one dim to maintain and conform with future marts |
| Surrogate vs natural keys | surrogates on dims · natural keys only | **surrogates** | Decouples from source key churn; required for type-2 implementation on dim_account |
| NULL / unknown FK members | −1 "unknown" member · NULL FK | **−1 unknown member on all dims** | NULL FKs break inner joins and silently drop rows from NRR aggregations |
| Late-arriving facts | hold · route to unknown member · backfill | **route to −1 unknown; backfill within 5-day close window** | Consistent with the late-cancellation close policy |
| Late-arriving dimensions | type-2 back-date · accept current-period drift | **accept drift for now; revisit if CRM sync proves unreliable** | No confirmed case of late dim arrivals yet; back-date logic adds complexity without a known trigger |

---

### Fork brief: movement measures — pre-computed vs query-time

**The fork:** expansion_mrr, contraction_mrr, and churned_mrr could live on the fact as pre-computed columns, or be derived at query time from period-over-period MRR differences.

**The stake if wrong:** pre-computed wrong = incorrect NRR everywhere it's used; query-time derivation = every NRR query carries window-function complexity and runs slower.

**Options:**
- *Pre-computed (recommended):* ETL reads billing_export_daily events within the period, classifies each as expansion / contraction / churn, and writes amounts to the fact. NRR query becomes a simple SUM. Cost: ETL is harder; event_type classification logic must match the KPI contract exactly.
- *Query-time derivation:* NRR query computes `LAG(mrr_amount)` across months per account and infers movement. Simpler ETL; more fragile query; harder to validate.

**Recommendation:** pre-compute. The KPI contract defines the classification precisely (expansion = MRR increase on a continuing account; contraction = MRR decrease; churn = full cancel). That logic belongs in the transformation layer once, not in every downstream query.

**Default if no decision:** pre-compute.

---

## Logical star

```
fct_account_month  (periodic snapshot)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
grain: one row per account per calendar month-end

Foreign keys:
  account_key          → dim_account (type 2; point-in-time segment, region)
  plan_key             → dim_plan    (SCD: [needs decision])
  snapshot_month_key   → dim_date    (role: the snapshot month)
  first_active_month_key → dim_date  (role: cohort anchor; ties each account
                                       to its first active month for cohort
                                       filtering — same dim, two roles)

Measures (see additivity table below):
  mrr_amount           semi-additive
  expansion_mrr        additive
  contraction_mrr      additive
  churned_mrr          additive
  seat_count           semi-additive  (include if available; same rule as MRR)

Degenerate dimension:
  account_status       (active / paused / churned — as of this month-end)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
dim_account  (type 2)
  account_key          surrogate PK
  account_id           natural key (from billing / accounts table)
  segment              [load only after crm_accounts_sync edge confirmed]
  region               [load only after crm_accounts_sync edge confirmed]
  plan_tier            (if not on dim_plan; clarify ownership)
  first_active_date    (for cohort slicing; also drives first_active_month_key on fact)
  effective_from       date
  effective_to         date (NULL = current)
  is_current           boolean

dim_plan  (SCD: [needs decision])
  plan_key             surrogate PK
  plan_id              natural key
  plan_name
  plan_tier
  billing_cadence      (monthly / annual)

dim_date  (static; role-played twice on the fact)
  date_key             surrogate PK
  calendar_date
  calendar_month       (YYYY-MM)
  fiscal_month
  fiscal_quarter
  fiscal_year          (US/Pacific, per KPI contract)
```

### Bus matrix

| Business process | dim_account | dim_plan | dim_date |
|---|---|---|---|
| Account MRR state — `fct_account_month` | ✓ (type 2) | ✓ | ✓ × 2 roles |
| Future: billing / invoicing mart | ✓ | ✓ | ✓ |
| Future: support desk / health mart | ✓ | — | ✓ |

`dim_account` and `dim_date` must be conformed across all three.
`dim_plan` should be conformed with billing if that mart is built.

---

## Measures + additivity

| Measure | Additivity | Rule |
|---|---|---|
| mrr_amount | semi-additive | Sum across accounts and plan; **never sum across months** — take month-end snapshot value |
| expansion_mrr | additive | Safe to sum across any dimension; it's a within-period event amount |
| contraction_mrr | additive | Same |
| churned_mrr | additive | Same |
| seat_count | semi-additive | Same rule as mrr_amount |
| NRR (derived metric) | non-additive ratio | Always compute from components: `(start_mrr + expansion − contraction − churn) / start_mrr`. Never sum NRR itself. |
| Gross churn rate (derived metric) | non-additive ratio | `(contraction_mrr + churned_mrr) / prior_month_mrr`. Never sum the rate. |

---

## Conformed dimensions + reconciliation

**dim_account:** the one conformed customer dim for all future marts. Its type-2
design is non-negotiable; any mart that overwrites it with type-1 breaks historical
NRR-by-segment attribution.

**dim_date:** standard conformed date dim. Role-played twice in this fact
(snapshot_month_key, first_active_month_key) via FK aliases — not two separate dims.

**Reconciliation to vw_monthly_churn:** `vw_monthly_churn` counts *logo* churn
(account count). This fact measures *MRR* churn. They will not and should not agree —
document this difference prominently in the board deck to prevent the board from
treating the two as comparable numbers.

**Reconciliation to Finance GL:** per KPI contract, the expected bridge is:
`GL revenue = cohort-retained MRR + new-logo MRR + one-time/services + billed-vs-recognized timing`.
Exact amounts are `[needs decision: Finance + RevOps]`. This must be signed off before
the board readout; an unexplained gap between this mart and Finance's deck sinks the number.

---

## Guardrails (what this model deliberately does NOT support)

- New-logo acquisition metrics — out of scope by KPI contract construction (NRR excludes new logos).
- Absolute revenue reporting — Finance GL scope; different grain and timing.
- Support ticket analysis — separate mart using tickets_weekly.
- PLG usage funnels — separate mart using usage_events.
- Sub-account billing line items — billing_export_daily event detail is the source for the ETL, but the fact is account/month. If sub-event drill-through becomes a requirement, add a transaction fact; do not widen this periodic snapshot.
- Trials and free accounts — excluded from all MRR measures per KPI contract.
- NRR as a native stored column — it is a derived metric computed from stored components; the metric definition lives in kpi-contract.md.

---

## Open questions (blocking before build)

See `open-questions.md` for the full list with owners.  Blocking gates first:

1. **A10 result — billing_export_daily grain:** Was A10 run? Is grain confirmed as
   one-row-per-(account_id, event_date, event_type)? If sub-event duplicates exist,
   the ETL aggregation logic must be redesigned before the fact is structured.
2. **subscriptions grain:** One-row-per-subscription or per-status-change event?
   Fan-out risk if multiple rows per subscription exist.
3. **A3 (open with RevOps):** Resolution expected to govern the win-backs /
   reactivation fork. Until closed, cohort membership rules are incomplete.
4. **A9 (open with RevOps):** Resolution expected to govern the Finance GL
   reconciliation bridge. Until closed, the board deck comparison is unvalidated.
5. **crm_accounts_sync → accounts edge (unverified):** Confirm before loading
   segment or region onto dim_account.
6. **dim_plan SCD type:** Analytics + RevOps to decide whether point-in-time plan
   attribution is required.
7. **accounts source system:** Which system owns and populates accounts? Are
   duplicate account_ids possible? (estate-map gap — DBA or engineering to confirm.)

---

## Version + effective date
v1.0-draft · 2026-06-10 · Marcus Okafor (analyst)
Status: DESIGN LOCKED on all pinned forks; build gates open until items 1–7 above close.
Feeds: `review-my-query` (build reviewed against this contract once dbt authored).
Consumes: `kpi-contract.md` v1.0, `estate-map.md` 2026-06-09, `assumption-register.md` 2026-06-08.
