# Assumption Register — Retention Mart from `billing_export_daily`  [Audit]
_2026-06-08. Auditor: Marcus Okafor. Sources audited: `billing_export_daily` (Dana's
nightly billing extract, unreviewed since Dana left).
The build does not proceed on an unvalidated TRUNK row._

## Sources & their authority
- `billing_export_daily` — authoritative for what it exports; NOT for whether its scope,
  definitions, or grain are correct for the retention mart.
- Anchor hierarchy available: export proc code (if reachable) > this export > `vw_monthly_churn`
  (derivative — it reads downstream of or in parallel with the export; not a validation anchor).
- Related KB: `data-quality.md` documents four open issues on `vw_monthly_churn`; unknown
  whether those roots reach into the export. `query-review.md` has 4 Blocking code-level
  findings on the view. Neither substitutes for auditing the extract directly.

---

## Register

| # | Assumption (cite) | Blast radius | Settled by | Status | Evidence / check |
|---|---|---|---|---|---|
| A1 | One `account_id` = one subscribing customer — no parent/child hierarchy, no merge artifacts, no re-sign reuse of the same ID | TRUNK — identity | Verifiable + Decision | ASSUMPTION | `SELECT account_id, COUNT(*) FROM billing_export_daily WHERE event_type='new' GROUP BY account_id HAVING COUNT(*)>1` — any account with >1 new event and no intervening cancel breaks identity. Also ask RevOps: on re-sign, is the same `account_id` reused or is a fresh one issued? |
| A2 | `mrr_amount` is the MRR level (not a delta) at event time, denominated in USD cents or whole dollars, net of discounts, excluding tax | TRUNK — unit | Verifiable + Decision | ASSUMPTION | `SELECT MIN(mrr_amount), MAX(mrr_amount), PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY mrr_amount), COUNT(*) WHERE mrr_amount < 0` — median in cents range (e.g. 15 000 for a $150 plan) = cents denomination; large negatives = delta encoding. Ask RevOps: on a downgrade row, does `mrr_amount` carry the new level, the old level, or the delta? If delta, the MRR spine of the entire mart is wrong. |
| A3 | `event_date` is the effective date (when the event takes business effect) not the booking/processing date; for a cancel booked 2026-05-01 effective 2026-05-31, `event_date = 2026-05-31` | TRUNK — period basis | Decision | **NEEDS-DECISION** | Ask billing system owner / RevOps: *"For a cancel booked today effective end-of-month, what value does `event_date` carry?"* A 30-day systematic shift cascades through every NRR cohort window. Named owner: RevOps. |
| A4 | The export is a full-history snapshot (every event since account inception), not a delta (events since last run); the retention mart needs day-one cohort history | TRUNK — population completeness | Verifiable | ASSUMPTION | `SELECT MIN(event_date), COUNT(*) FROM billing_export_daily` — if `MIN(event_date)` is suspiciously recent (e.g., the date Dana set up the job), the export is delta-only and full history does not exist here. Also check whether row count grows monotonically across nightly files or stays stable (full snapshot replaced each night). |
| A5 | Trials are excluded from the export, or are unambiguously flagged by `plan_tier` so they can be filtered | TRUNK — population | Verifiable + Decision | ASSUMPTION | Dana flagged this as open for `vw_monthly_churn` (see `data-quality.md`); unknown whether trials enter the export upstream of the view. `SELECT DISTINCT plan_tier FROM billing_export_daily` — flag any value that looks like a trial tier. Ask Priya (VP Customer Success): are trials ever created in the billing system before conversion? If yes, every active-account count and every churn rate is inflated before a query is written. |
| A6 | `event_type` is exhaustive: {new, upgrade, downgrade, cancel} covers every state transition — no undocumented values (reactivation, suspension, pause, trial_convert, write-off, etc.) | TRUNK — event taxonomy | Verifiable | ASSUMPTION | `SELECT DISTINCT event_type, COUNT(*) FROM billing_export_daily GROUP BY event_type` — any value outside the documented four is an undocumented state. A reactivation misread as "new" double-counts tenure; a missing "suspension" silently extends an account's active streak. |
| A7 | A downgrade to $0 MRR is recorded as `event_type = 'cancel'`, not as `event_type = 'downgrade'` with `mrr_amount = 0` | TRUNK — event taxonomy | Verifiable | ASSUMPTION | `SELECT COUNT(*) FROM billing_export_daily WHERE event_type='downgrade' AND mrr_amount=0` — if non-zero, cancel count understates true churn and $0 downgrade rows survive indefinitely in the "active" population. |
| A8 | The hardcoded `NOT IN (...)` exclusion list in `vw_monthly_churn` lives in the view (post-export) and is NOT applied upstream inside the export proc; `billing_export_daily` contains all accounts unfiltered | TRUNK — population | Verifiable | ASSUMPTION | Dana inherited the list and never examined it (see `inputs/metrics_notes.md`). If the exclusion is baked into the export proc rather than the view, the mart inherits silent drops. Check the export proc code; compare distinct account counts in the extract vs the view's universe for the same period. |
| A9 | `billing_export_daily` draws from the same upstream billing system source that Finance uses for their quarterly NRR/retention deck | TRUNK — Finance alignment | Decision | **NEEDS-DECISION** | `data-quality.md`: the churn view and Finance's deck have never reconciled; nobody traced why. If the extract is a different cut of the billing system (or a different system entirely), the mart will also not reconcile to Finance — the same unresolved gap, re-inherited at larger scale. Ask: *"What tables or system does Finance pull from for quarterly NRR, and does `billing_export_daily` read the same source?"* Named owner: RevOps or Finance BI. |
| A10 | One row per event per account; `mrr_amount` is the account-level figure, not a per-seat or per-line-item figure; no fan-out from multi-product accounts | TRUNK — grain | Verifiable | ASSUMPTION | `SELECT account_id, event_date, event_type, COUNT(*), SUM(mrr_amount) FROM billing_export_daily GROUP BY account_id, event_date, event_type HAVING COUNT(*)>1` — any duplicates mean the grain is sub-account and every SUM fans out. |
| A11 | `start_date` is the subscription start date; `end_date` is NULL for active accounts and is the effective service-end date (not the billing-period-end) for terminated accounts | TRUNK — period basis | Verifiable + Decision | ASSUMPTION | `SELECT event_date, end_date, DATEDIFF(end_date, event_date) FROM billing_export_daily WHERE event_type='cancel' LIMIT 100` — if `end_date` always equals `event_date` on cancel rows, they may be the same field. If `end_date > event_date`, it is the service-end (useful for proration). Ask RevOps what each date represents. |
| A12 | `exported_at` lag is < 24 h; events are not systematically backdated into prior nightly runs (no silent restatement window) | leaf → trunk for incremental load | Verifiable | ASSUMPTION | `SELECT MAX(exported_at), MAX(event_date), DATEDIFF(MAX(exported_at), MAX(event_date))` — consistent large gaps = systematic lag; irregular gaps = backfill. An incremental mart with a narrow window will miss late-landing events silently. |
| A13 | `plan_tier` values are stable over time; no renamed or retired tier codes exist in the history that would cause a plan-mix break | leaf | Verifiable | ASSUMPTION | `SELECT DISTINCT plan_tier, MIN(event_date), MAX(event_date) FROM billing_export_daily GROUP BY plan_tier` — any tier with a hard cutoff date in the history is a renamed/retired tier; downstream plan-tier segmentation will miscategorize those rows. |

