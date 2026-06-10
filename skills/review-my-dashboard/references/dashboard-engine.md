# Dashboard engine — review-my-dashboard

Load when walking the layers (loop steps 3–5).

## Layer 1 — Semantic (what the numbers mean once assembled)

| Check | The quiet failure | The test |
|---|---|---|
| **Additivity** | a DISTINCTCOUNT summed in a total; an average of pre-averaged rows; a ratio totaled as a sum of ratios | per measure: is the total/subtotal recomputed at total grain, or aggregated from the visual's rows? Distinct counts, ratios, averages, and percentiles never sum |
| **Measure × filter interaction** | a visual-level filter silently re-scopes a measure built with its own filter context (DAX CALCULATE, LookML filtered measures) | enumerate page/visual/report filters per visual; ask of each measure: which filters does it respect, override, or ignore? |
| **Time intelligence** | YTD where the title says rolling-12; "today" resolved in server timezone at 02:00 refresh | each time-relative measure: window, calendar, timezone, and refresh-time semantics vs the contract |
| **Drill grain** | a drill path from monthly to daily where the measure only makes sense monthly (e.g., month-end balance) | does every measure survive every drill level, or does grain shift its meaning? |
| **Contract conformance** | the displayed "churn" is logo churn; the locked contract pins revenue churn | per displayed metric: definition vs `kpi-contract.md`; NO contract = a finding on its own |

## Layer 2 — State (what the surface is actually showing right now)

- **Default filters** — a default is a silent population claim; FY2025 as default while the
  title says "performance" excludes the current quarter for every casual viewer.
- **Extract/refresh staleness** — what the freshness label implies vs the actual refresh
  date; "live" over a March extract is a Blocking finding.
- **RLS / viewer-dependence** — which numbers differ by viewer, and does the surface say
  so? A screenshot circulated from an admin's view is a different dashboard.
- **Default view vs reviewed view** — bookmarks, saved states, and landing pages: review
  the state the AUDIENCE lands on.

## Layer 3 — Presentation (what the surface claims)

- **The title test** — every title, subtitle, and annotation is a claim; it may claim only
  what its visual's data supports, over the window actually shown. "Churn improving" over
  a hand-picked 3-month window fails even if the 3 months are real.
- Axis truncation (a 3.0–3.3% y-axis turning noise into a cliff), dual-axis implication
  (two unrelated scales implying correlation), color scales that exaggerate, ambiguous
  sort, units/rounding inconsistent with the contract's precision.

## Grading (review-my-query's rubric, pointed at the surface)

**Blocking** — the room reads a wrong number or claim as-is (bad total, excluding default,
stale-as-live, failed title test on a headline). **Latent** — right today, breaks on a
predictable event (a drill added, RLS rolled out, the FY rolls over). **Advisory** — costs
trust or invites misreading without being wrong.

## Worked example — the QBR dashboard

Four measures, all individually correct. The review finds: `Active Customers` is
`DISTINCTCOUNT(customer_id)` and the card's "Total" sums three regional pages (**Blocking**
— overlapping customers double-counted; recompute at total grain); the page default filter
is `FY = 2025` while the title says "Customer Health" (**Blocking** — Q1-2026 silently
absent; either retitle or default to all-time); `Avg Deal Size` averages a column that is
itself a per-rep average (**Blocking** — average-of-averages; weight by deals); the trend
tile titled "Churn improving" shows Mar–May after a Jan spike (**Advisory→Blocking if it
headlines** — the window is a choice the title hides); one measure (`Net Revenue`,
SUM over additive grain, matches its contract) passes and is SAID to pass. Verdict:
not shippable as-is; coverage boundary: visual-level filter list reviewed from the export,
RLS rules not provided — unreviewable, named.
