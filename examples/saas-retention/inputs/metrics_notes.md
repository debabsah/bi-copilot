# Metrics notes (Dana)

Quick notes before I hand this off. Sorry it is thin.

- **Churn**: how many customers we lose each month. Use `vw_monthly_churn`. The
  board likes it under 5%. It is logos, not dollars.
- **NRR** (net revenue retention): Finance has this in their quarterly deck. Ask
  Priya (VP Customer Success) or someone in RevOps. I never built it here.
- Heads up: the churn number from the view and whatever Finance shows for
  retention never quite line up. Nobody ever got to the bottom of why. I think it
  is because the view counts logos and Finance counts dollars, but I am not sure.
- The `NOT IN (...)` list in the view: I inherited that from the analyst before me.
  I think they are a few odd accounts. I left it alone.
- Trials: not totally sure they are excluded. Worth checking.
