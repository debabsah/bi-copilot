
```markdown
# Status — week of 2026-07-17  [Operate]
_For: Exec sponsor (routed via Priya Sharma, VP CS). Composed 2026-07-17 from
the knowledge-base record + attributed updates._

**RAG: AMBER**
Criteria: green = on plan, no unowned blocker, no active BLOCKING gate, no expired verdict.
Two lines below fail: onboarding pilot write-up gated (cannot be reported as a lift); forecast
intervals gated (cannot be planned against). Turns green when both gates clear and A3/A9
owners are assigned.
Watermelon test: capped by rows 5 and 7 below.

---

## The ledger

| Item | Status | Says who / as of |
|---|---|---|
| NRR parity — billing migration (v1→v2) | **Done (evidenced)** — 9 strata all within ±0.50 pp; residuals fully classified | parity-proof.md · 2026-06-24 · Marcus Okafor / BI assistant |
| Retention mart — design | **Done (evidenced)** — fct_account_month + dims specified | model-contract · timeline 2026-06-10 · Marcus |
| Retention mart — build | **Blocked** — gating open questions A3 (event_date on cancel) + A9 (Finance source tables) have no owner and no close date; build cannot proceed past these | audit register 2026-06-08; open-questions.md — since 2026-06-08, no change |
| Q1 finding: first-90-day churn +17.2 pp | **In-progress (Exploratory-found)** — hold-out Check 1 pre-registered for 2026-09; H2 (Starter tier) still PENDING — per-tier columns absent from paste-back | exploration-log · graded 2026-06-12 · Marcus |
| Onboarding pilot — "showed a lift" | **BLOCKING gate — write-up cannot proceed.** Nominal p = .049 does not survive sequential correction (7 peeks on a 10-week plan). Separately: 30-day activation is a proxy metric; 90-day churn (the decision metric) is unmeasured. The result cannot be reported to the sponsor at this time. | audit-my-experiment · 2026-07-06 · Marcus |
| Finance churn forecast — point path | **In-progress (gate passed)** — beats naïve 2.1×; usable for point-estimate planning | audit-my-forecast · 2026-07-08 · Marcus |
| Finance churn forecast — interval bands | **BLOCKING gate** — 50 % coverage vs 80 % nominal; all misses are upper-bound (understaffing side). Do not plan headcount or budget against the bands until recalibrated | audit-my-forecast · 2026-07-08 · Marcus |
| Four gating data questions (A2, A3, A5, A9) | **Blocked — no owners** — gates Q2/Q3/Q4, the mart build, and MRR spine accuracy; oldest open since 2026-06-08 | open-questions.md |
| Note | "Keep it green and upbeat" requested by Priya; honest version supplied per status-truth | this report |

---

## Carried verdicts (with age)

- **parity-proof.md** — PARITY (2026-06-24); no Re-audit condition triggered by the record; **standing**.
- **billing_export_daily assumption register** — "do not build past A3/A9 without owners" (2026-06-08); A3/A9 still open; **standing**.
- **audit-my-experiment: onboarding pilot** — BLOCKING (2026-07-06); sequential-correction failure; **active gate**.
- **audit-my-forecast: Finance forecast intervals** — BLOCKING (2026-07-08); coverage 50 % vs 80 % nominal; **active gate**.

---

## Next period (owner-attributed commitments)

- Onboarding pilot: run to week 10, with pre-registered churn guardrail and MME pinned to CS-team breakeven — **pilot team / Marcus to confirm schedule**.
- Forecast interval recalibration: Finance BI to own and close — **ask below**.
- A3 + A9 owner assignment: unblocks mart build within the same sprint — **ask below**.

---

## Asks

1. **RevOps** — assign owner to A3 (event_date on end-of-month cancel) and A2 (MRR on downgrade). Both are gating the mart build; oldest is 39 days open.
2. **RevOps or Finance BI** — assign owner to A9 (which tables Finance pulls for quarterly NRR vs billing_export_daily). Gates mart-to-board-deck reconciliation.
3. **Priya** — respond to A5 (are trials in billing_export_daily?). Gates every active-account count and churn rate.
4. **Finance BI** — schedule forecast interval recalibration before September planning cycle. The point path is usable now; the bands are not.
5. **Pilot team** — confirm week-10 run date and pre-registered churn guardrail. The nominal result cannot be cited to the sponsor until the gate clears.

---

## Notes

- **On the green request:** The parity win and the mart design are real and earned. The pilot result and forecast bands are not reportable at this grade — citing them in the September budget conversation as evidence and then having the methodology challenged would be the worse outcome. The amber clears the moment the two gates close and A3/A9 get owners; that is achievable before September.
- **Re-base check:** No plan dates have been re-based this period; no slips to record. The mart build block is a standing open question, not a new slip.
