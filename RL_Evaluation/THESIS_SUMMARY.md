# RL Model Evaluation — Thesis Summary

Numbers-first summary of `RL_Evaluation/results/`, written to be pulled
near-verbatim into a Results-section RL evaluation subsection and a
Discussion/Limitations paragraph. All numbers below are **post-fix**
(generated against `Environment.py` with both Goal-0 reward bugs fixed —
see "Goal 0" note at the end) unless explicitly marked pre-fix. Full
provenance, methodology, and per-file documentation: `README.md` and
`METHODOLOGY.md` in this directory.

## Goal 1 — Training convergence

- **Small dashboard (6 visualisations), 100 episodes, seed 42.** Reward
  (`R_Final`) rises from a first-10-episode mean of 0.4077 to a last-10-episode
  mean of 0.4252 (+4.3%), plateauing by approximately **episode 28**. A
  separate 500-episode stretch run confirms this holds: the reward at
  episode 500 (0.4252) is identical (to 4 decimal places) to its value from
  episode ~28 onward through the original 100-episode run — extending
  training 5x further produces no further gain.
- **Large dashboard (15 visualisations), 100 episodes, seed 42.** Reward
  moves from a first-10 mean of 0.2900 to a last-10 mean of 0.2798 (**−3.5%**
  — essentially flat, with a slight *decline* rather than the small
  dashboard's slight incline), plateauing by approximately **episode 6**.
  Valid sampled-action counts per episode ranged 21-200 out of a 200-step
  budget; episode 3 came within 1 action of the 20-action (10%) validity
  floor, with 661 invalid (masked-out) sampling attempts that episode — a
  real, if modest, safety-margin concern for the larger/more varied
  dashboard, absent on the small dashboard (valid actions never dropped
  below 32).

## Goal 3 — Training-budget adequacy verdict

**100 episodes is sufficient** for both dashboard sizes tested: both
plateau well inside the budget (small: ~episode 28; large: ~episode 6), and
a 500-episode stretch run on the small dashboard shows no further reward
gain past its original convergence point. Caveat: the *margin of safety*
against the 10% valid-action floor is materially thinner for the larger,
more varied dashboard (down to 21/200 valid actions in one early episode,
vs. never below 32/200 on the small dashboard) — this doesn't overturn the
sufficiency verdict but means it should not be assumed to generalise
comfortably to arbitrarily complex dashboards. Goal 4c (below) confirms
this concern is real and, for at least one actual real-world dashboard,
substantially worse than either fixture showed.

## Goal 2 — Reward-weight sensitivity (post-fix, with reversal)

Two test states, 4 reward-weight configurations, reward recomputed for
every action the model's own masking allows:

- **`pie_chart_9items`**: top-1 recommendation ("Change to Bar Chart") is
  **identical across all 4 weight sets** — robust to the weight choice.
- **`bar_chart_5items`** (bar chart, 5 items — the same state as the
  thesis's published Action Space worked example): top-1 is **"Change to
  Pie Chart"** for 3 of the 4 weight sets, but **"Remove Item Limit"** for
  the 4th (equal-weights) set — **not robust to the weight choice**.

**This is a reversal from the pre-fix result**, where `bar_chart_5items`'s
top-1 ("Remove Item Limit") *was* robust across all 4 weight sets. The
reversal traces directly to the Goal-0 decluttering-formula bug fix: that
bug used to score "no item limit set" as near-maximum decluttering; the fix
correctly scores it as minimum decluttering, which demotes `RemoveItemLimit`
from rank 1 to rank 2 under 3 of the 4 weight sets. `pie_chart_9items`'s top
action doesn't touch item limits, so it was unaffected by the fix and
stayed robust both before and after.

**Honest framing for thesis text:** "the model's #1 recommendation is
robust to the reward-weight choice for some dashboard states but not
others — for the bar-chart worked-example state specifically, the top pick
flips between two candidate actions depending on the weights used."

## Goal 4 — Frozen-policy baselines and cross-dashboard robustness

**Baseline comparison (4b), trained greedy top-1 vs. 100-sample random mean
vs. rule-based heuristic, 8 dashboards (2 synthetic fixtures + 6 real
dashboards converted from seeded ESG-reporting dashboard specifications):**

| dashboard | trained top-1 | random mean ± std | rule-based |
|---|---|---|---|
| small | 0.4477 | 0.4224 ± 0.0256 | 0.4427 |
| large | 0.2855 | 0.2740 ± 0.0108 | 0.2742 |
| real_energy_climate | 0.5543 | 0.5845 ± 0.0217 | 0.5543 |
| real_cority_quality_monitor | 0.4747 | 0.5449 ± 0.0386 | 0.4747 |
| real_accuvio_resource_overview | 0.5786 | 0.5422 ± 0.0340 | 0.5634 |
| real_esgbook_score_analytics | 0.5147 | 0.5586 ± 0.0220 | 0.5147 |
| real_rimm_topic_scorecard | 0.6000 | 0.5915 ± 0.0116 | 0.5754 |
| real_measurabl_data_cards | 0.5746 | 0.5409 ± 0.0295 | 0.5234 |

**The trained model beats both baselines on 5 of the 8 dashboards** (small,
large, `real_accuvio_resource_overview`, `real_rimm_topic_scorecard`,
`real_measurabl_data_cards`), by margins of roughly +1% to +10% over the
better of the two baselines on each. **On the remaining 3 of 8**
(`real_energy_climate`, `real_cority_quality_monitor`,
`real_esgbook_score_analytics`), the trained model's top-1 reward is
**exactly tied** with the rule-based heuristic (identical to full float
precision in all three) but is **beaten by the random-baseline mean** by
5-13%. The trained model never loses to the rule-based baseline outright.
Report this as-is: the trained model does not uniformly beat a simple
hand-written heuristic across all dashboards tested, though it matches it
everywhere and clearly exceeds both baselines on the majority (5/8) of
dashboards.

**Cross-dashboard robustness (4c):** convergence speed ranges from episode
6 to episode 28 across the 8 dashboards and does **not** track dashboard
size in a simple way — the 15-visualisation `large` fixture converges
fastest (episode 6), while the 6-visualisation `small` fixture converges
slowest (episode 28); real dashboards fall in between (episodes 8-19).
Final-vs-initial reward change ranges from −3.5% (`large`) to +32.0%
(`real_esgbook_score_analytics`). **Frozen-policy evaluation (4a) is fully
deterministic**: the live top-K inference path enumerates and ranks by
probability rather than sampling, confirmed empirically across all 8
dashboards (3/3 repeat runs agree on the #1 action every time), so a single
evaluation run per dashboard is sufficient and was used throughout.

**Wall-clock training time (4d):** total 100-episode training time ranged
from ~1,765s (~29 min, `real_accuvio_resource_overview`) to ~7,388s (~123
min, `real_cority_quality_monitor` — see anomaly below). Time to reach the
convergence episode specifically ranged ~110s to ~1,692s. This is real
per-dashboard latency a user of the live product would wait through for a
fresh model to train on their own dashboard.

**Deeper ablation (4f) — zeroing (not just reweighting) one reward
component at a time, 4 test states:** whether the #1 action changes is
state- and component-specific:

| state | flips when zeroing | stable under |
|---|---|---|
| `bar_chart_5items` | Decluttering | Appropriate-Vis-Types, Chart Variety, Data Completeness |
| `pie_chart_9items` | Appropriate-Vis-Types, Data Completeness | Decluttering, Chart Variety |
| `small_dashboard` (whole 6-viz fixture) | Appropriate-Vis-Types | Decluttering, Chart Variety, Data Completeness |
| `real_energy_climate` | *(none — fully robust)* | all 4 components |

## Anomaly found during Goal 4 sanity-checking: `real_cority_quality_monitor`'s validity-floor breach

Per-episode inspection of `goal4c_training_log_real_cority_quality_monitor.csv`
shows this dashboard's training run stayed **below the intended 20-valid-action
(10%) floor for 9 of episodes 12-21**, bottoming out at **3 valid actions**
in episode 18 (1.5% of the 200-step budget) against **3,997 invalid
sampling attempts** that episode — within 3 attempts of the training loop's
hard cap (4,000). For roughly 10 consecutive episodes, this run was
effectively relying on the hard cap to end the episode, rather than
genuinely satisfying the floor's design intent. `real_measurabl_data_cards`
shows a much milder version of the same pattern (16 valid actions,
episodes 3-4 only, immediately recovers). All 6 other dashboards tested
never dropped below 20 valid actions in any episode. No run crashed;
`real_cority_quality_monitor`'s reward did recover and plateau afterward
(convergence estimated at episode 19, right at the tail of the problem
window) — but this is a genuine, dashboard-specific data point that the
"100 episodes / 10% floor is comfortably sufficient" conclusion does not
hold uniformly, worth a Discussion/Limitations sentence alongside the
milder version of the same concern already found on the synthetic `large`
fixture (Goal 1/3).

## Resolved: the SENSITIVITY_STATE_BAR_5 worked-example question

**Question:** for the state matching the thesis's published Action Space
worked example (bar chart, 5 items, state vector `[5,1,0.06,0,0.02,0]`),
was the model's actual **pre-fix** top-1 recommendation "Change to Line
Chart" (the published outcome)?

**Answer: No.** The pre-fix top-1 was **"Remove Item Limit"** (rank 1
across all 4 weight sets tested, reward 0.696/0.745/0.729/0.775 — see
`results/pre_bugfix/goal2_weight_sensitivity.csv`). "Change to Line Chart"
does not appear anywhere in the ranked candidates, pre-fix or post-fix,
**because it was never a structurally valid candidate action for this
state in the first place**: the model's own action masking
(`Environment.py::get_parameter_mask`) only allows a Bar Chart to change to
another categorical type (Pie) or to Table (or Single Value Display, if
reduced to exactly 1 data item) — never to Line Chart, which is reserved
for transitions from an existing Line/Multi-Series-Line source, by design.

**Implication for the thesis:** the published worked example's "change to
Line Chart" outcome was illustrative/hypothetical, not a real captured
model output — this is true independent of the Goal-0 bug fixes, since the
action was never reachable under the masking rules either before or after.
No worked-example rewrite is required, but if kept as-is, a caveat is
warranted: the real model's actual top-1 pick for this exact state is
weight-sensitive post-fix (Pie Chart for most weightings, Remove Item Limit
for equal weighting) and was never "Line Chart" under any tested
configuration.

## Goal 5 — Hyperparameter sensitivity (design-review follow-up, separate pass)

Tests a critical design review's untested hypothesis: that `GAMMA=1.0` (no
discounting), `LEARNING_RATE=1e-2` (high for Adam + policy gradients), and
no entropy bonus together explain Goal 1's premature, fully-deterministic
convergence (`reward_final` bit-identical across consecutive episodes from
~episode 28-31 onward). Small dashboard, 100 episodes, seed 42 throughout.
Full numbers and methodology: `GOAL5_FINDINGS.md`.

- **Learning rate alone is the one clean fix.** `lr=1e-3` (γ=1.0 unchanged)
  never bit-collapses within 100 episodes and reaches a last-10-episode mean
  reward of **0.4606**, above the collapsed default's 0.4252 (+13.9% vs. the
  default's own +4.3%), with `valid_actions` never dropping below 21 (vs.
  the default's 32) — no dangerous side effects. `lr=1e-4` also avoids
  collapse but is too slow to have improved within 100 episodes.
- **Discounting alone (lower γ, `LEARNING_RATE=1e-2` unchanged) is actively
  harmful — the most striking finding of this pass.** `γ=0.95` **permanently**
  loses the ability to sample a single structurally-valid action from
  episode 44 onward (0 of 4,000 attempts valid, every episode through 100;
  `reward_final` locked at 0.0). `γ=0.99` is similarly severe but oscillates
  rather than locking in (last-10 mean reward 0.0851, **−80.1%** vs. its own
  first-10 mean). This is the opposite of what the hypothesis predicted:
  discounting does not produce a healthier, less-collapsed policy at the
  current learning rate — it produces a different, more severe failure
  (total loss of valid-action sampling, not just early convergence).
- **Entropy bonus (coefficient 0.01 only, at production defaults) is
  inconclusive, not a clean fix.** It never bit-collapses and ends at a
  reasonable final reward (0.4427), but hits the same near-total
  valid-action bottleneck as the gamma runs (89 of 100 episodes below the
  20-action/10% validity floor) before partially recovering late in
  training — unlike gamma-alone, it never fully flatlines to zero. A second,
  smaller coefficient that might avoid the bottleneck entirely was planned
  but not run (time budget).
- **One combined config is informative about interaction:** `lr=1e-3/γ=0.99`
  uses the exact γ that alone caused total breakdown, yet trains cleanly
  (never drops below 21 valid actions) and reaches the best reward of
  anything tested (0.4658, **+14.7%**) — suggesting gamma's harmful effect at
  the current LR is conditional on that LR, not intrinsic to discounting.
  Based on two data points, not a full grid.
- **Honest verdict: the hypothesis is partially, not fully, supported.**
  Learning rate is confirmed as the real driver of the observed collapse.
  Discounting and the entropy bonus, tested alone at the current learning
  rate, are net *negative* changes in this evaluation, not net-positive
  ones — they should not be recommended as standalone fixes without also
  lowering the learning rate. A large-dashboard confirmation run and a
  second entropy coefficient were both cut from scope for time; see
  `GOAL5_FINDINGS.md` for the full, explicit list of what was and wasn't
  completed.

## New issue found, not fixed

**File:** `openESEA_interpreter/backend/core/DashboardRLModel/Dashboard/Environment.py`,
line 341, inside `get_parameter_mask()`'s nested `valid_change()` function.

```python
# Grouped/stacked bar to grouped/stacked bar or table
if visualisation in groupedBarVisualisations:
    if newType in groupedBarVisualisations or newType == VisualisationType.TABLE:
        return True
```

**Why this looks like a bug:** every other branch of `valid_change()` tests
`visualisation_type` (the current visualisation's type, extracted at the
top of the function as `visualisation_type = visualisation.visualisationType`)
against a list of `VisualisationType` enum members — e.g. `if
visualisation_type == VisualisationType.SINGLE`, `if visualisation_type in
fractionalVisualisations`, `if visualisation_type in categoricalVisualisations`,
`if visualisation_type == VisualisationType.LINE`. This one branch instead
tests `visualisation` (the whole `Visualisation` object) against
`groupedBarVisualisations` (a list of `VisualisationType` enum values). A
`Visualisation` instance is never equal to a `VisualisationType` enum
member, so `visualisation in groupedBarVisualisations` is **always
`False`**, regardless of the visualisation's actual type — the branch can
never execute, and any visualisation currently typed Grouped Bar Chart or
Stacked Bar Chart falls through to `return False` at the end of the
function for every possible target type.

**Effect:** `ChangeVisualisationType` is silently masked as invalid for
*every* target type whenever the source visualisation is a Grouped Bar
Chart or Stacked Bar Chart — the model (and any script using the same
masking, including a live user of the product) can never be offered a
"change visualisation type" recommendation starting from one of these two
chart types, even though the intent (visible from the comment and the
pattern of every neighbouring branch) is clearly to allow such a
visualisation to change to another grouped/stacked bar variant or to a
Table.

**Scope of impact on this evaluation:** confirmed (by grepping all
dashboard fixtures used) that only the synthetic `large` fixture (1 of its
15 visualisations is a Stacked Bar Chart) is affected among everything
actually trained/evaluated in this pass. None of the 6 real dashboards
converted from the seeded database use Grouped Bar Chart or Stacked Bar
Chart. Likely negligible effect on `large`'s aggregate reward (1 of 15
visualisations, one action type unavailable to it), but worth fixing
separately from this evaluation, since it silently restricts the live
product's recommendations for any dashboard containing these chart types,
not just this evaluation's results.

**Not fixed, per the brief's instruction to only apply the two named Goal-0
reward-formula fixes and report anything else found.**

## Goal 0 reminder (bug fixes this evaluation depends on)

Two bugs were found and fixed in `Environment.py`, both verified to keep
every reward component in `[0,1]`: (1) reward weights were applied twice
(`w² · r` instead of `w · r`) in the training-time reward path — fixed to
apply each weight once; (2) the Decluttering formula scored "no item limit
set" as near-maximum decluttering (a `0/0`-adjacent edge case) — fixed with
an `itemLimit ≤ 0` guard. All numbers in this document are post-fix unless
marked otherwise. See `README.md` and `METHODOLOGY.md` for full technical
detail and the complete pre-fix/post-fix numbers for every goal.
