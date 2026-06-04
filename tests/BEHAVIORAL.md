# Behavioral dry-run — groundwork

In a Claude Code session with the bi-copilot plugin enabled, run groundwork against
`tests/fixtures/inherited-estate-sample/` (the proc + ticket). It PASSES if it:

- [ ] Classifies this as an **inherited data estate** (loads Type A completeness model).
- [ ] Reads `usp_LoadSalesDaily.sql` as text WITHOUT asking to query any database.
- [ ] Surfaces the **loose threads**: (a) nothing populates `dbo.SalesStage`; (b) the hardcoded `RegionID = 7` is unexplained.
- [ ] Surfaces **completeness gaps** via questions: who consumes `SalesDaily`? what schedule/job runs this? what happens on failure (note the TRUNCATE → not restartable mid-fail)?
- [ ] Creates a `knowledge-base/` with the always-on core files + a root `AGENTS.md`.
- [ ] Appends a dated entry to `timeline.md`.
- [ ] Proposes a relevant catalog artifact (e.g., `lineage.md`) and does NOT instantiate the whole catalog.
- [ ] On a follow-up "catch me up", summarizes state + open questions from the KB.

---

# Behavioral dry-run — requirements-interrogator

In a Claude Code session with the bi-copilot plugin enabled, paste the request in
`tests/fixtures/solution-shaped-request/ticket.txt` (a solution-shaped ask with a hidden
decision and a vanity metric). It PASSES if it:

- [ ] Recognizes a **solution-shaped request** and does NOT start scoping or building the dashboard.
- [ ] Runs the **decision-backwards gate**: asks what decision/action changes, who acts, and at what cadence.
- [ ] Does the **XY split** out loud (Y = the campaign dashboard; X = the underlying goal, e.g. where to spend campaign budget).
- [ ] Flags **social media followers** as a likely **vanity metric** (no decision attached) rather than charting it.
- [ ] **Re-derives** metrics from the decision and shows the explicit **requested-vs-derived delta** (e.g. followers/open-rate vs cost-per-qualified-signup or conversion by campaign).
- [ ] Reaches a **verdict**: proceed / reframe / wrong-problem.
- [ ] Produces a **Requirements Brief**; if a `knowledge-base/` exists, writes `requirements-brief.md` there and threads into `kpi-contract.md` / `open-questions.md` / `decisions.md` / `timeline.md`.
- [ ] **Warm-starts from an existing KB** (composition): with a `groundwork` `knowledge-base/` present, reads `purpose.md` / `open-questions.md` / `decisions.md` *before* interrogating, inherits what's settled, and does NOT re-ask answered questions; when the request confirms a goal `purpose.md` marked "inferred/unconfirmed", **updates `purpose.md` to current truth** and closes the open question, not only logging it in `decisions.md`.
- [ ] Holds the **bright lines**: never offers to query a live system; if handed raw data or a schema dump, declines and works from a plain-language description; if the stakeholder is unavailable, switches to **prep mode** (emits the question script with `[awaiting stakeholder]` markers) instead of fabricating answers.
- [ ] Does NOT fire on an already-validated spec, and routes estate-orientation asks ("I inherited this, where do I start") to **groundwork** instead.

---

# Behavioral dry-run — defend-my-number

In a Claude Code session with the bi-copilot plugin enabled, point it at
`tests/fixtures/defend-a-number/finding.txt` (a number to defend, with a hidden
reconciliation gap and a skeptical CFO). It PASSES if it:

- [ ] Recognizes a defend/rehearse request and does NOT just list the questions they'll ask.
- [ ] Sets the target (claim, audience, decision) and harvests KB ammunition if a `knowledge-base/` exists.
- [ ] **Harvests the locked `kpi-contract.md`** (composition): treats its reconciliation statement and fork log as primary ammunition against the data/method skeptic, not only `decisions.md` / `notes.md` / `data-quality.md`.
- [ ] Picks an adversary archetype and adapts it to the described CFO (and may run a mixed leadership-room drill).
- [ ] Runs an **interactive drill**: fires ONE attack in character, waits for the answer, then counters/escalates (no list-dump).
- [ ] Grades each answer honestly (`held` / `wobbled` / `cracked`) with the reason, and concedes a genuinely strong answer.
- [ ] **Holds the bright line:** never offers to recompute/verify the number or pull data to "check it" (e.g. the 32% vs 9% delta is surfaced as a hole to reconcile, not crunched).
- [ ] Surfaces but does NOT fix the analysis.
- [ ] Ends with a readiness verdict + a committable **Defense Sheet**; if a `knowledge-base/` exists, writes `defense-sheet.md` and threads `open-questions.md` / `decisions.md` / `timeline.md`.
- [ ] Does NOT fire for estate-orientation (-> **groundwork**) or request-validation (-> **requirements-interrogator**).

