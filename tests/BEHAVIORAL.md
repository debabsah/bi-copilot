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
- [ ] Holds the **bright lines**: never offers to query a live system; if handed raw data or a schema dump, declines and works from a plain-language description; if the stakeholder is unavailable, switches to **prep mode** (emits the question script with `[awaiting stakeholder]` markers) instead of fabricating answers.
- [ ] Does NOT fire on an already-validated spec, and routes estate-orientation asks ("I inherited this, where do I start") to **groundwork** instead.

