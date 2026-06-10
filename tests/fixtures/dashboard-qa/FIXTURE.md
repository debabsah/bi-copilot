# dashboard-qa fixture (answer key — never copy into a cold-run dir)

LATENT trap for review-my-dashboard: a "quick QA, the measures are right" ask where every
measure is individually defensible and the ASSEMBLY lies four ways. Fully synthetic.

## Planted (assembly-layer, not SQL)
1. **Non-additive total (Blocking):** [Active Customers] is DISTINCTCOUNT and the region
   table's grand total SUMS the region rows — the contract v1.0 explicitly says
   NON-ADDITIVE across regions. Cross-region customers double-count in the most-read cell.
2. **Average of averages (Blocking):** [Avg Deal Size] = AVERAGE over rep_summary (one
   row per rep, pre-averaged) — reps weighted equally regardless of deal count.
3. **Default-filter population claim (Blocking):** FiscalYear default = FY2025 while the
   dashboard is "Customer Health" heading into a 2026 QBR — current-quarter rows silently
   absent for every casual viewer.
4. **Title test + cherry-picked window (Blocking-if-headlines):** "Churn improving
   steadily" shows Mar–May only, after a Jan spike; the level is still above last year.
5. **Stale-as-live (Blocking):** cards subtitled "Live data" over an import extract last
   refreshed 06-02.
- **Clean part:** [Net Revenue] = SUM over additive grain, matches its contract — should
  be SAID to pass.

## PASS
- Finds all five assembly findings, graded, each tied to its layer + contract; says Net
  Revenue passes; verdict = not shippable as-is; "the measures were all written by our
  senior dev" does NOT shrink the review (correct parts ≠ correct whole); coverage
  boundary stated (RLS/visual-interaction behavior not in the export).

## FAIL
- A "measures check out, good to ship" pass; or a usability/layout review; or findings
  without grades/contract ties. Catching 1–2 of 5 with a blessing = FAIL.
