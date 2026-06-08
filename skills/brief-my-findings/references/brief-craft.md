# Findings-brief craft — the engine

Load when building the claim ledger (loop step 3). Two jobs: ledger every claim, then compose the brief without smoothing. Comprehensive thinking, lean output: the brief carries only what the decision needs, but every line of it is sourced.

## The status rubric — grade by what the evidence supports, not by what lands
- **Supported** — backed by a validated or reconciled finding (a locked contract figure, a reviewed query, a reconciled number). Can be stated plainly.
- **Directional-only** — the evidence points one way but is not yet reconciled or validated. Say "directional"; never "certified". A number that has not cleared its reconciliation is Directional, not Supported, however good it looks.
- **[Open - needs decision]** — a fork the contract left open, an unreconciled gap, a cut not yet built. It stays open in the brief. You report that it is open and why it matters; you do not resolve it in prose.
- **Inferred** — your reasoning beyond the data. Allowed only when labeled as inference, and only when it helps the decision; never dressed up as a finding. An external benchmark nobody measured is not even Inferred — it has no provenance, so it is cut.

## Qualifiers travel with the figure (the anti-laundering rule)
A status tag is not enough — the number's **qualifier** must ride with it as part of the figure, or a soft estimate reads as a hard fact by the time it hits the slide. The closed set:
- **Interval / error band** (±, 95% CI) — for an *estimate* only.
- **Denominator / base** (n=, the population the rate is over).
- **Measurement-scope caveat** — window + filter ("first-90-day only", "excludes refunds", "US accounts").

**Estimate vs exact (so the rule doesn't cry wolf):** an *estimate* (sampled / modeled / projected / a rate with sampling error) carries a mandatory interval; an *exact* figure (full-population count, ledger total) needs no interval but still carries its base and scope. The trigger is a **dropped** qualifier, not a missing-by-nature one — if the figure *arrived* with a CI/n/scope (from the analysis or `audit-my-experiment`'s handoff) and the brief would strip it, that is laundering: keep it. A bare estimate whose interval/base/scope is **unknown** is `[Open]` (not yet sayable as a hard fact), never one the brief invents — read-only: carry the qualifier the analysis produced; never compute or widen one. Anchor the denominator/scope to what `kpi-contract` already defined — the brief ensures it rides along, it does not redefine it. When the figure came from `audit-my-experiment`, carry its CI **and** its materiality verdict (`material` / `immaterial` / `straddles-MME`) — both are part of the number's honest statement.

**Carrying it onward (instruct, don't render).** The brief keeps each figure's qualifier verbatim; because the slide/email is the user's to write, the brief does NOT draft it — it adds a one-line handoff instruction ("carry the ±/n/scope onto the slide; do not drop it in the deck") so stripping the qualifier downstream is a visible, named choice, not a silent one.

## Building the claim ledger
For every sentence the brief will assert, ask **"says who?"** and attach the source and status before it earns a place. A claim that cannot name a source is cut or demoted to an open item. Two failure shapes to catch in yourself:
- **The smoothing reflex:** an open gap is uncomfortable in a brief, so the instinct is to explain it away ("the gap is just timing / just new logos"). If the KB marks it `[needs decision]`, that explanation is a finding you are inventing. Keep it `[Open]`.
- **The confidence upgrade:** a recommendation reads stronger without the caveat, so the caveat quietly drops. Carry the verdict and the status exactly as the analysis graded them.

## Composing without smoothing
Shape each finding as **observation → implication → action → watch-for**:
- **observation** — what the analysis found (with its status tag).
- **implication** — what it means for *this decision* (not a generic restatement).
- **action** — what to do or recommend; if the verdict is "not yet", the action is to close the open item, not to recommend.
- **watch-for** — what would change this, and the pushback to expect. This is the bridge to `defend-my-number`: today's watch-for is tomorrow's rehearsed attack.

Quarantine the `[Open]` items in their own "what is still open" section so they are impossible to miss and impossible to smooth. Lead the brief with the bottom line at the confidence the evidence supports — including "not yet" when that is the verdict.

## Audience calibration (keep it light)
- **Exec / board:** lead with the decision and its readiness; one line per finding; the open items and the carried verdict are the point. Define a metric only if a fork would otherwise be misread.
- **Technical peer:** the same ledger, but you can keep the method detail (definitions, the query-review findings, the reconciliation bridge status) in the body rather than an appendix.
Either register, the provenance/status discipline is identical; only the prose depth changes.

## Worked example — the Meridian board brief done right
Inputs on hand: NRR 108% (up from 102%) and gross revenue churn 4.2% from the locked contract; `query-review` retired the inherited logo view (4 Blocking); `defense-sheet` verdict "not yet" — the Finance reconciliation cracked, the early-life cohort cut wobbled. The disciplined brief:

```markdown
# Findings Brief — onboarding-team vs new-logo-growth funding call  [Deliver]
_Briefed 2026-06-04. For: the board (ex-CFO reads numbers closely). Decision: where next year's CS budget goes._
_Built from: kpi-contract v1.0 · query-review · defense-sheet · open-questions._
Read-only: composed from evidence on hand; no number computed; nothing manufactured.

- **Bottom line:** retention is trending up, but the recommendation is **not yet defensible** — two items must close first.

## Findings
1. **NRR is 108% (cohort n=412 starting accounts; trailing-12-mo; excludes trials), up from 102% a year ago** `[Directional-only : kpi-contract — not yet reconciled to Finance]`
   - Implication: the existing base is growing on its own, which would favor funding growth over onboarding.
   - Action: hold the recommendation until the reconciliation closes (below).
   - Watch-for: "Finance says revenue grew ~2%, you say 108% — which is wrong?"
   - **Carry onto the slide:** the n=412 base and the trailing-12-mo / excludes-trials scope ride with the 108% — a bare "NRR is 108%" on the deck is the laundering this brief prevents.
2. **The prior board churn number came from a view that measured the wrong thing** `[Supported : query-review, 4 Blocking]`
   - Implication: past slides understated revenue loss; the change in numbers is a fix, not a goalpost move.
   - Action: state plainly that the metric was corrected and re-based.
   - Watch-for: "Did you move the goalposts since last year?"

## What is still open / not yet sayable
| # | Open item | Status | Why it matters | Owner |
|---|---|---|---|---|
| 1 | NRR-to-Finance reconciliation bridge | Open | the board will compare the two; an unexplained gap sinks the number | Finance + RevOps |
| 2 | early-life (first-90-day) churn by cohort | Open | the funding call turns on it; blended NRR hides it | this team |

## Readiness
- **Verdict carried:** not yet. Do not present the recommendation until items 1 and 2 close.
- **Confidence:** finding 2 is Supported; the 108% is Directional-only until the reconciliation lands.
```

What the brief does NOT do: it does not explain the Finance gap away (item 1 stays Open, not "it's just new logos"), it does not state "fund growth" as the recommendation (the verdict is carried as "not yet"), and it invents no benchmark. It locates, sources, grades, and carries — the analyst closes the open items, then briefs again.
