# Completeness Models (per project type)

The guide's *thinking* layer: what a full understanding of each project type requires. Compare what's known against the relevant list and flag empty slots. Comprehensive checklist, lean output — a thorough check never means a bloated KB.

## How to use
1. Classify the project type (ask if unclear). 2. Load that list. 3. For each item, mark known / unknown. 4. Unknowns → `open-questions.md`; known facts → the relevant core file.

## Type A — Inherited data estate
- **Purpose** — business process served; who/what consumes outputs.
- **Data flow** — sources → transformations/business logic → targets (queries, procedures, pipeline data flows).
- **Lineage & dependencies** — object DAG (scheduled job → pipeline/package → query/procedure → table), upstream/downstream.
- **Orchestration** — schedule, run order, triggers.
- **Reliability** — failure handling, restartability, data freshness/latency, alerting.
- **Structure** — grain & keys of the important tables.
- **People & risk** — owners/contacts; known gotchas (hardcodes, manual steps); access/PII.

## Type B — New reporting / KPI request
- **Decision** — what decision/action it supports; who acts; cadence.
- **Real need vs stated ask** — separate requested solution from underlying need (XY problem / 5-whys).
- **Metrics** — definition, formula, grain, dimensions, threshold/target per metric.
- **Data feasibility** — does the data exist at the needed grain; which sources.
- **Consumers & distribution** — who uses it, how, where it lives.
- **Acceptance** — success criteria; definition of done.
- **Constraints** — refresh cadence, security/PII, performance.

## Type C — Migration / modernization
- **Scope** — what's in/out.
- **Source understanding** — apply the Type A list to the source.
- **Target** — destination platform, capabilities, gaps vs source.
- **Parity & validation** — how correctness is proven (reconciliation strategy).
- **Cutover** — sequencing, downtime, rollback.
- **Affected dependencies & consumers.**
- **Risks/gotchas** — behavior/semantic differences between source and target platforms.

## Type D — New pipeline / integration
- **Source system** — what it is, owner, access, grain, keys, volume, change-capture.
- **Data contract** — schema, semantics, SLAs, freshness expectations.
- **Target model** — where it lands, grain, conformance.
- **Transformations / business rules** needed.
- **Orchestration & scheduling** plan.
- **Reliability** — failure handling, idempotency/restartability.
- **Consumers & acceptance.**
