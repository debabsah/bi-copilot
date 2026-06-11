
```markdown
# Change Impact — billing_export_daily → billing_export_v2 (4 sub-changes)  [Build]
_Assessed 2026-06-15, by BI assistant (request: Marcus Okafor, RevOps). Deploy pressure: Tuesday 2026-06-17 — noted, not obeyed._
_Before/after: (1) mrr_amount INTEGER cents → DECIMAL(12,2) dollars; (2) event_type values new/cancel/upgrade/downgrade → created/churned/expansion/contraction; (3) exported_at column dropped; (4) history backfilled 2024-01 only — 2023 rows absent._
**Walked from:** estate-map.md (drawn 2026-06-09) · model-contract.md v1.0-draft (2026-06-10) · kpi-contract.md v1.0 (locked 2026-05-22) · vw_monthly_churn.sql (on hand) — radius is only as complete as this evidence; coverage boundary below.

---

## Verdict

0 hard BREAKS evidenced · 3 SILENT-DRIFT risks (1 on the locked NRR contract — RevOps + Finance sign-off required) · 3 unaffected (evidenced) · 2 UNKNOWN (explore cuts consumer class; exported_at usage — likely BREAKS on grep confirmation).

**Safe to ship: NO.** The three silent drifts outrank any pipeline error; one unresolved UNKNOWN consumer class; exported_at likely-BREAK not yet confirmed. All six pre-flight checks must clear before Tuesday.

**Coverage boundary:** explore cuts (platform, query count, column references not documented); any analyst notebooks or ad-hoc scripts on billing_export_daily; pipelines not in the estate map.

---

## The radius (every node, graded)

Severity ranked: silent drifts first, per the bright line that meaning-breaks outrank loud failures.

| Node | Reached via | Verdict | Evidence / check |
|---|---|---|---|
| **Retention mart ETL (mid-flight)** — sub-change 2: event_type rename | model-contract.md: billing_export_daily is a GATE source; ETL derives expansion / contraction / churn by filtering on event_type | **SILENT-DRIFT (filter/population) — #1 ranked** | Any `WHERE event_type IN ('new','cancel','upgrade','downgrade')` runs without error in v2 but returns 0 rows. Movement measures compute to 0. NRR = 100% for all cohorts. No pipeline alert fires. This is the failure mode that passes QA and surfaces at the board. Note: mart is mid-flight — if the filter code is not yet written, the risk is that it gets written with v1 vocabulary. Pre-flight: grep mart SQL dir for old event_type string literals AND brief the mart developer on v2 vocabulary before they author the movement CTEs. |
| **NRR kpi-contract.md** — sub-change 1: mrr_amount unit | kpi-contract.md: "Source of record: MRR from the billing system" — unit (cents vs dollars) is not pinned in the contract | **SILENT-DRIFT (type/unit + CONTRACT-MEANING) — owner sign-off required** | Any computation that joins a v1-sourced snapshot (cents) against v2 events (dollars) produces a ~100× ratio error in the NRR numerator or denominator. If the mart has materialised any intermediate MRR snapshot from v1, that snapshot cannot be mixed with v2 events without a one-time conversion pass. Even for a pure-v2 pipeline the contract itself must be amended: mrr_amount units are now part of the definition. Pre-flight: (a) grep mart code for ÷100 or ×0.01 conversion; (b) confirm no v1-sourced cents snapshot exists in any mart staging table. Owner sign-off: RevOps (primary) + Finance (co-signer), per kpi-contract.md. |
| **Retention mart ETL (mid-flight)** — sub-change 1: mrr_amount unit | model-contract.md: mrr_amount is the movement-measure input; fork "pre-computed on fact" means the ETL derives period-over-period values from billing events | **SILENT-DRIFT (type/unit)** | If mart ETL code contains a ÷100 conversion (cents-to-dollars), applying it against v2 doubles the division — MRR appears 100× too small. If no conversion: absolute MRR values shift but NRR ratio is preserved provided input is pure v2. Pre-flight: grep mart codebase for `mrr_amount` in context of any division or multiplication. |
| **Retention mart ETL (mid-flight)** — sub-change 3: exported_at dropped | Daily-extract incremental load patterns routinely use an export timestamp as the watermark; model-contract.md does not document the ETL's incremental strategy | **UNKNOWN — likely BREAKS** | If `exported_at >= last_watermark` is the incremental load key, the column-not-found error fires on the first v2 run. The mart fails to load. Pre-flight: `grep -rn "exported_at" <mart-sql-dir>`. Any hit = hard BREAK; redesign incremental strategy (event_date, ingestion_ts, or full reload) before ship. Zero hits = this node is safe. |
| **Retention mart ETL (mid-flight)** — sub-change 4: 2023 history absent | model-contract.md: signup_cohort is a stated NRR dimension; NRR formula requires start-of-period cohort MRR | **SILENT-DRIFT (filter/population) — bounded** | v2 backfill starts 2024-01-01. Current trailing-12 board window (Jul 2025–Jun 2026) is fully covered — **unaffected for the current readout**. Impact is on historical cohort slices: accounts whose first billing event is in 2023 will have a missing or partial MRR denominator, producing inflated NRR for those cohorts. Pre-flight: `SELECT MIN(event_date) FROM billing_export_v2` (confirm 2024-01-01 floor); ask RevOps whether any live board or finance slide shows NRR for 2023 cohorts. |
| **Explore cuts** (Marcus: "the explore cuts read this extract") | Marcus Okafor verbal, 2026-06-15 | **UNKNOWN — all 4 sub-changes potentially break or drift them** | Platform, owner list, query count, and column references not documented. Sub-change 2 (event_type): segmentation by event_type silently returns 0 rows. Sub-change 1 (mrr_amount): displayed MRR drops 100× or double-converts if ÷100 logic is present. Sub-change 3 (exported_at): BREAKS if referenced as a filter or sort key. Sub-change 4: gaps in any historical cuts pre-2024. `SELECT *` over billing_export_daily propagates the column drop invisibly to any downstream view. Pre-flight: Marcus to identify tool, owner list, and surface SQL for grep. See open-questions.md OQ-1. |
| **vw_monthly_churn** | estate-map.md edge ledger + vw_monthly_churn.sql on hand: reads subscriptions (status, canceled_at) and accounts (account_id JOIN) — billing_export_daily is not in the join path | **Unaffected (evidenced)** | No billing_export_daily edge. The view is not in the blast radius of this swap. |
| **Board Deck (logo churn)** | estate-map.md: "board deck currently pulls logo churn from vw_monthly_churn" | **Unaffected (evidenced)** | Reads vw_monthly_churn, which is unaffected. The planned retention mart replacement of this feed has not shipped — not in scope for this change. |
| **Finance Quarterly Deck** | estate-map.md: "Finance's retention number is produced separately from the GL" | **Unaffected (evidenced)** | Finance GL source only; no billing_export edge in the estate map. |

---

## Pre-flight checks (run and paste back before the change)

**1 — Event-type string scan (sub-change 2) — HIGHEST PRIORITY**
```bash
grep -rn \
  "'new'\|'cancel'\|'upgrade'\|'downgrade'\|\"new\"\|\"cancel\"\|\"upgrade\"\|\"downgrade\"" \
  <mart-sql-dir> <explore-cuts-query-dir>