---

## Trunk rows still open — gating; do not build past these

- **A3 (NEEDS-DECISION → RevOps / billing system owner):** Effective vs booking date on cancel events. Controls which NRR cohort every churn lands in.
- **A9 (NEEDS-DECISION → RevOps / Finance BI):** Is this the same source Finance uses? If not, the mart will not reconcile to the board deck from day one — the gap inherited, not explained.
- **A5 (VERIFIABLE + Decision → Priya, VP Customer Success):** Are trials in the export? If yes, the active base and churn rate are wrong before a single query runs.
- **A2 (VERIFIABLE + Decision → RevOps):** Is `mrr_amount` a level or a delta on downgrade rows? If delta, the MRR spine is wrong.

---

## Trend / falsification runs — run before the build

| Check | Query / action | What confirms vs falsifies |
|---|---|---|
| **Trend (A4, A8) — most critical** | Profile distinct active accounts and new-event counts by month over full history | A structural break (step-change in volume) flags a recording-proc change; a very recent `MIN(event_date)` flags delta-only export |
| **Grain (A10)** | Count rows per (account_id, event_date, event_type) | Any >1 = grain is sub-account; sum-based MRR fans out |
| **event_type completeness (A6, A7)** | `SELECT DISTINCT event_type, COUNT(*)` + `WHERE event_type='downgrade' AND mrr_amount=0` | Values beyond four documented = undocumented transitions; $0-downgrade count > 0 = silent churns |
| **mrr_amount unit (A2)** | Percentile profile; check for negatives | Median in cents range = cents denomination; negatives = delta encoding |
| **Decompose-and-trend-each (A1)** | Plot new-event counts and cancel-event counts separately by month | A ratio held flat while both legs are moving = compensating shift, not stability |
| **Finance gap (A9)** | Compare distinct active account counts in export vs Finance's reported customer count for a known quarter | Material disagreement = gap lives in the source layer, not the view layer |

---

## Seam tie-outs to run during the build

- **Export → mart staging:** account count and event count at each load; any delta from the prior nightly run that looks like a backfill should be flagged, not silently absorbed.
- **Mart → charter/explore query:** row-level spot check on ≥4 accounts (one new, one cancel, one upgrade, one downgrade) — does the mart reflect what the raw export shows?
- **Mart headline → Finance deck:** once A9 is answered, document the expected gap (logos vs revenue, scope differences) so divergence is explained in the charter, not discovered at the board.
- Tie at the **grain** (account-event count), not just total MRR — a conserved total hides a wrong distribution.

---

## Verdict

**Foundation not cleared. 4 trunk rows gating (A3, A9, A5, A2) — the build must not
proceed on these until the owner questions are answered.**

The verifiable trunk checks (A1, A4, A6, A7, A10) can be run against the export now without owner input. The four Decision-type opens (A3, A9, A5, A2) require RevOps and Priya; A9 is the most dangerous — if the extract does not share Finance's source, the retention mart will inherit the same unresolved board-level gap that made `vw_monthly_churn` un-presentable. Building past it means building the gap twice, at larger scale.

**Re-verify when:** the billing export proc is changed, a new billing system is stood up, plan
tiers are renamed or restructured, or a pricing change lands that could alter how events are
recorded.

**Owner override:** owner may build past a gating trunk row. Log to `decisions.md`
(`2026-06-08 — OVERRIDE: built past <row> — owner <name>, rationale: <stated>`); no named
owner or rationale = no override. Every downstream brief/status carries
_"built over an open trunk assumption"_ visibly.
