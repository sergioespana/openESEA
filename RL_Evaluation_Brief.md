# RL Model Evaluation — Brief for Codebase Agent

## Context

This is for a master's thesis (openESEA dashboarding + reinforcement learning model,
repo: https://github.com/sergioespana/openESEA). The RL model is a policy-gradient
actor-critic network (PyTorch) that recommends dashboard edits (add/remove item limit,
change visualisation type). The thesis currently has zero quantitative evidence that
the model actually learns anything — it describes the architecture in detail but never
shows a training curve, a sensitivity check on the reward weights, or an explicit
statement on whether the training budget (100 episodes) was sufficient. Final
tables/plots will be built later from whatever raw data these produce — for now we
just need the raw numbers/logs in a clean, reusable format (CSV/JSON preferred).

**Status: Goals 1-3 were done, but see Goal 0 below — two reward-function bugs were
found after the fact, and Goals 1-3 need a re-run against the corrected reward before
their results can be treated as final.** Summary of what was found under the
*pre-fix* (buggy) reward function, for context — see `RL_Evaluation/README.md` for
the full writeup, scripts, and results:
- Reward converges almost immediately (~episode 10) and is fully flat by episode 100
  on the small (6-viz) dashboard; confirmed to stay flat all the way to episode 500 in
  a separate stretch run — 100 episodes was sufficient for this dashboard.
- On a larger (15-viz) dashboard, convergence also happens well within 100 episodes,
  but the safety margin against the minimum 10%-valid-action floor was much thinner
  early in training (episodes 8-10 came close to the floor) — the "100 episodes is
  enough" conclusion does not obviously generalise to more complex dashboards without
  more headroom.
- The #1-ranked recommended action is identical across all 4 reward-weight
  configurations tested, for both test dashboard states — the headline recommendation
  is robust to the reward-weight choice, even though lower-ranked candidates do shift.

**Goal 4 (below) is new.** It was not in the original brief. Read it in full before
starting — it changes how test dashboards should be handled going forward (see
"Real dashboards" note in Goal 4).

Existing methodology to preserve (do not change unless a goal below explicitly asks
you to): 100 training episodes, up to 200 time steps per episode, minimum 10% valid
sampled-action success rate per episode, top 10 highest-probability actions collected
as candidate recommendations per episode.

Reward function weights currently in use (heuristically chosen — this is exactly what
Goal 2 interrogates, and what Goal 4's baseline comparison contextualises):
- Decluttering: 1.0
- Appropriate Visualisation Types: 0.8
- Chart Variety: 0.5
- Data Completeness: 0.2

---

## Goal 0 — Fix two reward-function bugs, then re-run Goals 1-3

**STATUS UPDATE (post your last message):** both bugs are fixed and verified (rewards
stay in `[0,1]`, no crashes). Bug 2's actual fix ended up different from the literal
instruction below — dividing by `itemLimit` turned out to be unbounded/perverse, so
you correctly kept the `dataItems` divisor and added a guard for `itemLimit ≤ 0`
instead. That's accepted as the right fix; the thesis text will be updated to match
your corrected formula, not the original instruction. Goal 2 is re-run. Goal 1's
small/large re-runs are in progress; Goal 3 to follow.

**Two things needed from you before proceeding further:**

1. **Goal 4 — hold off until Goals 1 and 3 are confirmed done and the README's
   pre-fix/post-fix comparison reads coherently, then proceed.** Don't run it in
   parallel with Goals 1/3. Given the 3+ day runtime last time was mostly the machine
   sleeping, please disable sleep for the duration of this run (e.g. on Windows,
   `powercfg /change standby-timeout-ac 0`, or Settings → Power → never sleep while
   plugged in) before kicking it off.
2. **Worked-example check:** `SENSITIVITY_STATE_BAR_5` is the same starting state as
   the thesis's existing Action Space worked example (bar chart, 5 items,
   `[5,1,0.06,0,0.02,0]`), whose published outcome is "change to Line Chart." Your
   post-fix Goal 2 result shows the real top-1 for that state is "Change to Pie
   Chart" (weight sets 1-3) or "Remove Item Limit" (set 4) — neither is "Line Chart."
   **What was the *pre-fix* top-1 for that exact state** (should be in
   `results/pre_bugfix/goal2_weight_sensitivity.csv` once that move happens)? If it
   was "Line Chart," the worked example was a real (now-invalidated) model output and
   will need regenerating against the corrected reward; if not, it was illustrative
   and just needs a caveat noting the real model's top pick for that state is
   weight-sensitive. Report back which case it is — no thesis edit needed from you
   either way, just the data point.

