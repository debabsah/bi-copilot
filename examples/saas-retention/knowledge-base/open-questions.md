# Open Questions  [all phases]
_What we don't know yet. Each: the gap, why it matters, who or where to resolve it._

- [x] What decision rides on the churn dashboard? Closed 2026-05-20 by the
  interrogation: fund onboarding vs fund growth (annual), plus the board story. See
  `purpose.md` and `requirements-brief.md`.
- [ ] **How must NRR reconcile to the Finance GL deck, and which retention number
  does the board see?** The board will compare the two; an unexplained gap is fatal
  (it cracked the rehearsal). Owner: Finance + RevOps. **Blocking the 2026-06-10 board meeting.**
- [ ] Win-backs / reactivations: does a returning account rejoin its original cohort
  or start fresh? Changes the NRR denominator. Owner: RevOps (contract fork left open).
- [ ] Early-life (first-90-day) churn by signup cohort is not built yet. The funding
  decision turns on it and the recommendation wobbled without it. Owner: this team.
- [ ] Who are the five hardcoded `NOT IN` accounts in `vw_monthly_churn`? They are
  silently dropped from every current figure. Owner: whoever inherits Dana's access.
- [ ] Are trials actually excluded from the active base? Inflates the base if not.
  Owner: billing / RevOps.
- [ ] **Cohort-grain bug in `vw_monthly_churn`:** the `active_start` CTE buckets by the
  month a billing period started, not by "active at month start," so accounts on annual
  or multi-month plans drop out of the denominator. Surfaced by `query-review.md`
  (Blocking #4); confirm the grain of `subscriptions` before any rebuild reuses this
  logic. Owner: whoever builds the NRR model.
- [ ] Full graded defect list for the inherited view: see `query-review.md` (4 Blocking,
  3 Latent, 1 Advisory). The Blocking ones gate any board number from this view.
- [ ] **Cross-source join keys: is there a confirmed shared account identifier across billing, CRM, support desk, and product usage?** Without this, Q2 (usage signal), Q3 (segmentation), Q4 (support signal), and Q6 (acquisition fit) cannot run. Owner: RevOps or whoever owns the data warehouse. First check: ask RevOps whether a unified account ID exists and where it lives. **Blocking Q2, Q3, Q4, Q6.**
- [ ] **Shorter-cadence CS allocation decisions:** Does Priya make quarterly decisions (at-risk account triage, renewal playbooks, QBR selection) that should anchor additional charter candidates? Owner: clarify with Priya in next session.
## Escalated from assumption-register.md (2026-06-08) — retention mart pre-flight

| # | Question | Owner | Gating |
|---|---|---|---|
| A3 | For a cancel booked today effective end-of-month, what value does `event_date` carry in `billing_export_daily`? | RevOps / billing system owner | YES — controls every NRR cohort window |
| A9 | What tables/system does Finance pull from for quarterly NRR, and does `billing_export_daily` read the same source? | RevOps or Finance BI | YES — if different, the mart will not reconcile to the board deck from day one |
| A5 | Are trials ever created in the billing system before conversion, and if so, are they in `billing_export_daily`? | Priya, VP Customer Success | YES — if present, every active-account count and churn rate is inflated |
| A2 | On a downgrade row in `billing_export_daily`, does `mrr_amount` carry the new MRR level, the old level, or the delta? | RevOps | YES — if delta, the mart's MRR spine is wrong |
# Open Questions  [Understand]
_Append-only. Resolved questions stay here with their answer and close date._

## From estate-map, 2026-06-09 (retention reporting data flow)

- [ ] **crm_accounts_sync → accounts (wiring):** Does a nightly job write CRM segment data into billing's `accounts` table, or is this a runtime join? If a write: which job, what target fields? Who to ask: Marcus → DBA.
- [ ] **accounts source system:** Which system owns and populates `accounts`? Check DDL or ask DBA.
- [ ] **billing_export_daily downstream:** What reads this extract in the retention scope? Does it load `subscriptions` or is it a separate analyst-facing extract? Marcus has field list from assumption audit.
- [ ] **tickets_weekly downstream:** Any current consumer? Or candidate-input only for future mart?
- [ ] **usage_events downstream:** What jobs or views read `usage_events`? Check DB catalog or ask engineering.
- [ ] **Board Deck vs Finance Quarterly Deck — metric definition reconciliation:** vw_monthly_churn = logo churn only; Finance GL = NRR/retention. Two figures, never reconciled. Are they measuring the same thing? Pre-requisite for model-contract design.
