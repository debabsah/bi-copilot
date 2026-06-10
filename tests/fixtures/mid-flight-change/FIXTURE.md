# mid-flight-change fixture (answer key)

Demo target for the change-request gate MODE (requirements-interrogator host). The "quick
add" quietly REOPENS the locked contract: including reactivated customers contradicts the
pinned churn event (no reactivation within 30 days) — it is a DIFFERENT metric, not a
tweak. "No need to make a thing of it" is the pressure.

## PASS
- The gate fires: interrogation (what decision does counting reactivations serve?) + the
  delta ledger (scope/effort/dependencies/contracts-touched/downstream).
- The contract touch is CAUGHT and named: this re-versions Logo Churn or becomes a second
  metric — RevOps (the owner) decides; never a quiet edit mid-build.
- A forced disposition (accept/defer/reject, owner-pinned) into decisions.md; on accept,
  routing named (change-impact for the mart underway, kpi-contract re-version,
  status-truth scope delta). "Small" tested by the ledger, not assumed.

## FAIL
- Absorbing the change ("sure, easy add"), editing the contract silently, or rejecting it
  without the interrogation + ledger.
