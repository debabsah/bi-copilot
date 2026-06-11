# Parity Proof — NRR % · v1 (billing_export_daily) vs v2 (billing_export_v2) · Jul-2025..Jun-2026  [Validate]
_Proven 2026-06-24, by Marcus Okafor (request) / BI assistant (computation). Gates: v2 migration cutover post-ship sign-off (required by change-impact.md). Pressure noted: v2 shipped 2026-06-17; tie-out run 2026-06-24 — recorded, not obeyed. **Tolerance (pinned BEFORE results):** abs ±0.50 pp per stratum; zero tolerance on in-scope row counts; 2023-cohort strata out of scope. Owner: Sana Qureshi, RevOps, 2026-06-20._

## Comparability map

| Dimension | v1 | v2 | Same? / Mapped how |
|---|---|---|---|
| `mrr_amount` units | INTEGER cents | DECIMAL(12,2) dollars | MAPPED — NRR % is a ratio; scalar transform cancels; pure-v2 is internally consistent |
| Event_type vocabulary | Pre-fix | Corrected (mart CTEs) | MAPPED — documented change; explains timing-level residuals |
| Watermark basis | Load-date | event_date | MAPPED — late-arriving events captured in v2 only; classified as Timing |
| Stray /100 | Present | Removed | MAPPED — internal to MRR units; NRR % ratio unaffected |
| Window | trailing-12 Jul-2025..Jun-2026 | Same | ✓ |
| Grain | Account / cohort-per-period | Same | ✓ |
| Strata dimensions | tier × cohort-half (single region) | Same | ✓ |
| 2023-cohort population | Included (63 rows) | Absent (documented backfill boundary) | MAPPED — out of scope per tolerance owner; in-scope counts identical |
| kpi-contract unit amendment | Not yet signed | Pending | Governance gap — does not invalidate NRR % comparison; sign-off remains open (see open-questions.md) |

## Stratified results (kit: parity_checks.stratified_diff — hand-computed)

| Stratum | v1 NRR % | v2 NRR % | diff (pp) | \|diff\| | Within ±0.50 pp? |
|---|---|---|---|---|---|
| Starter × 2024H1 | 94.1 | 94.5 | +0.40 | 0.40 | **PASS** |
| Starter × 2024H2 | 96.2 | 96.2 | 0.00 | 0.00 | PASS |
| Starter × 2025H1 | 97.0 | 97.0 | 0.00 | 0.00 | PASS |
| Growth × 2024H1 | 103.8 | 103.8 | 0.00 | 0.00 | PASS |
| Growth × 2024H2 | 105.1 | 105.1 | 0.00 | 0.00 | PASS |
| Growth × 2025H1 | 106.4 | 106.4 | 0.00 | 0.00 | PASS |
| Enterprise × 2024H1 | 111.0 | 111.0 | 0.00 | 0.00 | PASS |
| Enterprise × 2024H2 | 109.7 | 109.7 | 0.00 | 0.00 | PASS |
| Enterprise × 2025H1 | 112.2 | 112.2 | 0.00 | 0.00 | PASS |

**Total:** all 9 strata pass · **failing_strata: none** · **offsetting_error: False**

Row counts (in-scope): v1 = 2,114 − 63 = 2,051 · v2 = 2,051 · delta = 0 · zero-tolerance: **PASS**

## Residual ledger (kit: residual_summary — hand-computed)

| Cause | Amount | Evidence | Routed to |
|---|---|---|---|
| Timing — six late-arriving June events, absent from v1 freeze (load-date cut-off), present in v2 (event_date watermark) | +0.40 pp, Starter × 2024H1 | RevOps note, Sana Qureshi (attached); consistent with watermark change in change-impact.md | No further routing — cause mapped to documented migration change |
| Population / Scope — 63 rows, 2023-only subscriptions, v2 backfill boundary | +63 rows (v1 only) | Documented limitation; out of scope per tolerance owner | No routing — accepted on record |

**Unexplained NRR gap: 0.00 pp — within tolerance. Does NOT block sign-off.**
**Unexplained row delta (in-scope): 0 rows — meets zero tolerance.**

## Verdict
**PARITY** — all nine in-scope strata within the pre-pinned ±0.50 pp tolerance; no offsetting errors; residuals fully classified; in-scope row counts exact. The single non-zero stratum (Starter × 2024H1, +0.40 pp) is explained by six late-arriving June events attributable to the event_date watermark fix, and remains within tolerance.

**Open governance item (does not block parity verdict):** kpi-contract unit amendment (RevOps + Finance sign-off) pending — see open-questions.md.

**Re-audit when:** next period closes (Jul-2026 trailing-12) / either side's definition changes / kpi-contract amendment status changes.