---

## Goal 0 (original instructions, for reference)

**This supersedes the "Goals 1-3 are done" status above.** Manually cross-checking
`Dashboard/Environment.py` against the thesis's own reward formulas turned up two
genuine implementation bugs (not just description mismatches). Both need fixing, then
Goals 1, 2, and 3 need one combined re-run against the corrected reward function —
treat the existing `RL_Evaluation/results/goal{1,2,3}_*` files as provisional/
pre-fix, not final.

### Bug 1 — reward weights applied twice

In `collect_state_rewards()`:
```python
state_reward = state_reward_weight * state_reward_function(self, state)  # weight applied here
state_rewards.append((state_reward, state_reward_weight))
```
Then in `reward()`:
```python
for reward, weight in current_state_rewards:
    current_state_reward += weight * reward   # weight applied AGAIN
    current_state_reward_weight += weight
normalized_reward = current_state_reward / current_state_reward_weight
```
Net effect: `normalized_reward = Σ(w_i² · r_i) / Σ(w_i)` instead of the intended
`Σ(w_i · r_i) / Σ(w_i)`. This exaggerates the influence of higher-weighted components
(Decluttering 1.0, Appropriate Vis Types 0.8) relative to lower-weighted ones (Chart
Variety 0.5, Data Completeness 0.2) beyond what the stated weights imply — and since
`reward()` is what training itself calls, this affected Goal 1's training runs and
Goal 3's adequacy conclusions too, not just Goal 2's sensitivity check.

**Fix:** apply each weight exactly once — either drop the multiplication in
`collect_state_rewards()` and keep it in `reward()`, or the reverse; either works as
long as it happens once before the sum, and `current_state_reward_weight` stays a
plain (not squared) sum of weights.

### Bug 2 — decluttering reward formula doesn't match the thesis

`reward_decluttering()` divides the excess-items term by `dataItems`:
```python
reward += 0.5 * (0 if visualisation.dataItems <= visualisation.itemLimit
                  else ((visualisation.dataItems - visualisation.itemLimit) / visualisation.dataItems))
```
The thesis's documented formula divides by `itemLimit` instead. Change the code to
divide by `itemLimit` — the thesis text is being treated as authoritative here, not
the code.

### What to re-run afterward

- Re-run `goal1_training_run.py` for both fixture dashboards (small + large) and the
  500-episode stretch run, all against the fixed reward function.
- Re-run `goal2_weight_sensitivity.py` for both existing test states
  (`SENSITIVITY_STATE_BAR_5`, `SENSITIVITY_STATE_PIE_9`).
