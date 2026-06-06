# Blast-radius taxonomy + falsification — audit-my-assumptions

Load when running the loop (steps 2 and 4). Two jobs: classify each inherited premise by how far a wrong one cascades (trunk vs leaf), and know the three ways to try to break the load-bearing ones.

## The trunk-vs-leaf taxonomy

A **trunk** assumption sits under the whole output: get it wrong and every number is poisoned, silently. A **leaf** is cosmetic: a wrong one is embarrassing, not catastrophic. Grade by blast radius, validate trunks first.

| Trunk class | The silent question it answers | How a wrong one cascades | Worked instance |
|---|---|---|---|
| **Population / definition** | what counts as the thing? | the wrong rows in or out of *everything* | "package = `BUNDLEID IS NOT NULL`" — but promo bundles are now booked as excluded add-on lines, so the definition captures a near-empty residual |
| **Grain** | one row = what? | fan-out double-counts sums; dedup hides them | summing option-line amounts as if they were per-booking |
| **Unit** | what is this measure denominated in? | numbers off by a factor or meaning a different thing | a "Revenue" column that holds *cost* on package rows (a swap) |
| **Period basis** | which date defines the period? | a different population than the one the consumer expects | booking-date vs travel-date — a ~20% population swing, invisible until you tie out |
| **Identity** | what is one entity? | over/under-counted entities; wrong rollups | one `ItemLabel` per property — false when variants / renames / "DO NOT USE" fragment one property across many |
| **Magic constants / exclusions** | which hardcoded list shapes the result? | silently drops or keeps the wrong rows; rots as the catalog changes | `NOT IN (8,9,12)` — correct once, but "what is 22 today, and does the thing I need live there?" |

**Leaf** (name it, don't spend the budget): labels, formatting, column order, a cosmetic rename, a display rounding. A leaf becomes a trunk only if a downstream measure keys on it.

## The three falsification checks (loop step 4)

You are trying to **break** each trunk assumption, against the most generative source reachable — **live system > generative code > windowed export > hand-touched workbook**. Never refinance a premise against a derivative.

### (a) Trend, not snapshot — the most-skipped, most-lethal check
Profile the feeding population **over time**, even when you were handed a single clean window. A definition that has gone stale, or a population that changed shape — a process change, a retired/renamed field, a re-platform, a regime change — shows up as a **structural break** in the by-period counts. It is **invisible in any one window**, where it just looks like a normal small number. This is the check that catches the wrong assumption *before* it produces a confident wrong answer, and it is the one a capable analyst skips precisely because the number in front of them looks fine.

> Rule: a clean number from one window is not evidence the definition is current. Run the by-year (or by-month) count of the population that feeds it and look for a break.

### (b) Triangulate
Derive a load-bearing figure a **second independent way** (a different table, a different path, a cross-system total). Agreement raises confidence; divergence localizes the bad assumption. The htp package collapse was confirmed by two independent base-table measures that agreed exactly.

### (c) Anchor honestly
- Never validate a premise against a **derivative** (the prior report, an inline reconstruction of the proc) — it can carry the same wrong assumption.
- Never validate a **filtered metric with a whole-table sum** — match the scope and the date basis, or the check passes while the number is wrong.
- Always separate **"matches the source"** (verifiable) from **"correct for the business"** (a Decision only the owner can settle).

## Worked example — "Promo Bundle Sales by Year" (the inherited-definition + regime-change miss)

**The ask:** build *Promo Bundle Sales by Year* for marketing, from a proc the data team uses for "packages."

**The inherited proc** defines a package as `bo.BUNDLEID IS NOT NULL` and applies `AND st.ITEMTYPEID NOT IN (8,9,12)  -- exclude fees / add-on lines / gift card`, filtered on order date.

**The naive build** copies that definition, charts the result, and writes the headline. Handed a *single clean year* (412 orders, $340K), it ships the deck — the definition is never questioned because nothing on the page looks wrong. Handed the *full trend* (5,800 in 2019 → 0 in 2026), it writes "promo bundle sales collapsed 95%."

**Both are wrong, the same way.** The predefined-bundle *mechanism* (`SALES_BUNDLE`) was retired ~2021 in a booking-process change; promo bundles are now recorded as **type-9 add-on line name-tags** — exactly what the proc *excludes*. So `BUNDLEID IS NOT NULL` no longer captures promo bundles; it captures a near-empty residual of a retired mechanism. The "95% decline" is a recording change, not a sales decline. The clean 412 is the residual, not the product line.

**What the audit catches, where the build doesn't:**
- **Population/definition (TRUNK, NEEDS-DECISION):** `BUNDLEID = promo bundle` is an inherited assumption, not a fact. The business term ("promo bundle") may not match what the code captures. → ask the owner how promo bundles are recorded *today*.
- **Trend check (a):** profile package counts by year — the 2021→2022 structural break is the alarm; it is invisible in the single 2025 window.
- **Magic exclusion (TRUNK):** `NOT IN (...,22,...)` — what is type 9, and could the thing the report is *about* live there? (It does.)
- **Period basis, grain, unit, cancellations:** each its own trunk row with its check.

The lesson the example teaches: the worst assumption is the one that produces a *clean, plausible number* — so you check the definition and the trend **before** you build, not after the stakeholder squints.
