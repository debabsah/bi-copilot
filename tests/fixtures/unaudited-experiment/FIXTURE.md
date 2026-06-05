# Fixtures for audit-my-experiment (answer key — never copy into a cold-run dir)
- subtle-srm.txt: arms 500000/502800 -> srm_chisquare p~=0.0048 = ELEVATED (1-in-200). GREEN must COMPUTE this, not eyeball "~50/50". Also: relative-only framing; "p<0.001" with no CI.
- glaring-srm.txt: arms 50000/54200 -> p~=1e-38 = hard SRM (Blocking). Plus peeking (daily, stop on cross) and 8-metric multiplicity. GREEN gates HOLD/invalid.
- clean.txt: balanced (240000/240500 -> ok), fixed horizon, single metric, CI excludes 0, revenue tracks. GREEN must NOT false-alarm -> verdict ship-ready (false-alarm control).
