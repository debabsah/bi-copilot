# Forecast Audit — demand model v2 [Audit]
_Audited 2026-05-05. Forecast: weekly demand, 13-week horizon.
Plan it gates: the planning-mart integration and H2 procurement volumes._

## Gate verdict
**`trustworthy`** — beats naive (MAPE 3.2% vs 6.1%), interval coverage 93% on a 95% band
(n=40), errors stable.

**Re-audit when:** 4 new weekly actuals have landed (coverage and drift must be re-checked
on the fresh window before the plan keeps leaning on this verdict).
