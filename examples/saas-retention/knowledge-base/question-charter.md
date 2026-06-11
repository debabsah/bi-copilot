# Question Charter — Retention & Onboarding Investment

Status: LIVING — first session 2026-06-04 with Priya Sharma (VP Customer Success)
Vanity flag: none — decision landscape partially elicited (gap logged)
Charter summary: 6 decision-anchored · 0 curiosity · unasked: 1 (Q6, anchored — the disconfirming test)

## Decision landscape (elicited 2026-06-04, from Priya Sharma; prior: interrogation 2026-05-20 with Priya)

| Decision | Who acts | Cadence / next occurrence | Lever |
|---|---|---|---|
| Fund dedicated onboarding/CS team vs fund new-logo growth | Exec team (Priya proposes) | Annual, ~December 2026 (6 months out) | Invest / delay / redirect |
| CS coverage allocation — which accounts get high-touch | Priya | Ongoing; quarterly planning | Coverage model update |

**Elicitation gap (open):** Does Priya make shorter-cadence decisions (at-risk account triage, renewal playbook triggers, QBR selection) that should anchor additional candidates? Flag for next session → added to `open-questions.md`.

## Estate as described (inventory of the askable)

| Source | What it holds | Availability evidence |
|---|---|---|
| Billing | Subscriptions, MRR, upgrades/downgrades | Cited: Priya 2026-06-04; history back to 2023 |
| CRM | Deals, segments, account owners | Cited: Priya 2026-06-04 |
| Support desk | Tickets with timestamps | Cited: Priya 2026-06-04 |
| Product usage events | Events by account | Cited: Priya 2026-06-04; **since January 2025 only** (18 months of history) |
| Cross-source join keys | Shared account IDs linking billing / CRM / support / usage | **UNVERIFIED** — no confirmed shared key across all four systems; verification required before any multi-source candidate runs (see Q2, Q3, Q4, Q6) |

