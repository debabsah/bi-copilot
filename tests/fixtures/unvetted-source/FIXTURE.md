# unvetted-source fixture (answer key — never inline into a cold run)

LATENT trap for audit-my-assumptions. The model is asked to turn an inherited proc's clean
single-year output into a marketing-deck summary. Everything looks fine — a tidy, small number
(412 / 880 / $340,000). That is the trap: the load-bearing inherited **definition is stale**, and
nothing in the handed-over window signals it.

Fully synthetic schema and figures — illustrative only, no real data.

## The buried defect (invisible by design)
`usp_BundleSalesReport` defines a "bundle" as `ol.BUNDLEID IS NOT NULL` and excludes
`ITEMTYPEID NOT IN (8, 9, 12)` (fees / add-on lines / gift cards). In the business this models, the
predefined-bundle mechanism was retired; promo bundles are now recorded as **type-9 add-on lines** —
exactly what the proc EXCLUDES. So `BUNDLEID IS NOT NULL` no longer captures promo bundles; the 412 is
the residual of a retired mechanism, not the product line. The defect is INVISIBLE in the single 2025
window — it only surfaces if you (a) question the inherited definition vs the business term, or
(b) profile the population by year and see the structural break.

This is the de-narrated, INVISIBLE variant. (A legible variant — handing over the full multi-year trend
with a dramatic cliff — DEFLATES: a bare model catches the on-page anomaly unaided.)

Secondary inherited-assumption traps a complete audit names: option-grain fan-out (`SUM(Qty)` /
`SUM(Amount)` over lines can double-count per order); no order-status filter (cancellations inflate all
three); the `NOT IN (8, 9, 12)` magic list (what is type 9 today, and could the thing the report is
about live there?).

## PASS (detection lift) — the audit STOPS and excavates
- Does NOT just build the deck summary on the inherited definition.
- Flags `BUNDLEID = promo bundle` as an inherited assumption to validate (TRUNK / NEEDS-DECISION),
  noting the code definition may not match the business term "promo bundle".
- Bonus (strong): calls for the by-year trend / asks how promo bundles are recorded today, and/or
  flags the excluded type-9 add-on lines as possibly where today's bundles now live.
- Routes the intent-type assumptions to the owner; produces a graded register rather than a slide.

## FAIL (no lift) — builds the slide
Writes the 412 / 880 / $340,000 summary + takeaway, inheriting the stale definition silently
(a peripheral caveat about the date basis or the exclusion list does NOT count as catching the trunk).
