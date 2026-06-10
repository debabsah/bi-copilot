# Exploration engine — explore-my-data

Load when grading findings (loop steps 3–5). Three jobs: name the dredging move being
tempted, do the cut-counter math, and separate robust patterns from lucky cells.

## The dredging taxonomy (the moves to refuse)

| Move | What it looks like | The honest move instead |
|---|---|---|
| **HARKing** | the hypothesis written after the hit ("we suspected tablets all along") | pre-registered vs post-hoc labels; post-hoc is fine, hidden post-hoc is not |
| **Garden of forking paths** | 24 cuts taken, 1 reported | the cut log: every fork counted, the multiplicity line stated |
| **Base-rate burial** | "+96% lift!" | "5 of 85 vs ~3% baseline" leads; the lift follows |
| **Correlation laundering** | "segment X drives conversion" | correlation language; a design (→ audit-my-experiment) for "drives" |
| **Generating-data confirmation** | re-running the same query "to verify" | a pre-specified hold-out the finding has never seen |
| **Dead-end deletion** | the log shows only hits | dead ends recorded — they are the denominator of the story |

## The cut-counter math (prose, no kit needed)

With N cuts examined at α≈.05, ~N/20 false hits are EXPECTED under pure noise — so a
24-cut table owes you ~1.2 striking cells for free. The line goes next to every striking
pattern: *"one of 24 cuts examined; ≈1.2 false hits expected at this threshold — this may
be one."* Small bases amplify it: with a 3% base rate, a cell of n=85 expects ~2.6
conversions; seeing 5 (5.9%) happens by chance in roughly one cell in nine — near-certain
somewhere across 24 cells. A formal multiplicity correction (Holm/BH) is
`audit-my-experiment`'s kit; this skill states the expectation math and routes formal
claims there.

## Robust vs lucky (the tests a pattern must face before "Robust pattern")

- **Consistency across related cells** — does the effect hold in the neighboring slices
  (other regions on tablet? other devices in APAC?), or does it live in exactly one cell?
- **Dose-response / monotonicity** — if the driver story were true, intermediate exposures
  should show intermediate effects. Do they?
- **Pre-period stability** — does the pattern exist in the prior window, or was it born in
  the window that was searched?
- **Base adequacy** — is n large enough that the effect couldn't be three customers?
Passing these upgrades a hit to **Robust pattern** — still unconfirmed until the
pre-specified hold-out paste-back.

## Worked mirage — the tablet×APAC "goldmine"

A 24-cell cut of conversion (channel × region × device): overall 3.0%, twenty-three cells
between 2.6–3.4%, and tablet×APAC at **5.9%** — "+96% lift, our best segment!" The honest
read: 5 conversions on n=85 (the smallest cell on the table); ~1.2 false hits were
expected across 24 cuts; no neighboring cell agrees (tablet elsewhere ~2.9%, APAC on
other devices ~3.1%); the pre-period shows the same cell at 2.4%. Grade: **Exploratory —
found, likely mirage**; the log records the cut count, the base, the failed
robustness tests, and ONE confirmation check (next 8 weeks of tablet×APAC traffic,
pre-registered threshold) — and the deck does NOT get a goldmine slide this week. That
non-slide is a `catches.md` line.
