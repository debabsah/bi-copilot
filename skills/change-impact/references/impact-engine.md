# Impact engine — change-impact

Load when walking and grading (loop steps 3–4).

## The walk method

- **Start node:** the exact object/column/path being changed.
- **Edges that count** (map-my-estate's evidence rules, applied to traversal): an FK or
  reference in DDL, a join/SELECT in code on hand, a dbt manifest parent→child entry,
  documented lineage, an attributed owner statement. Name-likeness never counts.
- **Transitive, to the end:** every reached node is itself walked. Two patterns propagate
  invisibly and get flagged wherever they appear: `SELECT *` (a rename/drop sails through
  and breaks at the far end) and view-on-view chains (the drift compounds).
- **Dashed `[unverified]` edges and islands** from the estate map enter the register as
  UNKNOWN with a pre-flight check — they are candidate impacts, never dismissals.
- **The coverage boundary:** at the end of the walk, state what the evidence could not
  see — undocumented consumers, BI-tool datasets, exports, ad-hoc users. That sentence is
  part of the verdict, not a footnote.

## The dbt-manifest entry path

A provided `manifest.json` is read as text: `child_map[<changed node>]` seeds the radius;
each child's `compiled_sql`/`depends_on` confirms the edge kind; exposures are consumers.
The manifest is EVIDENCE for what dbt knows about — everything outside dbt (procs,
BI-tool models, exports) stays on the unknown side of the coverage boundary.

## The silent-drift taxonomy (the meaning-breaks no error log catches)

| Drift | The quiet mechanism | The check |
|---|---|---|
| **Type / rounding** | `DECIMAL(12,2)→(10,0)`, float→int, string-date coercion | before/after on the contract metric at full precision |
| **Filter / population** | a WHERE tweak shifts who is counted | row counts + boundary cases by segment, before/after |
| **Grain / weighting** | dedup or grain change re-weights every average | grain assertion + a weighted-vs-unweighted comparison |
| **Timezone / date basis** | DATE vs TIMESTAMP, UTC vs local — day-boundary rows migrate | day-boundary sample, both bases |
| **SCD semantics** | type-1 overwrite where history was assumed | as-of query on a known changed entity |
| **Contract-meaning** | the change makes the built thing diverge from the LOCKED `kpi-contract` definition | read the contract's pinned forks against the change; any divergence routes to the contract owner |

Pipeline-breaks get found by the deploy; these get found by the board. Rank accordingly.

## Worked example — "just a rename, we deploy tonight"

Change: `orders.amount → orders.gross_amount`, plus "while we're in there" a cast to
`DECIMAL(10,0)`. The walk: `vw_orders_paid` references `o.amount` (BREAKS,
vw_orders_paid.sql:3); `vw_daily_rev` is `SELECT *` over orders feeding `rev_summary`
(BREAKS at the far end — star-expansion flagged); the NRR contract's revenue input is
`orders.amount` at 2dp (the cast = **contract-meaning drift**: revenue rounds to whole
units, ~0.3% on a typical basket — no pipeline fails, the board number moves); the estate
map shows `finance_export` as an island (UNKNOWN — pre-flight: ask Finance what feeds the
export). Verdict: 2 BREAKS, 1 SILENT-DRIFT on a locked contract (owner sign-off required),
1 UNKNOWN, coverage boundary stated. "It's just a rename" was four findings deep.
