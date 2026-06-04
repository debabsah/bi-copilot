# Modelling forks: checklist, primer, template, worked example

Loaded on demand by `model-contract`. The fork checklist is the engine; the primer is the why; the template is the committable artifact; the worked example shows it end to end.

## The modelling-fork checklist
Walk every row. Each ends pinned (with a one-line rationale), `[needs decision: owner]`, or "N/A because ___". A silent skip is the bug this skill exists to beat.

| Fork | Options | Why it moves the build |
|---|---|---|
| **Source grain (per source) - the gate** | one row per business event / per status change / per snapshot / unknown | if a source is not the grain you assume, joins fan out and measures double-count; resolve before any structure |
| Target fact grain | transaction event / order-line / periodic snapshot / accumulating snapshot | the grain IS the model; every measure and dimension must be true at this grain |
| Fact type | transaction / periodic snapshot / accumulating snapshot | a snapshot hides line detail; an accumulating snapshot tracks a pipeline with milestones |
| Measure additivity (per measure) | additive / semi-additive (not over time) / non-additive (ratios, %) | summing a semi-additive measure across time double-counts; ratios must be computed from summed components |
| Conformed dimensions | shared across marts / local | an unconformed "customer" in two marts means the two never reconcile |
| SCD type (per dimension) | type 1 overwrite / type 2 history rows / type 3 limited / hybrid | type 1 loses history (a by-segment-by-month report goes wrong after a segment change); type 2 is the cost of correct point-in-time |
| Degenerate dimensions | keep the id on the fact / build a one-column dim | order_id with no attributes belongs on the fact, not a dim |
| Junk dimension | collapse low-cardinality flags into one dim / separate dims | a dim per boolean flag explodes the model |
| Role-playing dimensions | one date dim played as order / ship / invoice date / separate dims | reuse one conformed date dim via views or aliases |
| Late-arriving facts | hold / route to an unknown member / backfill | a fact whose dimension row is not there yet needs a policy |
| Late-arriving or restated dimensions | type-2 back-date / accept drift | restatements change historical attribution |
| Unknown / NULL members | a -1 "unknown" member / NULL FK | NULL foreign keys break inner joins and silently drop rows |
| Surrogate vs natural keys | surrogate on dims / natural keys | surrogates decouple the warehouse from source key churn and enable type-2 |

## A compact dimensional-modelling primer
**Grain first.** Declare the fact grain as one sentence, "one row per ___", before anything else. Every measure must be true at that grain and every dimension must attach at it. Choosing the grain wrong is the one mistake you cannot patch later; it is a rebuild.

**Fact types.** A transaction fact records an event (one row per event): most flexible, finest grain. A periodic snapshot records state at regular intervals (one row per entity per period, e.g. one row per subscription per month): ideal for balances and "as of" reporting. An accumulating snapshot tracks one row per pipeline instance, updated as it hits milestones (placed, shipped, delivered).

**Additivity.** Additive measures sum across every dimension (revenue, quantity). Semi-additive measures sum across some dimensions but not time (account balance, MRR, headcount: summing them across months double-counts; take period-end or average instead). Non-additive measures (ratios, percentages, unit price) must not be summed at all; sum the components and compute the ratio at query time.

**Slowly changing dimensions.** Type 1 overwrites, so you keep only the current value and historical facts re-attribute to today's attribute (a customer who moved SMB to Enterprise makes all prior orders look Enterprise). Type 2 adds a new row per change with effective-from / effective-to, preserving point-in-time truth at the cost of more rows and surrogate-key plumbing. Type 3 keeps a limited prior value in a column. The choice is a business call: does a by-attribute-over-time report need the attribute as it was then? If yes, type 2.

**Conformance and the bus matrix.** Dimensions shared across facts (date, customer, product) must be conformed: same keys, same grain, same meaning, or two marts built on them never reconcile. A bus matrix (business processes as rows, conformed dimensions as columns) is the one-page plan for that.

## The Model Contract template
```
# Model Contract: <model name>  (v<n>, effective <date>)

## Business process / decision served
<what this model exists to answer, and for whom>

## Target grain
One row per <___>.   (fact type: transaction | periodic snapshot | accumulating)

## Sources + gated grain
| Source | Its grain (evidenced) | Keys / dup risk | Status |
|---|---|---|---|
| <src> | one row per <___> (per <evidence>) | <pk> | pinned / [needs decision: owner] |

## Fork log
<the checklist rows, each pinned / [needs decision] / N/A-because, with a one-line why>

## Logical star
<fact + its dimensions, described; conformed dims marked; a small bus matrix if multi-process. No DDL.>

## Measures + additivity
| Measure | Additivity | Note |

## Conformed dimensions + reconciliation
<which dims are conformed; how this model reconciles to existing models and the metric contract>

## Guardrails
<what this model deliberately does NOT support; known risks / caveats>

## Open questions
<source-grain gates + [needs decision] forks, each with an owner>
```

## Worked example: a Meridian subscription/MRR fact
Reusing the Meridian world from `examples/saas-retention/` (its locked NRR contract is the metric anchor).

**Decision served:** monthly net revenue retention and MRR movement for the board readout.

**Target grain:** one row per subscription per month, a periodic snapshot (NRR is an "as of month end" measure; a transaction grain would force re-derivation on every query).

**Source-grain gate (applied):** the billing feed: is it one row per invoice, per subscription-period, or per plan-change event? Pinned only after the owner confirms it emits one row per subscription per billing cycle; until then it was `[needs decision: RevOps]`. This is exactly the gate the base model skips.

**Fork log (excerpt):**

| Fork | Pinned |
|---|---|
| Fact grain | one row per subscription per month (periodic snapshot) |
| MRR additivity | semi-additive: sum across customers and plans, NOT across months (take month-end) |
| customer SCD | type 2: segment changes must not re-write historical NRR by segment |
| subscription_status | degenerate dimension on the fact (active / paused / churned) |
| Conformed dims | customer, date, plan (shared with the billing mart) |
| Late-arriving cancels | restate the affected month-end snapshot; flagged in the contract |

**Logical star:** `fct_subscription_month` (grain: subscription x month) joins `dim_customer` (type 2), `dim_plan`, and `dim_date` (role-played as snapshot_month). Measures: `mrr` (semi-additive), `seats` (semi-additive), `mrr_change` (additive within a month). Reconciliation: month-end MRR summed across active subscriptions equals the locked NRR contract's numerator base.

No DDL: this is the design the build team implements and `review-my-query` later checks against the contract.
