# Which skill, when — the human routing map

The skills route themselves from your natural phrasing; you never need this page to use the
bench. It exists for the moments a human wants to *choose* deliberately — the seams where
two skills sound alike but do different jobs.

## The four families

Every skill belongs to one family, and its description opens with the family's shared
stanza — the family carries the heavy discrimination, members discriminate within it:

| Family | The ask-shape | Members |
|---|---|---|
| **Shape** | the work itself is still being shaped, before anything is built | groundwork · requirements-interrogator · kpi-contract · model-contract |
| **Audit** | a finished thing is about to be trusted; the gate fires first | audit-my-assumptions · audit-my-experiment · audit-my-forecast · review-my-query · kb-reconcile |
| **Investigate** | hands-in-the-data right now | triage-my-number · explore-my-data · map-my-estate |
| **Deliver** | work is leaving the desk | brief-my-findings · defend-my-number · status-truth |

## The three gate questions

**1. Is there a symptom in hand?**
- A number is already wrong, suspicious, or moved unexpectedly → **triage-my-number**
  (the 5-branch differential: code / data / pipeline / definition / real change).
- No symptom — you're *about to* build on or present something whose premises were never
  examined → **audit-my-assumptions** (preventive, upstream; the clean unremarkable number
  is the primary case, not the edge case).

**2. What kind of thing is being validated?**
- A controlled A/B or causal result ("is this lift real?") → **audit-my-experiment**
  (SRM, peeking, multiplicity, power — computed, not eyeballed).
- A forecast or projection ("will this hold?") → **audit-my-forecast**
  (leakage, backtest validity, interval honesty, drift).
- One piece of code against a definition ("is this query right?") → **review-my-query**.
- The whole accreted record ("is what we wrote down still true?") → **kb-reconcile**.

**3. Which present-moment job is it?** (the trio that sounds alike)
- *"What am I assuming under this number?"* → **audit-my-assumptions** (premises).
- *"How do I write this up?"* → **brief-my-findings** (phrasing — one pass, one artifact).
- *"How do I hold up under live challenge?"* → **defend-my-number** (pushback — a
  stateful, escalating drill).

## The full bench by moment

| Moment | Skill | The one-line job |
|---|---|---|
| Starting blind | `groundwork` | orient on an estate, stand up the living knowledge base |
| A solution-shaped request arrives | `requirements-interrogator` | drive the ask back to the decision; requested-vs-derived delta |
| A metric needs one meaning | `kpi-contract` | pin every definitional fork; owner pins or `[needs decision]` |
| A mart needs structure | `model-contract` | declare the grain, gate on source grain, log the modelling forks |
| About to build on / present unvetted inputs | `audit-my-assumptions` | excavate, grade, falsify the silent premises first |
| Code behind a number, pre-ship | `review-my-query` | graded findings against the contract; review, never rewrite |
| An A/B result heading to a decision | `audit-my-experiment` | compute the validity checks; gate the ship |
| A forecast heading into a plan | `audit-my-forecast` | leakage/backtest/interval/drift; gate the plan |
| A number is wrong in production | `triage-my-number` | hold the differential; calibrated holding line for the room |
| The record itself needs trusting | `kb-reconcile` | reconcile every claim against its source; graded drift report |
| Findings need communicating | `brief-my-findings` | every claim carries provenance; open stays open |
| The meeting will push back | `defend-my-number` | rehearse under escalating attack; defense sheet of what cracked |
| The weekly status is due | `status-truth` | the provenance-graded status report — greens earn their color, slips carry their delta |
| An open-ended "find insights" look at data | `explore-my-data` | pre-registered, cut-counted exploration; found ≠ confirmed |
| The estate needs drawing (ER / lineage) | `map-my-estate` | the cited map — evidence-graded edges, honest gaps |

## Common confusions, settled

- **"Two numbers don't match"** — with a query in hand to check → `review-my-query`; as a
  production mystery ("find what's driving the gap") → `triage-my-number`; as a
  *definition* dispute ("Marketing and Finance define it differently") → `kpi-contract`.
- **"Validate this"** — an experiment → `audit-my-experiment`; a forecast →
  `audit-my-forecast`; a source you'll build on → `audit-my-assumptions`; the KB →
  `kb-reconcile`; a request → `requirements-interrogator`.
- **"Write up the win"** — if the result was never audited, the audit fires FIRST (the
  consumption ask does not skip the gate); brief composes only vetted findings.
- **"Catch me up" / "where did we leave off"** → `groundwork` (resume mode reads the
  timeline and briefs you).

There is no pipeline: every skill fires independently, at any moment, with or without the
others having run. The order above is a story, not a sequence.