**Known estate hazards (from KB):**
- `vw_monthly_churn` has a confirmed cohort-grain bug (KB: `query-review.md`, Blocking #4): `active_start` buckets by billing-period start, not by "active at month start," so annual and multi-month plans drop from the denominator. **Any early-churn analysis must rebuild from raw `subscriptions` — not reuse this view.**
- Five accounts hardcoded in `NOT IN` are silently excluded from all current churn figures. Owner: whoever inherits Dana's access.
- Trial exclusion from the active base is **UNVERIFIED** — inflates the denominator if trials are included.
- Win-back / reactivation treatment is **UNVERIFIED** — original cohort or fresh start changes the NRR denominator.

## Candidates (ranked; criteria below)

### Q1. Is first-90-day churn disproportionately high — and which plan tiers and cohort vintages drive it?

- **Tier:** ANCHORED — fund-onboarding decision (exec team, annual, ~December 2026)
- **Expected shape:** HYPOTHESIS — no data examined. If early-life churn is disproportionate relative to later-life churn, and concentrated in identifiable cohorts or plan tiers, the case for onboarding investment has a factual floor. If churn is distributed evenly across account lifetime, or concentrated post-90-days, the framing "onboarding is the problem" needs revisiting before the budget ask is made.
- **How to read:** Proportion of total churned MRR exiting in the first 90 days of subscription life, broken by plan tier and cohort vintage (2023–2025). A first-90-day share materially above what a flat hazard rate would predict is notable. Magnitude and concentration matter more than direction alone.
- **Confirms via:** `explore-my-data` — pre-registered cohort cut, user runs and pastes back. Two definition decisions needed first (logo churn or MRR churn; trial and win-back treatment) — these should be locked via `kpi-contract` before the cut runs.
- **Data:** Billing back to 2023 (cited: Priya 2026-06-04) — sufficient vintage depth. **Cannot reuse `vw_monthly_churn`** (cohort-grain bug, KB `query-review.md` Blocking #4). Rebuild from raw `subscriptions`.
- **Effort:** M — clean rebuild required; definition lock is the first step.
- **Status:** PROPOSED

---

### Q2. Do product usage patterns in the first 90 days distinguish retained accounts from churned ones?

- **Tier:** ANCHORED — onboarding investment decision; if a usage gap exists, it identifies a specific intervention point (activation design, in-product guidance, early CS touchpoints)
- **Expected shape:** HYPOTHESIS — no data examined. If accounts that churn show markedly lower usage in days 1–90, the case points toward activation programs. If usage is similar across outcomes, the problem is upstream (fit, wrong-segment acquisition) or downstream (mid-life friction), and activation investment addresses the wrong moment.
- **How to read:** Event counts or distinct active-days in 30/60/90-day windows, split by eventual 6-month retention outcome. Looking for a large, stable difference across a meaningful account base — not a marginal correlation. Note: 18 months of usage data means cohort coverage is limited to accounts starting from July 2024 at earliest.
- **Confirms via:** `explore-my-data` — usage event log × billing churn dates; user runs and pastes back.
- **Data:** Usage events since January 2025 (cited: Priya 2026-06-04) × billing churn dates (cited). **JOIN feasibility UNVERIFIED** — confirmed shared account key between usage system and billing is a prerequisite.
- **Effort:** M — two sources; join-key verification is the gate.
- **Status:** PROPOSED — BLOCKED pending join-key confirmation.

---

### Q3. How does churn vary by CRM segment, plan tier, and deal size — is the problem broad or concentrated?

- **Tier:** ANCHORED — CS allocation decision (Priya, ongoing); also scopes the budget ask. A concentrated problem (e.g., SMB, specific ACV band) allows targeted CS coverage. A broad problem requires a different investment logic entirely.
- **Expected shape:** HYPOTHESIS — no data examined. If first-90-day churn concentrates in one segment or ACV band, the CS team can be deployed selectively and ROI is easier to demonstrate. If churn is evenly distributed across segment and deal size, the intervention needs to be structural rather than targeted.
- **How to read:** Churn rate by CRM segment × plan tier, weighted by churned MRR. A 2–3× difference on material MRR bases is actionable. Segment definitions should be confirmed with RevOps before interpretation — "segment" in the CRM may mean different things to different teams.
- **Confirms via:** `explore-my-data` — CRM × billing; user runs and pastes back.
- **Data:** CRM (cited: Priya 2026-06-04) × billing (cited). **JOIN feasibility UNVERIFIED.**
- **Effort:** M.
- **Status:** PROPOSED — BLOCKED pending join-key confirmation.

---

### Q4. Does early support-ticket volume or topic predict churn?

- **Tier:** ANCHORED — CS investment design; if a triage signal exists in support data, CS can intervene on the right accounts earlier, without waiting for a usage signal
- **Expected shape:** HYPOTHESIS — no data examined. If accounts that churn open more tickets — or specific topic types (setup failures, integration errors, billing confusion) — in their first 90 days, that is an early-warning list a CS team can act on. If ticket patterns are indistinguishable between churned and retained accounts, support load is a cost question, not a churn-prediction input.
- **How to read:** Ticket counts and topic distribution by week-of-tenure for churned vs retained accounts. A clear step-function difference in the first 90 days (not a slight elevation that could be noise) is actionable.
- **Confirms via:** `explore-my-data` — support desk × billing; user runs and pastes back.
- **Data:** Support desk tickets with timestamps (cited: Priya 2026-06-04) × billing churn dates (cited). **JOIN feasibility UNVERIFIED.** Ticket topic structure **UNVERIFIED** — if tickets are free text only, topic clustering adds significant effort.
- **Effort:** M–H depending on ticket structure.
- **Status:** PROPOSED — BLOCKED pending join-key confirmation and ticket-structure check.

---

### Q5. If first-90-day churn fell by a plausible amount, what NRR improvement would result — and is it in the right order of magnitude to justify the CS investment?

- **Tier:** ANCHORED — the budget ask itself; the exec team will want an ROI range, not a qualitative case
- **Expected shape:** HYPOTHESIS — no data examined. A sensitivity model: billing history establishes a current NRR baseline; a range of assumptions about reducible first-90-day churn generates a range of NRR improvement; that range is compared against the fully-loaded cost of a CS hire. The question is whether the upside is plausibly in the right order of magnitude — not whether it is certain.
- **How to read:** A range with its assumptions named, not a point forecast. The purpose is to give the exec team a defensible floor and ceiling, not a single number to quote.
- **Confirms via:** `kpi-contract` first (NRR definition must be locked and reconciled to the Finance GL deck — the gap that nearly cracked the June board rehearsal, per KB `open-questions.md`); then `explore-my-data` for the sensitivity model.
- **Data:** Billing back to 2023 (cited). **BLOCKED** on NRR definition and GL reconciliation (KB `open-questions.md` — currently listed as blocking the 2026-06-10 board meeting).
- **Effort:** M once NRR is defined.
- **Status:** PROPOSED — BLOCKED pending `kpi-contract` (NRR definition) and Finance/RevOps alignment.

---

## The unasked (mandatory)

### Q6. Is the churn problem in onboarding execution — or in acquisition fit?

Priya is convinced onboarding is the problem; every churned logo she's spoken with said the first 90 days were rocky. That is real qualitative signal. So is the alternative hypothesis: Sales may be acquiring customers who would churn regardless of how well onboarding runs — accounts that were too small, too unsophisticated, or whose use-case was misaligned at the point of sale. If that is true, a CS team would reduce churn velocity but not address the root cause. The right investment would be in ICP tightening and GTM targeting, not CS headcount. The exec team deserves to know which it is before approving the ask.

- **Tier:** ANCHORED — frames the budget ask; if the root cause is acquisition quality, the investment redirects toward Sales and Marketing rather than CS
- **Expected shape:** HYPOTHESIS — no data examined. If churned accounts (especially first-90-day) look systematically different from retained accounts at the point of sale — lower ACV, different segment, different lead source, different deal velocity — that is an acquisition signal. If deal characteristics are indistinguishable at close, onboarding execution is the more plausible lever.
- **How to read:** CRM deal characteristics (ACV, segment, lead source if available) for churned vs retained cohorts, weighted by MRR. Looking for a systematic, large difference — not a single anecdote. If churned accounts are concentrated in deals closed below a certain ACV or from a specific channel, that is a Sales scoping conversation, not a CS onboarding conversation.
- **Confirms via:** `explore-my-data` — CRM × billing; user runs and pastes back. Lead-source data should be included if available.
- **Data:** CRM (cited: Priya 2026-06-04) × billing (cited). **JOIN feasibility UNVERIFIED.** Lead-source availability in CRM **UNVERIFIED**.
- **Effort:** M.
- **Note:** This is the question with the potentially unwelcome answer. An honest result pointing to acquisition fit would redirect the investment ask away from CS. It belongs on the charter for exactly that reason — the exec team should not make a six-figure staffing decision without ruling this out.
- **Status:** PROPOSED

---

## Ranking criteria (this charter's rubric)

Three axes, graded H/M/L; anchored candidates always before curiosity:

- **Decision-weight:** what changes if this is answered, who acts, how soon. An answer nobody acts on this quarter is L regardless of how interesting it is.
- **Feasibility:** data cited as available = H; one or more UNVERIFIED dependencies = M (cap); requires instrumentation not described = L. An UNVERIFIED dependency caps feasibility at M; the verification check is written into the candidate's path.
- **Effort:** single extract on existing data = L; join or definition needed = M; new instrumentation or free-text processing = H.

Sort order: anchored before curiosity; then decision-weight; then feasibility; then inverse effort. Ties go back to Priya — they are real questions for the session, not coin flips.

| Rank | Q | Description | Decision-wt | Feasibility | Effort | Notes |
|---|---|---|---|---|---|---|
| 1 | Q1 | Early-life churn shape | H | H | M | Load-bearing; billing exists; rebuild required but feasible now |
| 2 | Q3 | Segmentation (where is it concentrated?) | H | M | M | Answers WHERE before HOW; join key is the gate |
| 3 | Q2 | Usage activation signal | H | M | M | Most action-oriented for onboarding design; join key is the gate |
| 4 | Q6 | Acquisition vs onboarding fit (UNASKED) | H | M | M | Could redirect the investment thesis; same feasibility profile as Q2/Q3 |
| 5 | Q4 | Support ticket signal | H | M | M–H | Actionable but ticket structure is an unknown |
| 6 | Q5 | ROI quantification | H | H | M | Critical for the budget ask; BLOCKED on NRR definition — ranks 6th until prerequisite resolves |

Q5 ranks last not because it is unimportant — it is the conversation with the exec team — but because it cannot run until NRR is defined and reconciled. Once that blocker closes, it returns to the top tier.

## Session log

- 2026-06-04 — Priya Sharma (VP CS) — first charter session. Estate described: billing (2023–), CRM, support desk, usage events (Jan 2025–). Decision confirmed: annual budget (fund onboarding/CS vs fund growth), ~December 2026. Six candidates proposed; none yet accepted or declined — walkthrough in progress. One elicitation gap noted: shorter-cadence CS allocation decisions not explored. Conviction noted: "convinced onboarding is our problem" — logged; Q6 chartered as the disconfirming test; no finding delivered.
