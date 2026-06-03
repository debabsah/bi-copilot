# Frameworks — requirements-interrogator

Depth for the discipline. Load when interrogating a request. The named frameworks aren't decoration — they're what a stakeholder recognizes as principal-level rigor, and they're mostly uncited by the tools competing in this space.

## Decision-backwards (the gate)
Every metric exists to change an action. If it changes none, it's a vanity metric.
- "What **decision or action** changes based on this number?"
- "**Who** acts on it? At what **cadence** (daily / weekly / quarterly)?"
- "What would you do differently if it were high vs low?"

If none of these have an answer, stop the build and say so. Cadence also sets grain: a quarterly decision rarely needs a daily-refresh dashboard.

## XY Problem (separate the ask from the goal)
The stakeholder asks for **Y** (their guessed solution) when they actually need **X** (the goal). They lead with Y because Y is concrete and X is fuzzy.
- Y = "a dashboard with DAU, session length, bounce rate."
- X = the thing Y is *for*: "decide whether to keep investing in Feature A next quarter."
Name both explicitly. Most bad BI is a perfectly built Y for an unexamined X.

## 5 Whys (drive to the root need)
Ask "why do you need that?" on the goal, not the metric, until the answer stops moving.
- Don't stop at the first plausible business reason — that's usually still a proxy.
- Stop when the next "why" only restates the last answer, or reaches a decision someone is accountable for.
- Watch for the jump from a *reporting* need ("so I can see it") to a *decision* need ("so I can act"). Only the second one justifies the work.

## Jobs-to-be-Done (lock the need in one sentence)
> "When **[situation]**, I want to **[motivation]**, so I can **[expected outcome]**."

Example: "When I'm planning next quarter's roadmap, I want to know if Feature A is retaining the users it attracted, so I can decide whether to fund it further." Get the stakeholder to confirm the sentence verbatim — it's the contract for what "done" means.

## The vanity-metric test
A metric is vanity if any of these hold:
- No decision changes based on its value (failed the gate).
- It can only go up, or is always reported as "growing," with no threshold for action.
- Nobody can name what they'd do if it moved against them.
Flag it as such in the brief. A flagged vanity metric is a finding, not a failure.

## Re-derivation and the delta (the signature move)
This is what separates the skill from good clarifying questions. Do it explicitly, on paper.
1. From the **validated JTBD + decision**, derive the metric(s) that *actually* answer it — ignore what was requested.
2. Lay the two sets side by side:

| As requested | Decision-derived | Gap |
|---|---|---|
| Daily active users | Feature-A 30-day retention cohort | requested metric doesn't isolate Feature A |
| Avg session length | (not needed for this decision) | vanity for this decision |
| Bounce rate | Feature-A activation rate | proxy at best; activation is the real leading signal |

3. The gap drives the **verdict**: identical → *proceed*; same goal, different metrics → *reframe*; the request can't move the decision → *wrong-problem*.

## Two operating modes
- **Live** — you have the stakeholder or their answers. Interrogate interactively, one question at a time (or batched for an experienced user), and fill the brief as you go.
- **Prep** — you don't have them yet. You **cannot invent their answers.** Produce the interrogation as a script: the exact questions in order, phrased as confirm-the-default where possible ("Reading this as X — correct?"), so the meeting takes minutes, not a quiz. The brief comes back half-filled with `[awaiting stakeholder]` markers.

## Requirements Brief — template
A one-page, committable Markdown artifact. Lives at `knowledge-base/requirements-brief.md` if a KB exists, else next to the ticket. Phase-tag the heading `[Define]`.

```markdown
# Requirements Brief — <request name>  [Define]

- **Requestor / date:** <who, when>
- **As-requested (the solution Y):** <verbatim ask: metrics, dashboard, report>
- **Real decision (X):** <what action changes, who acts, what cadence>
- **Root need (JTBD):** When <situation>, I want to <motivation>, so I can <outcome>.
- **Success & threshold:** <what "good" is; the number that triggers the action; current baseline>
- **Feasibility note:** <does the data plausibly exist? plain-language only>

## Decision-derived metrics vs as-requested (the delta)
| As requested | Decision-derived | Gap |
|---|---|---|
| ... | ... | ... |

- **Open questions for the stakeholder:** <the ones still unanswered / for prep mode>
- **Verdict:** proceed | reframe | wrong-problem — <one line of why>
```

On a **proceed** or **reframe** verdict, carry the decision-derived metrics into `kpi-contract.md` (per the KB catalog: definition, formula, grain, dimensions, source, owner, refresh, threshold, caveats, version, effective-date) so the definitions get locked before build. On any verdict, append the interrogation to `timeline.md` and record a **reframe**/**wrong-problem** call (with rationale and rejected alternative) in `decisions.md`.

## Authority anchors (cite when it helps the stakeholder trust the method)
- **The XY Problem** — building the asked-for thing instead of the needed thing.
- **Jobs-to-be-Done** (Christensen) — people "hire" a metric to make progress on a job.
- **5 Whys** (Toyota) — root-cause laddering.
- **The Mom Test** (Fitzpatrick) — ask about their life and decisions, not about your proposed solution; people lie politely about solutions, not about what they actually do.
