# RL Evaluation — Outputs

Raw data produced for `RL_Evaluation_Brief.md`. This directory contains the
scripts and CSV/text outputs for Goals 1–4 (4e skipped as an optional
stretch goal per the brief), plus a later Goal 5 follow-up (see below). No
thesis text, tables, or plots are included here — that synthesis happens
later from these numbers. For a standalone, numbers-first summary written to
be lifted directly into thesis text, see `THESIS_SUMMARY.md`. For the full
architecture/methodology reference (network, state/action space, reward
formulas, training loop, real-dashboard conversion), see `METHODOLOGY.md` —
this file only covers *what was run and what it found*; `METHODOLOGY.md`
covers *how the system and the evaluation work*, and doesn't need to change
every time results are re-run. For Goal 5 (hyperparameter sensitivity —
learning rate, discount factor, entropy bonus), see `GOAL5_FINDINGS.md`,
summarised briefly below.

## Contents

```
RL_Evaluation/
  scripts/
    dashboard_fixture.py             # small/large synthetic test dashboards + Goal 2 states
    rl_common.py                     # shared env/reward/training/baseline helpers (Goal 4)
    goal1_training_run.py            # Goal 1: instrumented training loop -> per-episode CSV
    goal2_weight_sensitivity.py      # Goal 2: reward-weight sensitivity -> CSV
    goal3_training_budget_summary.py # Goal 3: reads a Goal 1 CSV -> adequacy summary (appends)
    goal4_pipeline.py                # Goal 4a-4d: per-dashboard train + frozen-eval + baselines
    goal4f_zero_out_ablation.py      # Goal 4f: zero-out (not just reweight) ablation
    db_dashboard_loader.py           # converts seeded dev-DB dashboards to model input JSON
    export_dashboard_jsons.py        # dumps dashboard_fixture.py constants to JSON
    goal5_hyperparameter_sensitivity.py  # Goal 5: LR/gamma/entropy-bonus sweep driver -> CSV
    goal5_entropy_network.py         # Goal 5: evaluation-only entropy-bonus AgentNetwork variant
  results/
    goal1_training_log_100ep.csv                  # small (6-viz) dashboard, 100 episodes
    goal1_training_log_100ep_large_dashboard.csv  # large (15-viz) dashboard, 100 episodes
    goal1_training_log_500ep_stretch.csv          # small dashboard, 500-episode stretch run
    goal2_weight_sensitivity.csv
    goal3_training_budget_summary.txt
    goal4a_frozen_policy_eval.csv
    goal4a_determinism_check.csv
    goal4b_baselines.csv
    goal4c_multi_dashboard_robustness.csv
    goal4c_training_log_real_*.csv                # per-real-dashboard Goal-1-style training logs
    goal4d_wallclock_timing.csv
    goal4f_zero_out_ablation.csv
    goal5a_learning_rate_sweep.csv                # Goal 5: LR sweep summary (+ reused baseline row)
    goal5b_gamma_sweep.csv                        # Goal 5: gamma sweep summary (+ reused baseline row)
    goal5c_combined_configs.csv                   # Goal 5: LR+gamma combined configs summary
    goal5d_entropy_bonus.csv                      # Goal 5: entropy-bonus variant summary
    goal5_training_log_*.csv                      # per-config Goal-1-style training logs for Goal 5
    pre_bugfix/                      # Goal 1-4 outputs from BEFORE the Goal 0 reward-bug fixes
    goal3_training_budget_summary.INCOMPLETE_STALE_BACKUP.txt  # see "Data-quality notes" below
```

## Goal 0 — reward-function bug fixes (context for everything below)

