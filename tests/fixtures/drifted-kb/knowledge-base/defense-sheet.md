# Defense Sheet - "NRR 108%, gross churn 4.2%, invest in growth not onboarding"  [Validate]
_Rehearsed 2026-06-01, ahead of the 2026-06-10 board meeting._

- **Claim defended:** NRR was 108% this quarter (up from 102% a year ago), gross
  revenue churn improved to 4.2% monthly; recommend investing next year's budget in
  new-logo growth rather than a dedicated onboarding team.
- **Decision it supports / audience:** the onboarding funding call and the board's
  read on retention health; the board, led by a former-CFO member who reads numbers
  closely.
- **Adversary rehearsed:** data / method skeptic (the ex-CFO board member).
- **Ammunition harvested:** the locked `kpi-contract.md` (its fork log and its
  reconciliation statement), `data-quality.md`, and `query-review.md` (the inherited
  view reviewed against the contract, which confirmed at the code level why it cannot
  reconcile to Finance).

## Attacks and answers
| Attack raised | Your best answer | Grade |
|---|---|---|
| "108% of what base? Survivors only, or including full churns?" | Start-of-period cohort MRR, account grain, expansion minus contraction and churn, per the locked contract. | held |
| "Finance says total revenue grew about 2%. You say retention is 108%. Which one is wrong?" | Answered 2026-06-03: the gap is definitional. NRR is existing-cohort billing-MRR; Finance is total GL revenue (new logos, services, timing). RevOps + Finance agreed NRR is the existing-base retention measure. | held (post-06-03) |
| "Did the definition move since last year?" | No: contract v1.0, effective-dated; last year's 102% recomputed on the same basis. | held |
| "Your NRR is blended. What is retention for accounts in their first 90 days?" | Did not have the early-life cohort cut on the slide. | wobbled |

## Weak spots to shore before the room
- **Finance reconciliation CLOSED 2026-06-03 (the gap that cracked the rehearsal): definitional, agreed and signed off.** This is the contract's
  former `[needs decision]`, resolved 2026-06-03. Finance and RevOps agreed the gap is definitional and which
  retention number the board sees (NRR for retention, beside Finance's total growth). It is
  the same gap `groundwork` first flagged in the inherited view on day one.
- **Add early-life churn by signup cohort.** It is the metric `requirements-brief.md`
  said the funding decision actually needs, and its absence is what let the
  recommendation wobble. Without it, "invest in growth, not onboarding" is unsupported.

- **Readiness verdict:** **the NRR number is ready** (Finance reconciliation closed 2026-06-03). The headline holds on definition, and the
  Finance gap is now reconciled (definitional); only the funding recommendation is not yet
  evidenced. Close the reconciliation and add the cohort cut, then rehearse again.
