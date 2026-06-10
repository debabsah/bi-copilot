# Fork points — kpi-contract

Load when pinning a metric. A metric definition silently makes a dozen choices; this is the checklist of where it can legitimately go two ways. Walk it, surface each fork, and let the **owner** pin it (or mark `[needs decision]`). The forks you skip are next quarter's argument.

## The fork checklist
Not every fork applies to every metric. Run the list, keep the ones that bite, pin each.

**Time**
- Which timestamp drives the period — event date, close date, recognition date, ingestion date?
- Timezone (UTC vs local vs reporting tz)? Period boundaries (calendar vs fiscal; inclusive/exclusive)?
- As-of vs trailing window? How are partial / in-flight periods shown?

**Population / filter**
- Who or what is in scope? Internal / test / bot records excluded?
- Active vs all (and what defines "active")? New vs existing vs renewal?

**Counting**
- Grain: one row per what? Deduplication — per user, per session, per order?
- Numerator gross vs net: include refunds / reversals / cancellations / chargebacks / downgrades?
- Multi-count rule: can one entity land in two buckets?

**Derivation**
- Attribution / allocation model (first / last / multi-touch; even / weighted)? Lookback window?
- Currency / FX rate (spot vs period-average)? Unit normalization (monthly → annual)?

**Late & changing data**
- How are late-arriving events handled? Is the metric **restated** as data lands, or **frozen** at period close?

**Source & reconciliation**
- Which system is the **source of record**? (Not "whatever's easiest to query.")
- Expected relationship to neighboring blessed numbers — subset of? equal to? bridges via what? An unknown bridge is `[needs decision]`, never "reconcile later".

**Decision fit**
- Refresh cadence (inherited from the decision the metric serves).
- Threshold that triggers action; is up good or bad?
- Which slices are valid to cut by, and which mislead?

> Two rules while walking the list: the **owner** pins each fork (you surface and recommend), and the **decision** drives the definition — never let the columns that happen to exist define the metric.

## KPI Contract — template
One page per metric, committable. Lives at `knowledge-base/kpi-contract.md` (append per metric); no `knowledge-base/` anywhere up-tree → create it now with the contract plus the stub `README.md` index (per the office convention in groundwork's kb-core-templates). Phase-tag the heading `[Define]`. When the office is git-tracked, offer the commit — `kb(kpi-contract): lock <metric> v<N>` — one artifact, one commit.

```markdown
# KPI Contract — <metric name>  [Define]

- **Definition (one sentence):** <what it measures, in business terms>
- **Formula:** <numerator / denominator or expression, plain language>
- **Grain:** <lowest level at which a row is valid>
- **Dimensions:** <slices valid to cut by; slices that mislead>
- **Source of record:** <the blessed system; the bridge to neighbors>
- **Reconciliation:** <expected relationship to [neighboring number]; or [needs decision]>
- **Refresh:** <cadence — inherited from the decision it serves>
- **Threshold / direction:** <value that triggers action; is up good or bad>
- **Owner:** <who owns this definition>
- **Caveats:** <known limits; what it is NOT>
- **Version / effective-date:** <vN, YYYY-MM-DD; if a redefinition: what changed + why>

## Fork log — the choices this definition makes
| Fork | Options | Pinned choice | Why it matters |
|---|---|---|---|
| ... | ... | ... or [needs decision] | ... |
```

## Worked example — marketing-attributed revenue
The classic two-teams-disagree metric (and the one `defend-my-number`'s sample rehearses). The spine is easy; the forks are the work.

```markdown
# KPI Contract — Marketing-Attributed Revenue  [Define]

- **Definition:** Recognized subscription revenue in the period attributable to a marketing campaign touch under the org's blessed attribution model.
- **Formula:** sum(recognized_revenue) where attributed_campaign is not null, net of refunds/downgrades.
- **Grain:** one row per subscription per recognition period.
- **Dimensions:** campaign, channel, segment. (Misleading: by close-date month, when reporting recognized revenue.)
- **Source of record:** recognized revenue from the Finance/billing ledger; attribution flag from HubSpot. NOT HubSpot deal value.
- **Reconciliation:** strict subset of Finance total recognized revenue; bridges via (a) no-touch/direct revenue, (b) out-of-window touches, (c) refunds. Expected ≤ Finance total.
- **Refresh:** quarterly (QBR cadence).
- **Threshold / direction:** up is good; informs next-quarter campaign budget.
- **Owner:** analytics, co-signed by Finance + Marketing.
- **Caveats:** is NOT total company revenue; is NOT bookings. Renewals excluded.
- **Version / effective-date:** v1.0, 2026-06-03.

## Fork log
| Fork | Options | Pinned choice | Why it matters |
|---|---|---|---|
| Revenue basis | bookings / recognized | recognized | bookings-vs-recognized is usually the biggest gap with Finance |
| Refunds & downgrades | gross / net | net | gross overstates; Finance is net |
| Scope | incl. renewals / new + expansion only | new + net-new expansion | renewals are account-managed, not marketing |
| Attribution model | first / last / multi-touch | [needs decision] | org standard not yet confirmed; changes campaign credit |
| Lookback window | 30 / 90 / 180 days | [needs decision] | inherit HubSpot's blessed setting; don't invent |
| Period basis | calendar / fiscal | fiscal (matches Finance) | aligns period boundaries with the board number |
```

Every `[needs decision]` goes to `open-questions.md`; the basis/scope calls and their rejected alternatives go to `decisions.md`. The contract is born defensible — which is exactly what makes it `defend-my-number`'s ammunition.
