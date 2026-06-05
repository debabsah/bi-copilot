# Object & Data Landscape  [Understand]
_Last updated: 2026-05-22._

- **Systems in play:** a billing system (subscriptions, MRR, plan changes); a
  Finance general ledger (recognized revenue, the quarterly board deck); no
  warehouse modeling layer for retention yet.
- **Key objects:**
  - `vw_monthly_churn` (SQL view, inherited from Dana) - monthly LOGO churn for the
    board deck. Counts accounts lost over accounts active at month start. Caveats in
    `data-quality.md`.
  - `metrics_notes.md` - half-page handoff note from Dana. Stale and partial.
  - Finance quarterly deck - reports a retention / NRR figure built outside this
    estate. Owner: Finance with RevOps (per Dana, unconfirmed).
- **How they connect:** the board deck currently pulls logo churn from
  `vw_monthly_churn`; Finance's retention number is produced separately from the GL.
  The two have never reconciled (see open questions).
- **Grain & keys:** `vw_monthly_churn` is one row per month, account grain
  underneath (account_id). Subscriptions carry status, period_start, canceled_at;
  trials reportedly share status = 'active' with paid accounts (unconfirmed).
