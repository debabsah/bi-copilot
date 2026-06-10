# Brief modes — micro-brief and delta brief

## Micro-brief ("three sentences for the exec")

Compression rules — the ledger discipline survives, the prose shrinks:
1. Only vetted claims enter, same as the full brief; an unvetted number doesn't become
   sayable by being short.
2. Status travels inline: "X is confirmed (audit, <date>); Y is directional pending the
   hold-out" — an open stays VISIBLY open.
3. Qualifiers survive: an overridden gate or carried verdict keeps its tag even at three
   sentences.
4. The honesty valve: if the truthful version doesn't fit, the last sentence says what was
   cut — "fuller picture in the brief; two open items not covered here."
5. Provenance compresses to a pointer, not zero: "(per the 06-04 audit)".

```markdown
**Micro-brief — <topic> (<date>, from the record):** <claim 1 with status>. <claim 2 with
status>. <the open/qualifier sentence, or the honesty valve>.
```

## Delta brief ("what changed since the last readout")

Composed as a DIFF of the record against the last brief's date — never re-narrated from
memory:
- **Moved:** numbers that changed, with both values and the cited cause (timeline/triage).
- **Closed:** open questions answered since (with the answer + who).
- **Flipped/expired:** verdicts that changed state — incl. Re-audit-when conditions met.
- **New:** opens, risks, decisions since (cited).
- **Unchanged:** named as unchanged — not re-sold, not silently dropped.

```markdown
# Delta brief — since <last readout date>  [Deliver]
_Source: the record's diff, <date range>. Unchanged items are listed, not re-narrated._
**Moved:** … · **Closed:** … · **Flipped/expired:** … · **New:** … · **Unchanged:** …
```

Both modes append to `knowledge-base/findings-brief.md` (dated, newest on top) and offer
the `kb(brief-my-findings)` commit — same composition as the full brief.