```
Expected: zero hits. Any hit = a movement-measure filter that will silently return 0 rows in v2. Fix: update string literals to `'created'`, `'churned'`, `'expansion'`, `'contraction'` before ship. Also brief the mart developer: v2 vocabulary is the authoring standard from here.

**2 — exported_at column scan (sub-change 3) — RESOLVES LIKELY-BREAK**
```bash
grep -rn "exported_at" <mart-sql-dir> <explore-cuts-query-dir>
```
Expected: zero hits (safe). Any hit = BREAKS on first v2 run. Fix: replace with an alternative watermark (event_date, an ingestion timestamp, or full-reload pattern) before ship.

**3 — mrr_amount conversion scan (sub-change 1)**
```bash
grep -rn "mrr_amount" <mart-sql-dir> <explore-cuts-query-dir>
# inspect each hit for: / 100, * 0.01, CAST … / 100, ::money
```
Any ÷100 logic = double-conversion in v2; remove it. Also check: does any mart staging or snapshot table already hold v1-sourced mrr_amount in cents? If yes, that table cannot be joined with v2-dollar events without a one-time conversion pass — document this before the ETL is authored.

**4 — v2 backfill floor and vocabulary (sub-changes 2 and 4)**
```sql
-- Confirm backfill floor
SELECT MIN(event_date) AS earliest_row FROM billing_export_v2;
-- Expected: 2024-01-01