Two genuine implementation bugs were found and fixed in
`openESEA_interpreter/backend/core/DashboardRLModel/Dashboard/Environment.py`,
committed as `8ec4318` ("Small fixes to reinforcement learning model",
2026-08-10 13:22) together with a training-related fix in `AgentNetwork.py`,
and a further environment fix in `110b1b2` ("Reset live dashboard to initial
state...", 2026-08-10 16:26). See `METHODOLOGY.md` §B.4 for the full
technical description of both reward bugs and their fixes. In short:

1. **Weights applied twice** in `collect_state_rewards()` + `reward()` —
   fixed to apply each weight exactly once. This affects **training itself**
   (`reward()` is what `env.step()` calls) — so Goals 1 and 3 (and Goal 4's
   training runs) are affected.
2. **Decluttering formula's zero-item-limit edge case** scored "no limit set
   at all" as near-maximum decluttering — fixed with an `itemLimit <= 0`
   guard (keeping the `dataItems` divisor, not switching to `itemLimit` as
   the brief's literal instruction suggested — see METHODOLOGY.md §B.4 for
   why). This affects **any code path that calls `reward_decluttering`**,
   which includes training (Goal 1/3), Goal 2 (calls the reward-component
   functions directly), and Goal 4.

Additionally, `110b1b2` fixed a **state-mismatch bug**: `self.dashboard` was
never reset between episodes, so it accumulated every action ever applied
across the whole training run while the state vector fed to the network
always represented `initial_dashboard` — a training-only bug (affects Goal 1
and Goal 4's per-dashboard training, not Goal 2, which never reuses an `env`
across multiple actions).

**All results in this directory (outside `pre_bugfix/`) were generated
against the code with both fixes applied**, verified as follows (see "Data
quality / staleness diagnosis" below for the full audit): Goal 1, 3, and all
of Goal 4's result files are timestamped after both fix commits. Goal 2's
result file has an earlier timestamp than the git commits (the fix was
apparently written to the file, and the script run against it, before the
commit was made) — this was verified **numerically**, not just by
timestamp: re-running `goal2_weight_sensitivity.py` against the current
checked-out code reproduces the existing `goal2_weight_sensitivity.csv`
byte-for-byte (the script is a deterministic enumeration, no RNG), and the
component-level arithmetic for the one action Bug 2 actually changes
(`RemoveItemLimit`, which zeroes the item limit) matches the *fixed* formula,
not the old buggy one. **No re-run was needed for Goal 2.**

## Data quality / staleness diagnosis (what was checked, and what needed fixing)

- **Goal 2 (`goal2_weight_sensitivity.csv`): NOT stale, verified, not
  re-run-with-different-results.** The script never calls the buggy
  `collect_state_rewards()`/`reward()` path at all — it calls the four
  reward-component functions directly and does its own single weighted sum
  (`compute_final_reward()`), so Bug 1 (double-weighting) never affected
  Goal 2 regardless of when the fix landed. Bug 2 (decluttering) *is* called
  directly by Goal 2, and is confirmed fixed in the current result (see
  above). The `AgentNetwork.py` fix and the `110b1b2` dashboard-reset fix
  are both training-only and irrelevant to Goal 2 (no training, no reused
  `env` across steps). Re-running the script live during this pass
  reproduced the exact existing CSV, confirming reproducibility.
- **Goal 1 / Goal 3 / Goal 4: correctly post-fix, but Goal 3's summary file
  was stale/incomplete and has been regenerated.** The old
  `goal3_training_budget_summary.txt` contained (a) a correct entry for the
  100-episode small-dashboard run, (b) a correct entry for the current
  100-episode large-dashboard run, but also (c) a **stray, contradictory**
  "large 15-viz dashboard" entry (first-10/last-10 means 0.3874/0.3896) that
  matches *neither* the current large-dashboard CSV nor any other file on
  disk — almost certainly left over from an earlier run of the large
  dashboard whose CSV was since overwritten (the script always *appends*
  when given an explicit CSV path, so a stale entry from a previous
  invocation survives unless the file is deleted first). It was also
  **missing the 500-episode stretch run's summary entirely**, despite the
  brief explicitly requiring it. The stale/incomplete file has been preserved
  as `results/goal3_training_budget_summary.INCOMPLETE_STALE_BACKUP.txt`,
  and `goal3_training_budget_summary.txt` has been regenerated cleanly (one
  entry per current CSV: small 100ep, large 100ep, 500ep stretch — see Goal
  3 findings below for the numbers).
- **Goal 4c real-dashboard training logs: no crashes, but one dashboard
  (`real_cority_quality_monitor`) has a genuine, sustained validity-floor
  concern** — see "Goal 4 findings" below, "Anomalies" bullet.

## How each goal was produced

See `METHODOLOGY.md` §B.6 for the full script-by-script technical
description. Summary:

- **Goal 1** (`goal1_training_run.py`): re-implements the exact per-episode
  training loop (masking, sampling, action space, network, gradient update
  unchanged) with per-episode logging of combined `R_Final`, the four
  unweighted reward components, and valid/invalid sampled-action counts.
- **Goal 2** (`goal2_weight_sensitivity.py`): no training. Enumerates every
  action passing the model's own masks from a fixed dashboard state, applies
  each, and recomputes `R_Final` under 4 weight sets using the unmodified
  reward-component functions.
- **Goal 3** (`goal3_training_budget_summary.py`): consumes a Goal 1 CSV,
  reports mean `R_Final` over the first/last 10% of episodes, percent
  change, and a plateau judgment.
- **Goal 4** (`goal4_pipeline.py` for 4a-4d, `goal4f_zero_out_ablation.py`
  for 4f): trains a fresh model per dashboard (same 100-episode protocol as
  Goal 1), then runs frozen/greedy evaluation, random + rule-based
  baselines, per-dashboard convergence/robustness stats, wall-clock timing,
  and (separately) a zero-out ablation of each reward component.

## Key findings — Goal 1 (Training / Reward Convergence Log)

Post-fix numbers (see `goal3_training_budget_summary.txt` for the full
generated text this is drawn from):

- **Small dashboard (6 viz), 100 episodes.** Converges by ~episode 28
  (post-fix; was ~episode 10-14 pre-fix — see "pre-fix vs. post-fix" below).
  First-10-episode mean `R_Final` = 0.4077, last-10 = 0.4252 (+4.3%),
  half-over-half change −1.4%, judged **plateaued**. Valid actions per
  episode ranged 32-200 (out of 200 steps), invalid attempts 0-421 — never
  close to the 10%-floor (20 valid actions) requirement.
- **Large dashboard (15 viz), 100 episodes.** Converges by ~episode 6
  (post-fix). First-10 mean = 0.2900, last-10 = 0.2798 (**−3.5%**, i.e. the
  reward is essentially flat but drifts slightly *down*, not up, over the
  run — judged plateaued by the slope/half-over-half heuristic, but this is
  a real qualitative difference from the small dashboard's slight upward
  drift). Valid actions ranged 21-200, invalid attempts 0-661; **episode 3
  came close to the 10% floor** (21 valid actions against a >20 requirement,
  661 invalid attempts) before the policy stabilised — a much smaller and
  earlier near-miss than the pre-fix run showed (pre-fix: episodes 8-10,
  21/21/23 valid, up to 3,502 invalid attempts in episode 9), but the same
  qualitative pattern: the large, more varied dashboard has less safety
  margin against the floor early in training than the small one does.
- **500-episode stretch run (small dashboard).** First-50 mean = 0.4313,
  last-50 mean = 0.4252 (−1.4%), plateaued. `R_Final` at episode 500 equals
  `R_Final` at episode ~28 through episode 100 to 4 decimal places (0.4252)
  — extending training 5x further produces no further gain. This is the
  same qualitative conclusion as pre-fix ("100 episodes is enough for this
  dashboard, confirmed out to 500"), just at a different converged reward
  value.

## Key findings — Goal 2 (Reward Weight Sensitivity Check)

**This is the goal whose qualitative conclusion changed from pre-fix to
post-fix.**

- **`bar_chart_5items`** (bar chart, 5 items, `itemLimit=6` — the thesis's
  Action Space worked-example state): post-fix top-1 is **"Change to Pie
  Chart"** for weight sets 1-3 (reward 0.616/0.645/0.55), and **"Remove Item
  Limit"** for weight set 4 (equal weights; reward 0.65, vs. 0.525 for Pie
  Chart under that same set). **The #1 recommendation is no longer robust
  across all 4 weight configurations** — it flips depending on the weights.
  ("Change to Line Chart" — the thesis's published outcome for this exact
  state — is not, and never was, a reachable candidate action here at all:
  see "Resolved: the SENSITIVITY_STATE_BAR_5 worked-example question" below.)
- **`pie_chart_9items`** (pie chart, 9 items): post-fix top-1 is **"Change to
  Bar Chart"** across **all 4** weight sets (reward 0.56/0.70/0.607/0.70) —
  this state's #1 recommendation *is* robust to the weight choice, same as
  pre-fix.
- **Why Goal 2's conclusion changed for `bar_chart_5items` but not
  `pie_chart_9items`:** the state that changed (`bar_chart_5items`) is the
  one whose top candidate action (`RemoveItemLimit`) directly touches the
  Decluttering component that Bug 2 fixed — zeroing the item limit used to
  be scored as near-maximum decluttering (bug), now correctly scores as
  minimum decluttering (0), which demotes `RemoveItemLimit` from rank 1 to
  rank 2 for 3 of the 4 weight sets. `pie_chart_9items`'s top action
  (`ChangeVisualisationType(to=Bar Chart)`) doesn't touch item limits at all,
  so it was unaffected by either bug fix.
- **Pre-fix (for context — see `results/pre_bugfix/goal2_weight_sensitivity.csv`):**
  `bar_chart_5items`'s top-1 was **"Remove Item Limit"** across all 4 weight
  sets (reward 0.696/0.745/0.729/0.775) — robust pre-fix, not robust
  post-fix. `pie_chart_9items`'s top-1 was "Change to Bar Chart" across all
  4 sets both pre- and post-fix (reward values differ, ranking doesn't).

## Resolved: the SENSITIVITY_STATE_BAR_5 worked-example question

**Question:** for `SENSITIVITY_STATE_BAR_5` (bar chart, 5 items — the same
state as the thesis's published Action Space worked example, whose published
outcome is "change to Line Chart"), what was the model's actual **pre-fix**
top-1 recommendation?

**Answer: "Remove Item Limit," not "Change to Line Chart."** From
`results/pre_bugfix/goal2_weight_sensitivity.csv`: `RemoveItemLimit` ranks
#1 across all 4 pre-fix weight sets (reward 0.696/0.745/0.729/0.775),
ahead of `ChangeVisualisationType(to=Pie Chart)` (rank 2) and
`ChangeVisualisationType(to=Table)` (rank 3).

**Additional, important context found while checking this:** "Change to
Line Chart" is not just absent from the top-1 spot — it was **never a
structurally valid candidate action for this state at all**, pre-fix or
post-fix. `Environment.py::get_parameter_mask`'s `valid_change()` function
only allows a `Bar Chart` (a "categorical" visualisation) to change to
another categorical type (Pie) or to Table (or to Single Value Display if
it has exactly 1 data item) — never to Line Chart, which is reserved for
transitions *from* an existing Line/Multi-Series-Line source. This is by
design (categorical vs. temporal visualisation families), not a bug. So the
real model, under its own masking rules, could **never** have produced
"Change to Line Chart" as a candidate for a Bar Chart state, regardless of
reward weights or the Goal-0 bug fixes.

**Conclusion for the thesis:** the published worked example's outcome was
illustrative/hypothetical, not a captured real-model output — neither the
pre-fix nor the post-fix real model ever ranks, or could even consider,
"Change to Line Chart" for this state. No thesis text change is required
per the brief, but if the worked example is kept, it may be worth a caveat
noting that the real model's actual top-1 pick for this exact state is
weight-sensitive post-fix (Pie Chart or Remove Item Limit, never Line
Chart).

## Key findings — Goal 3 (Training Budget Adequacy)

See the regenerated `goal3_training_budget_summary.txt` (3 entries: small
100ep, large 100ep, 500ep stretch — numbers reproduced in the Goal 1 section
above). **Verdict: 100 episodes is sufficient for both dashboard sizes** —
both plateau well inside the budget (small by ~episode 28, large by
~episode 6) and the 500-episode stretch confirms no further gain past
episode ~28 for the small dashboard. The large dashboard's early-training
safety margin against the 10% valid-action floor is thinner than the small
dashboard's (episode 3 dipped to 21/200 valid actions, barely above the
20-action floor) — this doesn't change the "100 episodes is enough"
verdict, but it's a real caveat about *how close* training got to the floor
along the way, and Goal 4c (below) shows this concern is much more serious
for at least one real dashboard.

## Key findings — Goal 4 (Frozen-Policy Evaluation, Baselines, Multi-Dashboard Robustness)

Framing (per the brief): each dashboard gets its own independently-trained
model, evaluated on itself — not one model trained once and tested on
unseen dashboards. 8 dashboards were run through the full Goal 4 pipeline:
the 2 synthetic fixtures (`small`, `large`) plus 6 real dashboards converted
from the project's seeded dev database (`real_energy_climate`,
`real_cority_quality_monitor`, `real_accuvio_resource_overview`,
`real_esgbook_score_analytics`, `real_rimm_topic_scorecard`,
`real_measurabl_data_cards` — see `METHODOLOGY.md` §B.7-B.8 for how these
were derived and why these 6 of the 16 available real dashboards were
chosen).

**4a — Frozen-policy (greedy) evaluation.** The live top-K inference path
(`forward_predict`) is fully deterministic — it enumerates and ranks by
probability rather than sampling (`torch.distributions.Categorical.sample()`
is never called on that path). Confirmed empirically: `goal4a_determinism_check.csv`
shows `deterministic=True`, `consistency_fraction=1.0` (3/3 repeat runs
agree on the #1 action) for **all 8 dashboards** — a single run per
dashboard is sufficient and was used for `goal4a_frozen_policy_eval.csv`'s
top-K tables. Top-1 rewards range from 0.2855 (`large`, the most complex
fixture) to 0.60 (`real_rimm_topic_scorecard`).

**4b — Baseline comparison.** Trained-model greedy top-1 vs. 100-sample
random-policy baseline (mean ± std) vs. rule-based heuristic baseline, all
under the same production reward weights (`goal4b_baselines.csv`):

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

**Honest finding:** the trained model beats *both* baselines on **5 of 8**
dashboards (small, large, accuvio, rimm, measurabl). On the other **3 of 8**
(energy_climate, cority_quality_monitor, esgbook_score_analytics), the
trained model's top-1 reward is **exactly tied** with the rule-based
heuristic (identical reward to full float precision in all 3 cases — the
model's greedy pick and the hand-written rule select actions of the same
reward value, though not always the same visualisation index) but is
**beaten by the mean of 100 random samples** by 5-13%. The model never
loses to the rule-based baseline outright and never loses by a lot to
random — but "does the trained model beat a simple heuristic" is not a
uniform "yes" across dashboards, and that's reported here as-is, not
smoothed over.

**4c — Multi-dashboard robustness.** `goal4c_multi_dashboard_robustness.csv`
gives convergence/robustness stats per dashboard. Convergence speed varies
substantially (episode 6 to episode 28 across the 8 dashboards) and does
not track dashboard size in a simple way (the largest dashboard, `large`
with 15 viz, converges fastest at episode 6; `small` with only 6 viz
converges slowest at episode 28) — so convergence speed looks more
sensitive to the specific mix of visualisation types and reward tension
present than to raw dashboard size. Final-vs-initial reward change ranges
from −3.5% (`large`, a slight decline) to +32.0% (`real_esgbook_score_analytics`).

**Anomaly — validity-floor breach on `real_cority_quality_monitor`.**
Checking each dashboard's per-episode `valid_actions`/`invalid_attempts`
(from the `goal4c_training_log_real_*.csv` files) against the intended
10%-valid-action floor (≥20 valid actions per 200-step episode): 6 of the 8
dashboards never dip below 20 valid actions in any episode. **Two do:**
`real_measurabl_data_cards` dips to 16 valid actions in episodes 3-4 only
(a brief, minor dip, recovers immediately). `real_cority_quality_monitor` is
far more serious — it stays **below the 20-action floor for 9 of episodes
12-21** (episodes 12-18, 20, 21), bottoming out at **only 3 valid actions**
in episode 18 (1.5% of the 200-step budget, against invalid attempts of
3,997 — within 3 of the training loop's hard cap of 4,000 total attempts
per episode). This means for roughly a 10-episode stretch, this dashboard's
training was effectively relying on the hard cap to end the episode at all,
rather than genuinely satisfying the "10% valid" design intent. The training
run did not crash and reward did recover and plateau afterward
(`goal4c_multi_dashboard_robustness.csv` reports this dashboard
`plateaued=True`, convergence estimate episode 19 — right at the tail of
the problem window), but this is flagged here as a genuine, dashboard-specific
weakening of the "100 episodes / 10% floor is comfortably sufficient"
conclusion — worth a sentence in Discussion/Limitations alongside the
large-fixture's milder version of the same concern (Goal 1/3 above).

**4d — Wall-clock training time.** `goal4d_wallclock_timing.csv`: total
100-episode wall-clock time ranged ~1,765s (`real_accuvio_resource_overview`,
~29 min) to ~7,388s (`real_cority_quality_monitor`, ~123 min — the
outlier, plausibly related to the validity-floor anomaly above: many more
invalid-sample retries mean many more forward passes per episode before an
episode can end). Wall-clock time to reach the convergence episode
specifically ranged ~110s (`large`) to ~1,692s (`real_cority_quality_monitor`,
again the outlier). This is real per-dashboard training latency a user
would wait through in the live product; it does not scale cleanly with
visualisation count alone.

**4f — Deeper (zero-out) ablation.** `goal4f_zero_out_ablation.py` extends
Goal 2 by fully zeroing (not just reweighting) one reward component at a
time, across 4 test states (`bar_chart_5items`, `pie_chart_9items`,
`small_dashboard`, `real_energy_climate`). Whether the #1 recommendation
changes is state-specific and component-specific, not uniform:

| state | changes when zeroing... | top-1 stable under... |
|---|---|---|
| `bar_chart_5items` | Decluttering (→ Remove Item Limit) | Appropriate-Vis-Types, Chart Variety, Data Completeness |
| `pie_chart_9items` | Appropriate-Vis-Types, Data Completeness (→ AddItemLimit(2)) | Decluttering, Chart Variety |
| `small_dashboard` (6-viz fixture, all visualisations as candidates) | Appropriate-Vis-Types (→ AddItemLimit(vis=2, limit=2)) | Decluttering, Chart Variety, Data Completeness |
| `real_energy_climate` | *(none)* | all 4 components |

`real_energy_climate`'s top-1 recommendation is fully robust to zeroing any
single reward component — the most robust of the 4 states tested. The two
single-visualisation sensitivity states each have exactly one component
whose removal flips the #1 pick, and it's a *different* component in each
case (Decluttering for the bar chart, Appropriate-Vis-Types/Data-Completeness
for the pie chart) — consistent with Goal 2's reweighting finding that
different states are sensitive to different parts of the reward.

## Goal 5 — Hyperparameter Sensitivity (design-review follow-up)

A later, separate pass (not part of the original Goals 1-4 brief) testing
three specific hypotheses a critical design review flagged as *plausible but
untested*: that `GAMMA=1.0` (no discounting), `LEARNING_RATE=1e-2` (high for
Adam + policy gradients), and the absence of an entropy bonus together
explain the premature, fully-deterministic policy collapse visible in the
Goal 1 training logs above (`reward_final` becoming bit-for-bit identical
across consecutive episodes from ~episode 28-31 onward on the small
dashboard). Full methodology, all numbers, and the complete write-up are in
`GOAL5_FINDINGS.md`; summary here:

- **Learning rate is confirmed as the dominant, and the only cleanly
  beneficial, lever.** Lowering it alone to `1e-3` prevents the bit-identical
  collapse within 100 episodes and ends with a last-10-episode mean reward
  of 0.4606 (vs. the collapsed baseline's 0.4252) with no pathological side
  effects (though a temporary mid-training rough patch, elevated but
  self-recovering invalid-action attempts, episodes ~25-55). `1e-4` avoids
  collapse too but is too slow to have caught up within 100 episodes.
- **Discounting alone (lower gamma, keeping `LEARNING_RATE=1e-2` unchanged)
  is actively harmful, not a fix.** Both `γ=0.99` and `γ=0.95` degrade
  training into a state where the policy can barely sample a single
  structurally-valid action per 200-step episode (hitting the training
  loop's 4,000-attempt hard cap). `γ=0.95` is the most severe finding in
  this evaluation: from episode 44 onward it **permanently** loses the
  ability to sample any valid action at all (0 valid actions in 4,000
  attempts, every episode through 100) — a genuine collapse, but to a broken
  state, not a good plateau.
- **The entropy-bonus variant (coefficient 0.01, at production defaults) is
  a mixed, inconclusive result, not a clean fix either.** It hits the same
  near-total valid-action bottleneck the gamma runs do (89 of 100 episodes
  below the 20-action validity floor) but — unlike gamma-alone — never fully
  flatlines, and ends at a reasonable final reward (0.4427). Whether a
  smaller coefficient would avoid the bottleneck entirely is untested.
- **Verdict: the original hypothesis is partially supported.** The evidence
  points at learning rate as the real driver of the observed collapse;
  discounting and (at the one coefficient tested) the entropy bonus are, if
  anything, counterproductive on their own at the current learning rate. One
  combined config (`lr=1e-3/γ=0.99`) suggests gamma's harmful effect is
  conditional on the high learning rate rather than intrinsic to discounting
  itself, but this is based on two data points, not a full grid.
- **Scope actually completed vs. the original plan:** LR sweep (2 configs),
  gamma sweep (2 configs), combined configs (2 configs), and one
  entropy-bonus run all completed on the `small` fixture. A second entropy
  coefficient and a large-dashboard confirmation run were both cut for time
  (see `GOAL5_FINDINGS.md`'s "Deviations from the original plan").

## New issue found during this evaluation, not fixed

Per the brief, code bugs found outside the two Goal-0 bugs are documented,
not fixed. See `THESIS_SUMMARY.md`'s "New issue found, not fixed" section
for the full write-up: `Environment.py::get_parameter_mask`'s `valid_change()`
function has a variable-name bug (`visualisation` instead of
`visualisation_type`) in its Grouped/Stacked Bar Chart branch, meaning
`ChangeVisualisationType` is silently always-invalid from a Grouped or
Stacked Bar source, regardless of target type. Confirmed to affect only the
`large` synthetic fixture among dashboards actually evaluated in this pass
(none of the 6 real dashboards use Grouped/Stacked Bar Chart).

## Assumptions / provenance notes

- **Training dashboards.** The repository does not retain the exact
  dashboard used for the thesis's original training run; `small` (6 viz)
  and `large` (15 viz) in `dashboard_fixture.py` are representative
  reconstructions, not a byte-for-byte replay. The 6 real dashboards are
  independently-converted seeded dev-database specifications (see
  `METHODOLOGY.md` §B.7 for the exact conversion rule and provenance).
- **Goal 2 test states.** `SENSITIVITY_STATE_BAR_5` reuses the thesis's own
  worked-example state (bar chart, 5 items, `[5,1,0.06,0,0.02,0]`).
  `SENSITIVITY_STATE_PIE_9` is an added second test case (pie chart, 9
  items) for robustness.
- **Seeding.** All training runs use `torch.manual_seed(42)`; the original
  thesis training run had no recorded seed.
- **Stretch run.** The 500-episode run is a fresh, independent run from
  episode 1 (not a continuation of the 100-episode run).
- **Pre-fix results.** `results/pre_bugfix/` holds the Goal 1-4 outputs
  generated before the Goal 0 reward-function fixes, kept for the explicit
  before/after comparisons throughout this document. It does not include a
  `real_measurabl_data_cards` training log — that real dashboard was added
  to the Goal 4 test set after the Goal 0 fixes, so it has no pre-fix
  counterpart.
