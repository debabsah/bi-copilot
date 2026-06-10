# clean-dashboard fixture (answer key — never copy into a cold-run dir)

CLEAN control for review-my-dashboard (the false-alarm side). Everything is honest:
additive measures with totals recomputed at total grain, no excluding defaults (title says
all-time AND shows all-time), the trend title claims exactly its window, axis from 0,
freshness label matches the actual nightly refresh, both measures match locked contracts.

## PASS
- A clean verdict: shippable; both measures conform; what passed is said plainly; the only
  honest residue is the coverage boundary (e.g., RLS/interaction behavior not in the
  export) — stated as a boundary, NOT converted into manufactured findings.

## FAIL
- Cry-wolf: inventing assembly defects, demanding contract work that's already done, or
  grading the boundary itself as a Blocking finding.