-- Confirm event_type vocabulary is exactly the new set
SELECT DISTINCT event_type FROM billing_export_v2 ORDER BY 1;
-- Expected exactly: contraction, created, churned, expansion
```
If unexpected event_type values appear, the grep in check 1 must also cover them.

**5 — v1 cents snapshot inventory (sub-change 1 — contract-meaning)**
```sql
-- For each mart staging or snapshot table already built from billing_export_daily:
SELECT MAX(mrr_amount) FROM <staging_table> WHERE <a known large account>;
-- A value in the millions = cents; in the tens of thousands = likely dollars.
```
If any such table exists: it must not be joined with v2 events until a conversion pass is run. List the tables and flag them to RevOps before sign-off.

**6 — Explore cuts inventory (all sub-changes) — GATES THE UNKNOWN**
Ask Marcus: (a) which BI tool or query layer hosts the explore cuts, (b) who owns them, (c) how many queries touch billing_export_daily. If this is unresolved by Tuesday 2026-06-17, the explore cuts must remain pointed at billing_export_daily (v1) until checks 1–3 are run against their SQL. Do not flip them to v2 on ship day without clearance.

---

## Post-change verification

- **Movement measures must be non-zero.** After v2 is live, run: `SELECT event_type, COUNT(*), SUM(mrr_amount) FROM billing_export_v2 WHERE event_date >= '2024-01-01' GROUP BY 1`. A 0-row or null result for churned/expansion/contraction is the event_type drift smoking gun, not a success signal.
- **MRR unit spot-check.** Pick one known account with ~$5,000 MRR. In v2: `SELECT SUM(mrr_amount) FROM billing_export_v2 WHERE account_id = '<known>' AND event_date = '<recent month>'`. Expected: ~5000.00. If ~500000: cents leak; if ~50.00: double-conversion.
- **NRR parity route to prove-my-parity.** Strata: plan_tier × signup_cohort × region. Comparison period: one complete trailing-12 window on v1 vs same window on v2. Grand-total NRR match alone is insufficient — offsetting silent drifts cancel at the aggregate. The proof is stratified.
- **Contract owner confirmation.** RevOps + Finance to compare v2-computed NRR against the last signed-off board number before the deck is regenerated from v2 data.

---

## Sign-offs and rollback

- **NRR kpi-contract.md (sub-change 1 — meaning drift):** RevOps (primary owner) + Finance (co-signer) must sign off before the board deck is regenerated from v2. Contract amendment required: add unit specification (`mrr_amount` is in USD dollars, DECIMAL(12,2)) to the NRR source-of-record clause. Status: **pending sign-off** (see kpi-contract.md amendment note).
- **2023 cohort gap (sub-change 4):** RevOps to confirm in writing whether any live board or finance slide requires pre-2024 cohort baselines. If yes: agree a migration path for 2023 data before ship. If no: document the accepted scope boundary.
- **Rollback:** keep `billing_export_daily` live in parallel until all six pre-flight checks pass and post-change verification completes. Re-point consumers one at a time — mart ETL first, explore cuts after their own pre-flight clears. Do not drop `billing_export_daily` on ship day.
```

---

```markdown
knowledge-base/open-questions.md
```

```markdown
# Open Questions

## OQ-1 — Explore cuts: consumer identity and blast-radius scope
**Raised:** 2026-06-15 · **From:** change-impact.md (billing_export_daily → billing_export_v2)
**Owner:** Marcus Okafor (raised the ask; knows the tooling)
**Question:** What platform hosts the explore cuts that read `billing_export_daily`? Who owns them? How many queries reference (a) old event_type string literals (`new`, `cancel`, `upgrade`, `downgrade`), (b) `exported_at`, (c) `mrr_amount` with a ÷100 conversion? This determines whether explore cuts are in the BREAKS or SILENT-DRIFT column for the v2 swap.
**Blocks:** ship decision for billing_export_v2. If unresolved by Tuesday 2026-06-17, explore cuts must remain on v1 until each check clears.

## OQ-2 — exported_at: usage in retention mart ETL
**Raised:** 2026-06-15 · **From:** change-impact.md (billing_export_daily → billing_export_v2)
**Owner:** mart developer (Marcus Okafor to identify)
**Question:** Does the mid-flight retention mart ETL reference `exported_at` as an incremental load watermark or for any other purpose? Resolution: `grep -rn "exported_at" <mart-sql-dir>`. Zero hits = safe. Any hit = BREAKS on first v2 run; incremental strategy must be redesigned before ship.
**Blocks:** ship decision (BREAKS-class risk pending grep).
```

---

```markdown
knowledge-base/timeline.md
```

```markdown
# Timeline

## 2026-06-15 — Change impact assessed: billing_export_daily → billing_export_v2
by: BI assistant (request: Marcus Okafor, RevOps)
Deploy pressure: Tuesday 2026-06-17.
Result: 3 SILENT-DRIFT risks (1 on locked NRR contract — RevOps + Finance sign-off required before board deck regeneration); 2 UNKNOWN risks (explore cuts consumer class OQ-1; exported_at likely-BREAK OQ-2); 3 nodes unaffected (vw_monthly_churn, Board Deck, Finance Quarterly Deck). Verdict: not safe to ship without pre-flight clearance. Six checks written; parity verification routes to prove-my-parity.
Artifacts: change-impact.md (this entry) · open-questions.md OQ-1, OQ-2 · catches.md (2 entries) · kpi-contract.md amendment note.
