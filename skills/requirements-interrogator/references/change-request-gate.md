# The change-request gate — mode of requirements-interrogator

Load when the ask is a MID-FLIGHT CHANGE ("can you also add ___", "small tweak while
you're in there", "just include reactivated customers too") against work underway or
contracts already locked. The interrogation still runs (what decision does the change
serve?) — this mode adds the delta ledger and the forced disposition. No change is
absorbed silently; "small" is a claim the ledger tests.

## The delta ledger

```markdown
## Change request — <the ask, verbatim> (<from whom, date>)  [Define]
_Gated <date>, by <who>. Interrogation verdict: <the real job behind the ask>._

| Delta dimension | Assessment |
|---|---|
| Scope | <what is actually being added/changed, precisely> |
| Effort | <order of magnitude + what it displaces> |
| Dependencies | <new sources, owners, upstream asks> |
| **Contracts touched** | <kpi-contract vN clause? model-contract grain/dim? NONE — verified, not assumed> |
| Downstream | <reports/consumers affected — route to change-impact if non-trivial> |

**Disposition: ACCEPT / DEFER (until <when/condition>) / REJECT** — owner: <named>,
rationale: <one sentence>. → recorded in `knowledge-base/decisions.md`, dated, by:.
```

## The contract-touch checklist (the part answer-mode skips)

For each locked artifact in the KB: does the change reopen a pinned definition (a new
population = a DIFFERENT metric → kpi-contract re-version, not a quiet edit)? Shift a
declared grain or add a dimension (model-contract re-version)? Invalidate a derived test
spec line? Touching a locked contract NEVER happens silently — the contract's owner is in
the disposition line.

## Routing on ACCEPT
- Non-trivial downstream surface → `change-impact` (the blast radius, before the build).
- A touched metric definition → `kpi-contract` (re-version with the owner).
- The scope delta → the next `status-truth` report (a re-base is named as a re-base).
- The disposition itself → `decisions.md` (owner-pinned, dated); the request artifact gets
  a dated copy in `inputs/` if it arrived as a file/ticket.

A scope creep stopped at the gate (the "small tweak" that would have reopened a locked
grain) appends one line to `knowledge-base/catches.md`.
