# Artifact template — assumption-register.md

The one file this skill writes (loop step 6). It is the pre-flight record: every inherited premise the build rests on, graded and statused, with the check or the owner-question that settles each. It hands off to the build only once the trunk rows are VERIFIED or consciously accepted.

## Template

```markdown
# Assumption Register — <deliverable> from <source(s)>  [Audit]
_<date>. Sources audited: <proc / query / export / workbook> (the generative anchors).
The build does not proceed on an unvalidated TRUNK row._

## Sources & their authority
- <source A> — authoritative for <what it computes>; NOT for <currency / intent / fitness>.
- Anchor hierarchy used: live system > generative code > windowed export > workbook.

## Register
| # | Assumption (with cite) | Blast radius | Settled by | Status | Evidence / the exact check |
|---|---|---|---|---|---|
| A1 | <statement> — `file:line` / verbatim | TRUNK / leaf | Verifiable / Decision | VERIFIED / ASSUMPTION / FALSIFIED / NEEDS-DECISION | <the run, or the owner question> |
| A2 | … | … | … | … | … |

## Trunk rows still open (gating — do not build past these)
- **A_n (NEEDS-DECISION → owner):** <the intent question, named owner>.
- **A_m (VERIFIABLE → run):** <the exact query/profile to run, and what result confirms vs falsifies>.

## Trend / falsification run
- Population profiled over time? <by-year counts; any structural break + the year it breaks>.
- Triangulated figure(s): <second derivation, agree/diverge>.
- Anchored to generative source (not a derivative)? <yes/what>.

## Seam tie-outs to run during the build
- source → export: <totals match on the matching scope/basis?>
- export → your query: <ties at the boundary before any new transform?>
- your query → output: <headline reconciles?>

## Verdict
<Foundation cleared / N trunk rows gating. The build may proceed on A1, A3 (verified);
A2, A5 must be answered by <owner> first. This register is the pre-flight, not the build.>

**Re-verify when:** <what invalidates the cleared foundation — the source proc changes, a
new period lands, the recording process shifts. A cleared foundation has a shelf life.>
```

## How it composes into the knowledge base
- **Reads** (if a `knowledge-base/` exists): `kpi-contract.md` (a pinned definition retires the matching assumption), `decisions.md` (a settled call is not re-litigated), `landscape.md` / lineage (what the source actually is).
- **Writes** the register to `knowledge-base/assumption-register.md`; escalate each **gating trunk** row to `open-questions.md`, route any definition gap to `kpi-contract`, and append `timeline.md`. The audited sources get dated copies in `inputs/` (`YYYY-MM-DD-<name>`) so the register's cites survive.
- **Hands off**: once the trunk rows clear, the build proceeds — and a confirmed code-level concern goes to `review-my-query`, a wrong number that slips through to `triage-my-number`. This skill is the front door; those are downstream.
- No KB anywhere up-tree? Create `knowledge-base/` now with the register + stub `README.md` index, routing notes inside it (`groundwork` can flesh it out later) — the next build inherits this one's cleared foundation.
- When the office is git-tracked, offer the commit — `kb(audit-my-assumptions): <deliverable> register — <verdict>` — one artifact, one commit (the git-native convention in groundwork's kb-core-templates).
