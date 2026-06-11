# Worked example: one project, end to end

This is the analytics-office bench run end to end on a single project, so you can watch
the disciplines **compose through a shared knowledge base** instead of just reading
that they do. This walkthrough threads seven of the nineteen disciplines on one project:
one notices something while reading inherited SQL, and a full lifecycle later that same
something is what keeps a bad number out of the board readout.

> **Meridian is a fictional B2B SaaS company.** Every account, name, and number here
> is invented for this example. Nothing is queried or computed; the skills read text
> and write Markdown, which is the whole point.

The reader-facing artifacts are real files you can open:

- [`inputs/`](inputs/) - the raw material you start with (an inherited SQL view, a
  departed analyst's notes, a stakeholder request, a number to defend).
- [`knowledge-base/`](knowledge-base/) - what those seven disciplines produced and kept
  updating. Start at [`knowledge-base/README.md`](knowledge-base/README.md).

---

## The setup

You have just taken over analytics at Meridian. The VP of Customer Success wants a
churn dashboard for a board meeting in three weeks. What you inherit is an undocumented
SQL view (`vw_monthly_churn`) and half a page of notes from the analyst who left. The
notes contain one throwaway line: the churn number and Finance's retention number
"never quite line up, and nobody ever got to the bottom of why."

Hold onto that line. The bench does.

## The chain at a glance

| # | Skill | Phase | Fed | Produced | KB files touched |
|---|---|---|---|---|---|
| 1 | groundwork | Understand | the inherited view + Dana's notes | the knowledge base, classified estate, the loose threads | purpose, landscape, open-questions, decisions, notes, data-quality, timeline, AGENTS |
| 2 | requirements-interrogator | Define | "build me a churn dashboard" + Priya's answers | a reframe verdict and the metrics the decision actually needs | requirements-brief, **purpose (updated)**, open-questions (one closed), decisions, timeline |
| 3 | kpi-contract | Define / Design | the reframed metrics | NRR + gross revenue churn, locked v1.0, with a fork log | kpi-contract, open-questions, decisions, timeline |
| 4 | review-my-query | Build / Validate | the inherited `vw_monthly_churn` + the locked contract | 8 graded findings (4 Blocking); the view implements neither contracted metric | query-review, open-questions, decisions, data-quality, timeline |
| 5 | defend-my-number | Validate | the 108% NRR claim + the board context | a rehearsal that cracks, and a "not yet" verdict | defense-sheet, open-questions, decisions, timeline |
| 6 | brief-my-findings | Deliver | the locked contract, the query review, the defense sheet | a board readout that carries the "not yet" and keeps the gaps open | findings-brief, decisions, timeline |
| 7 | triage-my-number | Operate | the retired view spiking in production + the KB | a measurement-artifact diagnosis, a calibrated line, no confirmed cause | triage, timeline, decisions (reinforced) |

Each skill was pointed only at its own input. None was told "read the knowledge base."
They read it because that is what the skills instruct, and because `groundwork` left an
`AGENTS.md` and a `README.md` index pointing the way.

## What each skill did

**1. groundwork (Understand).** Read `vw_monthly_churn.sql` and `metrics_notes.md` as
text, without touching a database. Classified an inherited estate and surfaced the
loose threads: churn is counted in logos (so seat downgrades are invisible), trials may
be silently included, five accounts are hardcoded out with no explanation, and the view
has never reconciled to Finance. It stood up the knowledge base and recorded the goal as
**inferred and unconfirmed**, because nobody had confirmed it yet.

**2. requirements-interrogator (Define).** Took Priya's request, which is a solution
("a dashboard with logo churn, MRR churn, and a 12-month curve"), and drove it back to
the decision: fund an onboarding team next year, or put the money into new-logo growth.
The 12-month curve turned out to be decoration ("the board likes a nice chart"). Logo
churn turned out to be the wrong headline for a business where customers expand and
contract seats. Verdict: **reframe**, build Net Revenue Retention instead. It then
**updated `purpose.md` from "inferred" to the confirmed goal** and closed the open
question groundwork had left, rather than just logging a note. State stays current truth.

**3. kpi-contract (Define / Design).** Pinned NRR and gross revenue churn. The fork log
forces every silent choice into the open: cohort base, window, grain, whether
contraction counts, trials, timezone, late data. Two forks could not be resolved on the
spot, so they were marked `[needs decision]` with named owners rather than guessed. One
of them is the Finance reconciliation.

**4. review-my-query (Build / Validate).** Read the inherited `vw_monthly_churn` as text,
without running it, against the locked contract. Walked each pinned fork, then the
failure-mode taxonomy, and graded what it found: 8 findings, 4 of them Blocking. The
headline finding is that the view counts logos while the contract pins MRR, so it is the
wrong metric, not a fixable one, and that unit mismatch is exactly why it never lined up
with Finance. It also caught quieter bugs the eye skips: trials leaking into the base via
`status = 'active'`, UTC truncation against a fiscal Pacific calendar, and a cohort CTE
that buckets by the month a period started rather than membership at month start. It
**did not rewrite the view or invent the missing trial flag** to make a fix runnable; it
located each defect, named the failure mode, graded it, pointed the direction, and left
`query-review.md`. Verdict on the inherited view: retire it as a board source.

**5. defend-my-number (Validate).** Rehearsed the board readout against a data and
method skeptic. It harvested the locked contract and the query review as ammunition,
which is exactly what held up under two of the attacks. But the unresolved reconciliation
was still unresolved, and that is the attack that cracked. Verdict: **not yet.**

**6. brief-my-findings (Deliver).** Composed the board readout from the evidence already
in the knowledge base: the locked contract, the query review, and the defense sheet. The
easy move, the one a confident pass makes, is "NRR is 108%, retention is healthy, invest
in growth." It did the disciplined thing instead: graded the 108% as **directional**
because it is not yet reconciled, kept the Finance gap and the missing cohort cut as open
items, and carried the rehearsal's **not yet** verdict into the brief rather than
smoothing it away. It wrote `findings-brief.md`, not the board slides. The honest readout
is the one that does not blow up in the room.

**7. triage-my-number (Operate).** Weeks of work later, the inherited view is still feeding
an internal exec dashboard, and one month it prints 11% logo churn instead of the usual 4%.
An exec asks if churn is spiking, days before the board call. Instead of tunnelling on the
scariest cause or reaching for the data, it ran a differential across the whole failure
surface and reached straight for the defects `query-review.md` had already graded: the
cohort-grain bug shrinks the denominator, trials inflate the base. It kept "a defect you can
read" separate from "the cause of this 11%", which still needs one decomposition check, gave
the exec a calibrated holding line ("almost certainly a measurement artifact, confirming by
EOD") instead of a guess, and never computed the number itself. The Build-phase review paid
off in Operate: the spike is the retirement decision proving itself in production.

## The money shot: one gap, traced across the whole spine

The single most important thing this example shows is not any one skill. It is what
travels between them. Follow the Finance reconciliation gap:

```
groundwork (Understand)            Dana's note says the view "never lines up" with Finance.
                                   Logged as a data-quality caveat and an open question.
        |
        v
requirements-interrogator (Define) Reframing to NRR makes the board-vs-Finance comparison
                                   explicit. The open question is carried, not dropped.
        |
        v
kpi-contract (Design)              The gap is formalized as a contract [needs decision]:
                                   "Finance + RevOps to confirm the exact bridge."
        |
        v
review-my-query (Build/Validate)   The inherited view, reviewed against the contract,
                                   counts logos, not dollars. That unit mismatch is the
                                   code-level root cause of the gap (Blocking #1). The
                                   old view is retired; the forward bridge stays open.
        |
        v
defend-my-number (Validate)        "Finance says revenue grew 2%, you say 108%. Which is
                                   wrong?" The presenter cannot answer. CRACKED.
                                   Verdict: not yet. Do not present until it is closed.
        |
        v
brief-my-findings (Deliver)        The board readout carries the gap as an open item and
                                   the verdict as "not yet", not "retention is healthy."
                                   The honest brief is the one that survives the room.
```

A throwaway line in a departed analyst's notes, read on day one, is what stops a
plausible-looking 108% from blowing up in front of the board three weeks later. No single
skill carries that. The knowledge base does.

(There is a quieter second thread too: the interrogator derived that the decision needs
early-life churn by cohort; it never made the contract's headline; and that gap is what
made the recommendation **wobble** under the last attack. The bench caught two problems,
not one.)

And a third thread shows the knowledge base compounding the other way. The defects
`review-my-query` graded during the build become `triage-my-number`'s first suspects when
the retired view misbehaves in production weeks later. Work done once, in Build, pays off
again in Operate: diagnosing the 11% spike took minutes and a calibrated holding line, not a
panic, because the suspects were already written down.

## What to notice

- **Composition is consumption plus accretion.** Each skill read what came before and
  *extended* the knowledge base; none restated or overwrote another's work. The timeline
  reads as one continuous project, not seven disconnected runs.
- **State is current truth.** The interrogator did not just append a note that the goal
  changed; it edited `purpose.md` and closed the stale question. A knowledge base that
  contradicts itself is worse than one that stayed quiet.
- **The read-only line held the whole way.** No skill queried a database, computed NRR,
  or wrote the production SQL. `groundwork` profiled a static file, `kpi-contract` pinned
  what the metric *means* and flagged what it could not know, `review-my-query` reviewed
  the inherited view without running it and pointed the fix direction instead of handing
  back a rewrite, `defend-my-number` surfaced the gap instead of crunching it,
  `brief-my-findings` wrote the readout without computing a number or rendering the board
  deck, and `triage-my-number` diagnosed the production spike without computing the sample
  it was handed. The number 108% is never calculated here; it is defined, contracted,
  reviewed, pressure-tested, and briefed.
- **The honest ending is the feature.** The chain ends in "reframe," two `[needs
  decision]` forks, and a "not yet" that the findings brief carries into the board readout
  itself rather than smoothing away. That is the bench doing its job: surfacing what a
  single confident pass would have shipped straight to the board.

## Run it yourself

With the analytics-office plugin enabled in Claude Code, from a copy of this folder:

1. Point **groundwork** at `inputs/vw_monthly_churn.sql` and `inputs/metrics_notes.md`:
   "I inherited this, help me get oriented." It builds the knowledge base.
2. Hand **requirements-interrogator** the request in `inputs/vp_request.md`.
3. Ask **kpi-contract** to lock the metrics the brief reframed to.
4. Ask **review-my-query** to review `inputs/vw_monthly_churn.sql` against the locked
   contract: "is this query right?" It grades the findings, no rewrite.
5. Give **defend-my-number** the claim in `inputs/the-number.md` and rehearse.
6. Ask **brief-my-findings** to "write up the findings brief for the board" from the
   knowledge base. It carries the "not yet" verdict instead of smoothing it.
7. When the inherited view spikes in production, ask **triage-my-number** "why is this
   number wrong?" It runs the differential, reaches for the known defects as suspects, and
   gives a calibrated holding line, no compute.

Each skill self-routes from how you phrase the ask; there is no router to configure. The
knowledge base you end with should look like the one in [`knowledge-base/`](knowledge-base/).