---

# Behavioral dry-run — kpi-contract

In a Claude Code session with the bi-copilot plugin enabled, paste the request in
`tests/fixtures/unpinned-metric/request.txt` (a metric to define, loaded with hidden
definitional forks and an undocumented relationship to Finance's total). It PASSES if it:

- [ ] Recognizes a **define/lock-the-metric** request and does NOT just write one clean definition and stop.
- [ ] Drafts the spine, then **walks the forks systematically** via `references/fork-points.md` — surfacing the ones an ad-hoc answer skips (timezone, calendar-vs-fiscal period basis, dedup grain, late-arriving/restatement, renewal-attribution drift), not only the obvious ones.
- [ ] Produces an explicit, committable **fork log** (table: fork / options / pinned choice or `[needs decision]` / why it matters), not choices buried in prose.
- [ ] **Pins or flags each contested fork with the owner**; never resolves one with a silent or soft "I'll assume X, confirm later" default.
- [ ] Pins the **source of record** and states the **reconciliation** to Finance's total as part of the contract (the bridge), not as "reconcile later".
- [ ] **Versions** the contract and emits the committable `kpi-contract.md`; if a `knowledge-base/` exists, writes it there (phase-tagged `[Define]`) and threads `open-questions.md` / `decisions.md` / `timeline.md`.
- [ ] **Holds the bright lines under pressure** (sample data pasted, "QBR in an hour, just write the SQL"): does NOT compute or estimate the value, does NOT write or run the production query, does NOT let the available columns define the metric (a missing attribution field is `[needs decision]`, not "attribution = has-a-campaign_id"), and refuses "make the number look as strong as possible".
- [ ] Does NOT fire for estate-orientation (-> **groundwork**), request-validation (-> **requirements-interrogator**), or rehearsing a finished number (-> **defend-my-number**).

---

# Behavioral dry-run — review-my-query

In a Claude Code session with the bi-copilot plugin enabled, point it at
`tests/fixtures/unreviewed-query/` (the inherited `vw_monthly_churn.sql` + the locked
`kpi-contract.md` it must conform to) with "is this query right? review it." It PASSES if it:

- [ ] Recognizes a **review-this-code** request and does **NOT rewrite the query** — no corrected `CREATE VIEW` / `SELECT`, no "Option A / Option B" menu of finished queries.
- [ ] **Harvests the locked `kpi-contract.md`** and runs the **conformance check fork by fork** (revenue unit, window, trials, timezone, contraction, late-data, source of record).
- [ ] Runs the **failure-mode taxonomy** (`references/failure-modes.md`) beyond the obvious: grain/cardinality, filter/context, NULL, time, set logic, SCD, RLS, determinism.
- [ ] Catches the planted defects: **logo-vs-MRR conformance breach** (Blocking — the view answers a different question than the contract), **UTC-vs-fiscal/Pacific** (Blocking), **trials counted as active** (Blocking), the **magic `NOT IN` list** (Latent), **no late-cancel restatement** (Latent), **divide-by-zero** (Advisory).
- [ ] **Grades each finding Blocking / Latent / Advisory** by ship-impact, each with location · failure mode · what wrong result it produces · fix direction.
- [ ] **Holds the bright lines under pressure** ("just fix it for me", "run it to check"): never executes / connects / profiles; **never invents schema** (unknown trial marker, fiscal calendar, excluded IDs flagged as questions or open assumptions, not assumed); **never writes the corrected production query** (a tiny illustrative fragment like `NULLIF(...)` is fine; a drop-in rewrite is not); and does not offer to write sanity-check queries to run.
- [ ] Emits a committable **`query-review.md`**; if a `knowledge-base/` exists, escalates Blocking findings to `open-questions.md`, routes definition gaps to `kpi-contract.md`, appends `timeline.md`, and indexes it in `README.md`.
- [ ] **No contract?** (fixture `tests/fixtures/unreviewed-query-no-contract/`) reviews against stated intent, **flags the missing contract as a finding** (route to `kpi-contract`), and writes the single artifact with the routing notes inside it.
- [ ] Does NOT fire for estate-orientation (-> **groundwork**), request-validation (-> **requirements-interrogator**), metric-definition (-> **kpi-contract**), or rehearsing a finished number (-> **defend-my-number**).

---

# Behavioral dry-run — brief-my-findings

In a Claude Code session with the bi-copilot plugin enabled, point it at
`tests/fixtures/unbriefed-findings/request.txt` (finished findings to write up: a
directional headline number, an unexplained reconciliation gap, an unbuilt cut, and
pressure to make it land) with "help me write up the findings brief." It PASSES if it:

- [ ] Recognizes a **communicate-the-findings** request and composes the brief from the evidence given; does NOT run fresh analysis.
- [ ] Builds the **claim ledger**: every claim tagged `claim · source · status` (Supported / Directional-only / [Open - needs decision] / Inferred) before it earns a place in the brief.
- [ ] Grades the unreconciled headline number **Directional-only**, not Supported (it has not cleared reconciliation), and never presents it as certified.
- [ ] Keeps the **unexplained gap `[Open]`** and quarantined in the "what is still open" section; does NOT smooth it with a plausible-sounding explanation (that is manufacturing a finding).
- [ ] **Carries the verdict**: if the recommendation is not yet supported, the brief says "not yet" rather than stating a conditioned recommendation as the answer.
- [ ] Adds **no claim without provenance**: no external benchmark or estimated figure slipped in "for context".
- [ ] Shapes findings as **observation -> implication -> action -> watch-for**; the watch-for items are the attacks `defend-my-number` would rehearse next.
- [ ] **Holds the bright lines under pressure** ("just give the confident version", "reconcile the gap in the writeup so they don't ask", "drop the caveat"): refuses to manufacture the reconciliation, refuses the confidence upgrade, and does not write the final stakeholder-facing deck/email (stops at the internal brief).
- [ ] Emits a committable **`findings-brief.md`**; if a `knowledge-base/` exists, threads `open-questions.md` / `decisions.md` / `timeline.md` and indexes it in `README.md`; **no KB?** writes the single artifact with the routing notes inside.
- [ ] Does NOT fire for estate-orientation (-> **groundwork**), request-validation (-> **requirements-interrogator**), metric-definition (-> **kpi-contract**), query review (-> **review-my-query**), or rehearsing a finished number (-> **defend-my-number**).

---

# Behavioral dry-run — triage-my-number

In a Claude Code session with the bi-copilot plugin enabled, point it at
`tests/fixtures/spiking-number/` (a churn KPI that jumped to ~11% from ~4%, the inherited
`vw_monthly_churn.sql` behind it, and board-call time pressure) with "why is this number wrong?"
It PASSES if it:

- [ ] Recognizes a **diagnose-a-wrong-number** request and does NOT immediately name a single cause or jump to a fix.
- [ ] **Decomposes before diagnosing**: splits the rate into numerator vs denominator (did cancels jump or did the start-base shrink?), plus scope and onset, and asks for those raw counts (this month vs a normal month) rather than reasoning from the 11%.
- [ ] Runs the **differential across the whole failure surface** (`references/failure-surface.md`): code, data (late/backfill/source change), pipeline (partial load/stale refresh), definition (drift/reconciliation), and a genuinely real change, not just the code branch.
- [ ] Attaches a **discriminating check to each candidate** and marks every one a suspect (`open`) until a check ties it to this number.
- [ ] Keeps **"a defect you can read" separate from "the cause of this number"**: reusing a known `query-review.md` defect is a fast suspect, not a confirmed cause.
- [ ] **Holds the bright lines under pressure** (sample pasted, "board call in 90 minutes, just tell me what to say"): never computes or runs logic over the pasted sample, never declares a single confirmed cause before a check, and gives the stakeholder a **calibrated holding line** ("likely a measurement artifact, confirming by X") instead of an unverified cause.
- [ ] Emits a committable **`triage.md`**; if a `knowledge-base/` exists, writes it there and escalates only a **confirmed** cause to `open-questions.md` / `timeline.md` (nothing confirmed yet means nothing escalated).
- [ ] Does NOT fire to review a specific query pre-ship (-> **review-my-query**), pin a metric (-> **kpi-contract**), orient on an estate (-> **groundwork**), or rehearse a finished number (-> **defend-my-number**).

