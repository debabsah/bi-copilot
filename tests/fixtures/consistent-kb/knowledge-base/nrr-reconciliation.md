# NRR reconciliation — billing ↔ Finance GL (Q2 FY26)
_Run 2026-05-28 against the billing warehouse and the Finance GL export. Signed off: RevOps
(J. Okafor), Finance (M. Chen)._

NRR formula (per `kpi-contract.md` v1.0): `(start MRR + expansion − contraction − churn) / start MRR`.

| Line | Billing basis | GL basis | Delta |
|---|---|---|---|
| Start-of-window cohort MRR | $5.00M | $5.00M | 0.0% |
| Expansion | $0.78M | $0.765M | +2.0% |
| Contraction + churn (gross loss) | $0.37M | $0.37M | 0.0% |
| **NRR** = (5.00 + exp − 0.37) / 5.00 | **108.2%** | **107.9%** | **+0.3%** |
| Gross revenue churn = 0.37 / 5.00 | 7.4% | 7.4% | 0.0% |

Check: billing (5.00 + 0.78 − 0.37) / 5.00 = 5.41 / 5.00 = **1.082**; GL (5.00 + 0.765 − 0.37) / 5.00
= 5.395 / 5.00 = **1.079**. Within the ±0.5% contract tolerance. Q2 FY26 close snapshot; re-run quarterly.
