# Worked example: one project, end to end

This is the analytics-office bench run end to end on a single project, so you can watch
the disciplines **compose through a shared knowledge base** instead of just reading
that they do. This walkthrough threads **all nineteen disciplines** on one project, in two acts:
one notices something while reading inherited SQL, and a full lifecycle later that same
something is what keeps a bad number out of the board readout.

> **Meridian is a fictional B2B SaaS company.** Every account, name, and number here
> is invented for this example. Nothing is queried or computed; the skills read text
> and write Markdown, which is the whole point.

The reader-facing artifacts are real files you can open:

- [`inputs/`](inputs/) - the raw material you start with (an inherited SQL view, a
  departed analyst's notes, a stakeholder request, a number to defend).
- [`knowledge-base/`](knowledge-base/) - what the nineteen disciplines produced and kept
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
| 8 | worth-knowing | Define | "what can our data tell us?" + six months to the budget call | the question charter: 6 anchored candidates, the unasked one testing Priya's own conviction | question-charter, open-questions, timeline |
| 9 | explore-my-data | Understand | charter candidate Q1, routed | pre-registered cuts, then graded results: Exploratory-found, a pending grade, a recorded dead end | exploration-log, timeline |
| 10 | audit-my-assumptions | Audit | the billing extract everything will be built on | a 10-row register; A9 catches the Act-I Finance gap about to be re-inherited | assumption-register, open-questions, timeline |
| 11 | map-my-estate | Understand | the view SQL + verbal source knowledge | the cited map: 9 evidenced edges, 1 dashed [unverified], islands kept | estate-map, open-questions, catches, timeline |
| 12 | model-contract | Design | the locked contracts + the map + the register | a star with the grain declared and the build GATED on unresolved sources | model-contract, timeline |
| 13 | change-impact | Operate | "RevOps ships billing_export_v2 Tuesday" | NOT safe to ship: 3 silent drifts (the 0-rows filter = NRR 100%% at the board), 6 pre-flight checks | change-impact, catches, kpi-contract (amendment), timeline |
| 14 | prove-my-parity | Validate | the shipped migration + a tolerance pinned before results | PARITY, stratified: 9 strata, offsetting computed false, residuals classified | parity-proof, timeline |
| 15 | audit-my-experiment | Validate | "the pilot won - make it sing" | the write-up refused: peeking kills nominal significance; activation is a proxy, not churn | experiment-audit, timeline |
| 16 | audit-my-forecast | Validate | Finance's churn forecast for headcount | point path beats naive 2.1x; intervals claim 80%%, deliver 50%% - plan blocked on the bands | forecast-audit, timeline |
| 17 | review-my-dashboard | Audit | the rebuilt dashboard, pre-ship | do not ship as-is: 4 Blocking, incl. "(validated)" on the gated pilot | dashboard-review, timeline |
| 18 | status-truth | Deliver | "keep it green" + the actual record | AMBER, pressure recorded; greens earn their color, ambers carry owners | status-report, timeline |
| 19 | kb-reconcile | Audit | the whole accreted record, pre-readout | 3 Blocking drifts the story itself created; the parity verdict's re-audit clock caught ticking | reconcile, timeline |

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

### Act II - from readout to budget evidence (skills 8-19)

The board took the honest "not yet." Act II is the six months that follow: turning an
honest readout into evidence for the onboarding-budget decision. Every artifact below is
**verbatim output of real runs on claude-sonnet-4-6** against this growing knowledge
base, lightly trimmed for length - not authored prose.

**8. worth-knowing.** Priya: "I'm convinced onboarding is our problem... what can our data
tell us?" The charter anchors six candidates to the budget decision - and its mandatory
*unasked* candidate (Q6) tests Priya's own conviction: onboarding execution, or
acquisition fit? "The question with the potentially unwelcome answer. It belongs on the
charter for exactly that reason."

**9. explore-my-data.** Q1 arrives pre-registered from the charter and the log adopts it
verbatim - then gates itself on Act I's own record ("do NOT touch vw_monthly_churn:
query-review Blocking #4"). When results come back it grades +17.2pp over the bar as
*Exploratory - found*, *refuses* to grade the tier split because the paste-back lacked
per-tier baselines, and records the vintage cut as a dead end "so the next explorer
doesn't re-walk it."

**10. audit-my-assumptions.** Ten rows on the billing extract; the killer is A9: does
the extract share Finance's source? If not, "the mart will inherit the same unresolved
board-level gap that made vw_monthly_churn un-presentable - building the gap twice, at
larger scale." The Act-I thread, caught about to propagate.

**11. map-my-estate.** Marcus says "I BELIEVE the CRM syncs on account_id but never
checked" - the map renders that edge dashed `[unverified]`, keeps usage_events as an
island, and logs four refused fabricated edges to catches.md.

**12. model-contract.** The star is designed but the build is GATED: source grains
unprofiled, and `dim_account.segment` declared unreliable until the map's dashed edge is
confirmed. The design respects what the record doesn't know.

**13. change-impact.** RevOps announces billing_export_v2. The #1-ranked finding isn't
the loud one: the event_type rename means every movement filter "runs without error and
returns 0 rows. NRR = 100%% for all cohorts. No alert fires. This is the failure mode
that passes QA and surfaces at the board." Verdict: not safe to ship; six pre-flight
checks; post-change tie-out routed to prove-my-parity with the strata named.

**14. prove-my-parity.** The tolerance was pinned in writing four days before results.
Nine strata, offsetting flag computed false, the 63-row count delta fully explained by
the documented backfill boundary. PARITY - with a re-audit condition that will matter
later.

**15. audit-my-experiment.** "The pilot won - make it sing." SRM passes (the
randomization was fine); the peeking check doesn't: seven weekly looks on a ten-week
plan, and nominal p=0.049 does not survive sequential correction. "The write-up cannot
proceed." And activation is a proxy - 90-day churn, the actual decision metric, is
unmeasured. What would clear it is specified, not vibed.

**16. audit-my-forecast.** Finance's model beats naive by 2.1x - credit where due - but
its 80%% intervals cover 6 of 12 months, and five of six misses breach the *upper*
bound: precisely the understaffing direction the headcount plan cares about. Point path
usable; nobody plans against the bands until they're recalibrated.

**17. review-my-dashboard.** Four Blocking assembly lies over individually-correct
parts: the YTD card sums monthly distinct counts, "all customers" titles a
Starter-excluded default, "live" subtitles a Monday extract - and "(validated)" decorates
the pilot chart that experiment-audit just gated. The claim is routed back to the gate
that refused it.

**18. status-truth.** "Keep it green - I don't want wobble." The first line of the
response records the pressure; the status ships AMBER, every green carrying its
criteria, every amber its owner - because "a green that detonates in September's budget
room is the worst outcome."

**19. kb-reconcile.** The finale audits everything above, three weeks before the next
readout - and every drift it finds was created naturally by the story: the open question
still labeled "blocking the 2026-06-10 meeting" forty days later, the estate map
predating v2's ship by five weeks, the parity verdict's re-audit clock firing at the
July close. The record corrects itself before the room quotes it.

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

And the same gap keeps traveling through Act II:

```
audit-my-assumptions (Audit)       A9: does the new mart's extract share Finance's
                                   source? "Building the gap twice, at larger scale."
                                   The build is gated on the answer.
        |
        v
status-truth (Deliver)             The gap appears in the steering asks with an owner -
                                   not smoothed into the green narrative.
        |
        v
kb-reconcile (Audit)               D1, Blocking: the question still says "blocking the
                                   2026-06-10 meeting" - 40 days past, outcome unrecorded.
                                   The stale label would have read as resolved. Fixed
                                   before the August deck is built on it.
```

One throwaway line in a departed analyst's notes, carried by ten different skills across
five months, never silently dropped, never quietly upgraded - and still honestly open.
That is what a living knowledge base is for.

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

**The seams are load-bearing, not decorative.** Act II exercised the bench's wired
hand-offs for real: the explore log adopted the charter's pre-registration verbatim and
recorded its outcome for the charter to sync; the mart design read the estate map's
dashed edge and gated on it; the blast radius named prove-my-parity's strata before the
migration shipped; the dashboard's "(validated)" was routed back to the exact audit that
had gated it.

**A weaker model held the discipline.** Act II was executed end-to-end on
claude-sonnet-4-6, not the strongest available model - deliberately. The structure did
the work: pre-registration before results, tolerances before comparisons, pressure
recorded before composing. Discipline that survives the weaker executor is structure,
not model heroics.

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
