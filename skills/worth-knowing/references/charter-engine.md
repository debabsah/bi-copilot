# The charter engine — lenses, rubric, worked example

How candidates get generated, ranked, and phrased. The artifact template lives in
`question-charter.md`; this file is the thinking behind it.

## The four generation lenses

Run all four, in this order. Each lens produces candidates the others structurally
miss; a charter built from one lens has a shape you can predict — and so can the
stakeholder.

**1. Decision-backwards (the anchor lens).** For each decision elicited in loop
step 3: *what question, answered, would change what this person does?* These
candidates arrive pre-anchored — decision, actor, cadence all named. Most of the
top tier comes from here.

**2. Estate-forwards (the curiosity lens).** For each source in the inventory:
*what could this data inform that nobody has asked about?* Order history nobody has
segmented, timestamps nobody has turned into durations, linkages nobody has joined.
This is where legitimate curiosity-tier candidates come from — and where feasibility
is cheapest to cite, because the lens starts FROM the data that exists.

**3. Outside-in (the experience lens).** What do organizations of this shape usually
need to know — retention before acquisition for subscription businesses, dilution
checks where discounting is heavy, capacity questions where service queues exist?
Honest label: this lens borrows from pattern, not from this estate. Its candidates
must still pass the feasibility citation before they enter the charter, and they
anchor only if a real elicited decision claims them.

**4. The unasked (the mandatory lens).** Invert the stakeholder's stated beliefs
into testable questions. Every confident claim heard in elicitation ("support is
overstaffed", "enterprise is where the growth is") is a hypothesis someone is
already betting on without data — which makes its test the highest-value question
in the room and the least likely to be requested. At least one candidate from this
lens, or a written reason why none exists. Unwelcome-answer potential is a feature,
stated plainly, not an apology.

## The ranking rubric (printed on every charter)

Three axes, graded H/M/L, criteria stated in the charter's own words:

- **Decision-weight** — what changes if this is answered, who acts, how soon. An
  answer nobody would act on this quarter is L regardless of how interesting it is.
- **Feasibility** — is the required data cited as available (vs UNVERIFIED), does
  its grain match the question, does the history go back far enough. UNVERIFIED
  dependencies cap feasibility at M and the verification check becomes part of the
  candidate's path.
- **Effort** — paste-back cuts on existing extracts (L effort) vs new joins or
  definitions needing a contract first (M) vs instrumentation that doesn't exist
  yet (H).

Sort order: anchored before curiosity, always; then decision-weight; then
feasibility; then inverse effort. Ties go to the stakeholder — that's a real
question for the session, not a coin flip. The rubric never reorders silently
between re-fires: a rank change names which axis moved and why.

## Candidate anatomy (every entry, no exceptions)

```
Q3. Do week-one activation rates predict month-six retention?
    Tier: ANCHORED — onboarding-investment decision (Head of CS, quarterly)
    Expected shape: HYPOTHESIS — no data examined. If activation predicts
      retention, early-warning intervention becomes worth pricing.
    How to read: a stable difference in retention between activation cohorts,
      on bases large enough to matter — not a correlation headline.
    Confirms via: explore-my-data — pre-registered cohort cut, user runs and
      pastes back; a causal claim would need a design (audit-my-experiment).
    Data: telemetry weekly seats (cited: platform team note 2026-06-07) ×
      billing end-dates (cited: same) — JOIN feasibility UNVERIFIED until keys
      are confirmed.
    Effort: M (two extracts + a key check).
```

The phrasing discipline: the question is a question; the expected shape says what
WOULD follow if it confirms, never what "will" be found; the confirmation path
names the room that runs it. If a sentence about a candidate could be quoted as a
result, rewrite it until it can't.

## Worked example (synthetic)

Engagement: a 40-location climbing-gym chain, "we have all this membership data
and no idea what to do with it." Elicited landscape: one decision-maker (COO),
two live decisions — winter staffing levels (monthly) and whether to keep the
10-visit punch pass (annual renewal negotiation, October).

The four lenses produced eight candidates; the charter's top three:

1. **Q1 (ANCHORED, H/H/L).** Do punch-pass holders convert to memberships or
   substitute for them? — the punch-pass decision's load-bearing question. Data:
   POS pass sales × membership starts, both cited available. HYPOTHESIS: if
   substitution dominates, the pass is cannibalizing; if conversion dominates,
   it's a funnel. Either answer changes the October call.
2. **Q2 (ANCHORED, H/M/M).** Does visit-time concentration justify the current
   staffing curve? Check-in timestamps cited; staffing roster UNVERIFIED (HR
   export never confirmed) — feasibility capped at M, verification check written.
3. **Q7 (THE UNASKED, H/M/M).** The COO "knows" weekday mornings are dead and
   wants them cut from staffing. Q7 tests it: morning visits by member tenure —
   if long-tenure members concentrate there, the dead slot may be the retention
   slot. Unwelcome answer possible; stated.

Two curiosity candidates (Q5 route-setting cadence vs visit frequency; Q8
seasonal joiner cohorts) ranked below every anchored item. One outside-in
candidate was DECLINED by the COO and stays on the charter as declined, with the
reaction logged — the next analyst inherits the whole conversation, not the
surviving half.
