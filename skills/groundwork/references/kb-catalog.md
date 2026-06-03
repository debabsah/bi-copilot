# KB Catalog — Adaptive Optional Artifacts

Beyond the always-on core, propose ONLY the artifacts this project actually needs. Never instantiate the whole catalog. Create each as `knowledge-base/<name>.md` and add it to the README index.

| Artifact | File | Propose when… | Holds |
|---|---|---|---|
| Meeting briefing | `meeting-briefing.md` | a stakeholder meeting is upcoming | objective, agenda, questions to ask, what to listen for |
| Requirements brief | `requirements-brief.md` | a request names a solution (KPIs/dashboard/report) before the decision behind it is validated | as-requested vs decision-derived metrics (the delta), the real decision, JTBD, verdict (proceed/reframe/wrong-problem) — produced by `requirements-interrogator` |
| KPI contract | `kpi-contract.md` | metrics are being defined (Type B) | per metric: definition, formula, grain, dimensions, source, owner, refresh, threshold, caveats, version, effective-date |
| Findings & recommendations | `findings.md` | analysis produces results to share | observation → implication → recommended action → watch-for |
| Lineage map | `lineage.md` | the estate has non-trivial dependencies (Type A/C/D) | the object DAG; source→target paths |
| Stakeholder map | `stakeholders.md` | multiple/contested stakeholders | who decides/validates/consumes/owns-data; interests; tensions |
| Status / roadmap | `status.md` | the project spans weeks | done / next / parked; phase position |
| Data quality | `data-quality.md` | trust/defensibility matters | coverage, known issues, validation evidence |

When you create an artifact file, phase-tag its heading the same way as the core files (e.g., `# KPI Contract  [Define]`).