- Re-run `goal3_training_budget_summary.py` against the new Goal 1 CSVs.
- **Keep the old (pre-fix) result files rather than overwriting them** — move the
  existing `results/goal{1,2,3}_*` files into a `results/pre_bugfix/` subfolder, and
  write the corrected re-runs to the original filenames/locations. Note in
  `RL_Evaluation/README.md` which set is which and why they differ — an honest
  before/after (here's what changed once this bug was found and fixed) may itself be
  worth a sentence in the thesis's Limitations section.
- Don't otherwise touch training hyperparameters, network architecture, action/state
  space, or masking as part of this — bug fix + re-run only, not a broader tuning
  pass. (Separately-identified design questions — discount factor, learning rate, no
  entropy bonus, the embedding layer's use of an LSTM over a single time step — are
  being written up as thesis limitations/future work, not code changes; do not act on
  those unless a future revision of this brief explicitly asks you to.)
- Update the "Key findings so far" section of `RL_Evaluation/README.md` with the new
  numbers, and flag clearly if the corrected results change any of the prior
  qualitative conclusions (e.g. "converges by ~episode 10", "#1 recommendation robust
  across weight configs").

---

## Goal 1 — Training / Reward Convergence Log — DONE

See `RL_Evaluation/README.md` and `RL_Evaluation/results/goal1_*.csv`. No further
action needed unless Goal 4's real dashboards (below) warrant additional runs using
the same `goal1_training_run.py` script.

---

## Goal 2 — Reward Weight Sensitivity Check — DONE

See `RL_Evaluation/README.md` and `RL_Evaluation/results/goal2_weight_sensitivity.csv`.
No further action needed unless Goal 4's real dashboards warrant additional test
states run through `goal2_weight_sensitivity.py`.

---

## Goal 3 — Training Budget Adequacy — DONE

See `RL_Evaluation/results/goal3_training_budget_summary.txt`. If Goal 4 adds new
training runs (e.g. on real dashboards), re-run `goal3_training_budget_summary.py`
against those new logs too, so each dashboard gets its own adequacy judgment rather
than assuming the small/large dashboard conclusions carry over.

---

## Goal 4 — Frozen-Policy Evaluation, Baselines, and Multi-Dashboard Robustness

**Why:** Goals 1-3 show the model learns *something* during training, but training
reward reflects exploratory/stochastic behaviour, not what a real user actually sees.
openESEA uses the model in inference mode (top-10 actions shown to the user, no
further learning) — so this is arguably closer to what the thesis needs to claim
works than the training curve is. There is also currently no baseline: a reward value
on its own doesn't tell a reader whether the model is doing anything better than
chance, or better than a simple hand-written rule.

**Framing note — read before starting:** the thesis's own text implies training
happens *per dashboard* (a fresh model trained on whichever dashboard is being
edited), not one global model trained once and expected to generalise to arbitrary
unseen dashboards. Goal 1 already followed this philosophy (separate runs for the
small and large dashboard, not one run claiming to cover both). Goal 4 continues that
pattern: **"robustness across dashboards" means independently retraining and
evaluating on each one, not testing a single frozen model on dashboards it never
trained on.** Don't build a train-once/test-on-unseen-data generalisation experiment
unless you have a specific reason to believe that's actually how the system is meant
to be used — check `core/DashboardRLModel/` for how training is actually invoked
(per-dashboard vs. global) if this is unclear, and flag it back if the assumption
above turns out to be wrong.

**Real dashboards — the user will supply several.** Design all Goal 4 scripts to take
a *folder of dashboard specifications* as input (reuse whatever the existing dashboard
fixture format is — see `dashboard_fixture.py` — or the actual openESEA YAML dashboard
format if that's easier to load directly), rather than hardcoding to the two existing
small/large fixtures. The two existing fixtures can stay as the default/fallback test
set for now; the user-supplied real dashboards get dropped into the same folder
structure and run through the identical pipeline once available. Don't block on
waiting for them — build and validate the pipeline against the existing fixtures
first, so it's a drop-in matter once the real dashboards arrive.

### 4a. Frozen-policy (greedy) evaluation

- After training converges (reuse the convergence points already found in Goal 1/3 —
  e.g. ~episode 14 for the small dashboard), freeze the trained weights and run the
  network in **deterministic/greedy** mode: argmax action selection, no gradient
  updates, no exploration sampling. Check whether the existing code has a clean way to
  do this (e.g. a `predict()`/`eval()` path) or whether greedy selection needs to be
  added as a thin wrapper around the existing sampling logic.
- For each test dashboard (existing fixtures + later, real dashboards), record the
  top-K recommended actions in this greedy mode, their $R_{Final}$, and the
  unweighted per-component reward breakdown for the #1 pick (reuse the same
  computation already used for Goal 1's per-episode component logging).
- **Consistency check:** if the eval path is truly deterministic (pure argmax), a
  single run per dashboard is sufficient — repeated evaluations on unchanged input
  and unchanged weights cannot differ. If there's any residual stochasticity in eval
  mode (e.g. sampling is used even at inference time, not argmax), run the evaluation
  10 times per dashboard and report what fraction of runs agree on the #1 action.
  State explicitly which of these two cases applies and why.

### 4b. Baseline comparison

- **Random-policy baseline:** for each test dashboard, sample uniformly at random from
  the same valid/masked action space the trained model uses (reuse the existing
  `get_action_mask`/`get_parameter_mask` logic from Goal 2), apply it, and compute
  $R_{Final}$. Repeat ~100 times per dashboard and report mean and standard deviation.
- **Rule-based heuristic baseline:** implement the simple threshold rule already cited
  in the thesis's Related Work (single value -> card/single-value display; a handful
  of values -> pie chart; more -> bar chart; above a second, larger threshold -> line
  chart — see the "Design Guidelines for Data Visualisation" section of the thesis for
  the exact thresholds/citation if needed) as a fixed, non-learned policy. Apply it to
  each test dashboard and compute $R_{Final}$.
- Report all three side by side per dashboard: trained model's greedy top-1 reward,
  random-baseline mean/std, rule-based-baseline reward. The expected/hoped-for result
  is trained > rule-based > random, but report whatever actually comes out — if the
  trained model doesn't beat the simple heuristic, that is itself an important and
  honest finding to have on record, not a failure of this evaluation.

### 4c. Multi-dashboard robustness (real dashboards)

- Once real dashboards are supplied: for each one, independently train a fresh model
  (same architecture, same hyperparameters, same 100-episode budget as the existing
  baseline runs), then run 4a and 4b on it.
- Report, across all dashboards tested (existing 2 fixtures + all supplied real ones):
  whether convergence speed, final reward, and the validity-floor safety margin
  (already flagged as a concern for the large fixture dashboard) are consistent, or
  whether they vary systematically with dashboard size/complexity (number of
  visualisations, mix of chart types, etc.).

### 4d. Wall-clock training time

- Log wall-clock time (not episode count) for each training run in Goal 1/4c, e.g.
  total seconds from training start to the convergence point identified in Goal 3.
  This matters because a real user waits for this in the actual UI — report it even
  if it's just a couple of sentences of context, no dedicated analysis needed.

### 4e. (Stretch, lower priority) Multiple random seeds

- If time allows: re-run training on the small and large fixture dashboards (and any
  real dashboards, if there's time) with 2-3 different random seeds each (the
  existing runs use `torch.manual_seed(42)` only). Report mean and standard deviation
  of the final converged $R_{Final}$ across seeds, to check how sensitive the result
  is to initialization. Skip this if it doesn't fit in the time available — Goals
  4a-4d are the priority.

### 4f. (Stretch, lower priority) Deeper ablation

- If time allows: extend Goal 2's sensitivity check by fully **zeroing out** one
  reward component at a time (not just reweighting it), and observe how much the #1
  recommended action changes per test dashboard. This is a stronger test than
  reweighting alone. Skip this if it doesn't fit in the time available.

**Output format needed:** one CSV or table per sub-goal (4a: dashboard, top-1 action,
reward + component breakdown, consistency fraction; 4b: dashboard, trained-model
reward, random-baseline mean/std, rule-based-baseline reward; 4c: same structure as
4a/4b but with one row per supplied real dashboard; 4d: dashboard, wall-clock
seconds). Keep each sub-goal's output in its own file under `RL_Evaluation/results/`,
following the existing `goal1_*`/`goal2_*`/`goal3_*` naming convention (e.g.
`goal4a_frozen_policy_eval.csv`, `goal4b_baselines.csv`, etc.), and update
`RL_Evaluation/README.md` with the same level of documentation already given to
Goals 1-3 (what was run, key findings, assumptions/provenance notes).

---

## What's explicitly NOT part of this brief

- No changes to the reward function formulas themselves beyond the two specific bug
  fixes in Goal 0 — otherwise, changes are limited to the weights (Goal 2) or to
  zeroing out a component for ablation (Goal 4f), never a broader permanent change to
  the live/deployed model.
- No changes to the action space or state space encoding.
- No new worked example write-up needed for the thesis text itself — the existing
  bar-chart-to-line-chart example is already done and doesn't need touching.
- Goal 4's baselines (random, rule-based) are standalone evaluation code — they should
  not replace or modify the trained model's own decision-making, only run alongside it
  for comparison.
