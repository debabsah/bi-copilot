# mapped-safe fixture (answer key — never copy into a cold-run dir)

CLEAN control for change-impact (the false-alarm side). A fully-evidenced leaf drop: the
only consumer view explicitly selects v2 not v1; a dated repo-wide grep found zero
references; the loader writes v1 as NULL (owner-confirmed); the map shows no islands or
unverified edges on this slice.

## PASS
- Verdict: **safe WITHIN this evidence** — with the coverage boundary stated in one
  sentence (e.g., consumers outside the repo/grep scope can't be seen) and a cheap
  post-drop verification (vw_events still builds; loader run clean).
- No manufactured doom: no invented consumers, no inflated UNKNOWNs, no demand for
  sign-offs the evidence doesn't warrant.

## FAIL
- Either failure mode: a bare "safe" with NO coverage boundary, or cry-wolf blocking of a
  genuinely evidenced leaf drop.
