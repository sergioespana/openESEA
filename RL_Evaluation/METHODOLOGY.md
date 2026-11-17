# RL Model — Evaluation Setup & Architecture

This document describes the model, environment, and evaluation methodology
behind everything in `RL_Evaluation/results/`. It's split into two parts:

- **Part A — Thesis-insertable summary.** A condensed version written at
  thesis register, short enough to drop into a Methodology/Evaluation Setup
  section with light editing.
- **Part B — Full technical reference.** Every concrete number, formula,
  and design decision, for anyone (including future-you) who needs to
  reproduce, extend, or defend a specific choice.

Nothing in this evaluation changed the model's architecture, hyperparameters,
reward formulas, action/state space, or (outside Goals 2/4f, clearly marked)
the reward weights. All of it is read-only instrumentation and evaluation
code layered on top of the existing `core/DashboardRLModel/` package.

**Split with the other two docs in this directory:** this file is the
architecture/methodology reference and doesn't change when results are
re-run. `README.md` is the results index — what was run, current numbers,
data-quality/staleness notes, per-goal findings. `THESIS_SUMMARY.md` is a
tight, numbers-first summary meant to be lifted near-verbatim into thesis
text. If you're looking for current findings/numbers rather than how the
system works, start with those two instead.

---

## Part A — Thesis-insertable summary

### Model and training setup

The dashboard-editing agent is a policy-gradient actor-critic network
(PyTorch). Each dashboard is encoded as a fixed-length vector: every
visualisation contributes a one-hot visualisation type (11 possible types),
three boolean flags (item-limit enabled, item-limit "large", "many data
items"), and two normalised scalars (item limit, data-item count), for 17
features per visualisation; the vector is zero-padded up to a
visualisation-capacity slot count (`max(20, round(1.2 × num_visualisations))`)
so dashboards of different sizes share one input width per training run. The
network makes one edit decision per time step through a hierarchical
LSTM-embedded decision head: it selects (1) which visualisation to edit, (2)
which of three action types to apply — change visualisation type, add an
item limit, or remove an item limit — and (3) that action's parameter (the
target visualisation type, or the item-limit value), with each stage's
output masked to only structurally valid choices before sampling and each
stage conditioned on the previous stages' one-hot-encoded choices. A shared
critic head estimates the value of the resulting state. Training uses
full-episode Monte Carlo returns (undiscounted, γ = 1), advantage-weighted
policy gradients, and a smooth-L1 critic loss, optimised jointly with Adam
(learning rate 0.01). An episode runs until either a hard cap of 200 time
steps is reached with more than a 10% valid-action rate, or indefinitely
retries on masked-out (invalid) samples otherwise. The standard training
budget is 100 episodes per dashboard; the model is trained independently per
dashboard rather than as one policy expected to generalise across dashboards,
consistent with how the system is actually used (a fresh model per
edited dashboard, in the live product).

The reward is a weighted combination of four components, each computed
per-visualisation and normalised to roughly [0, 1]: **Decluttering**
(rewards enabling and tightening item limits), **Chart Variety** (rewards a
moderate number of distinct chart types across the dashboard, penalising
both too little and too much variety), **Data Completeness** (rewards
*not* limiting item counts, in tension with Decluttering), and **Appropriate
Visualisation Types** (rewards matching a chart type to its data-item count
against literature-derived thresholds, e.g. pie charts for 3–6 categories,
bar charts for 7–15, line charts beyond that). The weighted sum is divided
by the sum of the weights to keep the combined reward in the same [0, 1]
range. Current production weights: Decluttering 1.0, Appropriate
Visualisation Types 0.8, Chart Variety 0.5, Data Completeness 0.2.

### Evaluation methodology

Four evaluation goals were run. **(1) Training-convergence logging**:
per-episode mean reward (combined and per-component) plus valid/invalid
sampled-action counts, across the standard 100-episode budget, a 500-episode
extension, and dashboards of two different sizes. **(2) Reward-weight
sensitivity**: recomputing the (unmodified) reward formulas for every
structurally valid candidate action from a fixed dashboard state under four
weight configurations, to check whether the top-ranked recommendation is
robust to the (heuristically chosen) weights. **(3) Training-budget
adequacy**: comparing mean reward across the first vs. last 10% of episodes
and checking for a plateau, to give an evidence-based answer on whether 100
episodes is enough. **(4) Frozen-policy evaluation and baselines**: after
training, the network is run in its existing deterministic top-K inference
mode (no further learning, no random sampling — it enumerates and ranks by
probability rather than sampling) and compared against two non-learned
baselines on the same dashboard: a uniform-random policy (100 samples,
respecting the same action masking) and a simple literature-threshold rule
(single value → single-value card; a handful of values → pie chart; more →
bar chart; many/time-series-scale → line chart).

### Dashboards used

Two synthetic dashboards were constructed as reconstructions (the exact
dashboard from the thesis's original training run was not recoverable from
the repository or any log): a 6-visualisation "small" dashboard and a
15-visualisation "large" dashboard spanning every supported chart type. To
ground the evaluation in realistic compositions, 16 additional dashboards
were pulled from the project's local development database — seeded
specifications modelled after real ESG-reporting tools (Accuvio, Apambu,
ArcherIRM, Cority, Deloitte, Diligent, Envizi, ESGBook, Measurabl, Navex,
RIMM) plus three generic examples, each populated with realistic synthetic
organisational data (5 organisations × 4 reporting years). Their per-chart
data-item counts were derived directly from the same formula the production
frontend uses when building this exact model input
(`Data Items = number of data rows × number of value fields per chart`),
not estimated. Of these 16, a diverse subset of 6 (spanning 6–14
visualisations and different chart-type compositions) was independently
trained and evaluated end-to-end, given the compute cost of training one
model per dashboard; all 16 converted dashboards remain available for future
extension of this evaluation.

---

## Part B — Full technical reference

### B.1 Network architecture

`core/DashboardRLModel/AgentNetwork/AgentNetwork.py`:

- `FeedForwardLayer`: an `LSTMEmbeddingLayer` (single-step LSTM used purely
  as a learned embedding, not a real sequence model — input is unsqueezed to
  a length-1 "sequence") → `Linear` (ReLU) → `Linear` → softmax. Used for
  the visualisation-selection head, the action-type head, and each action's
  parameter head(s).
- `CriticLayer`: same embedding pattern, but outputs a single scalar value
  estimate instead of a softmax distribution.
- Decision order per time step: **visualisation** (softmax over
  `visualisation_capacity` slots, masked to real visualisations) →
  **action type** (softmax over 3 actions, masked by
  `get_action_mask`, conditioned on the one-hot visualisation choice) →
  **action parameter(s)** (softmax over the action's parameter space,
  masked by `get_parameter_mask`, conditioned on all prior one-hot choices)
  → **critic value** (conditioned on everything sampled so far).
- Sampling: `forward_sample` uses `torch.distributions.Categorical(...).sample()`
  at each stage (this is what makes *training* stochastic/exploratory).
  `forward_predict` (used for the live top-10 "best actions" UI feature, and
  reused here for the frozen/greedy evaluation) instead *enumerates* every
  category via `collect_categorical` and sorts by running probability
  product at each stage, keeping only the top-`K` branches — no
  `Categorical.sample()` call anywhere in that path, so it is fully
  deterministic given fixed weights and a fixed input state.
- Masking (`DashboardEnvironment.get_visualisation_mask` /
  `get_action_mask` / `get_parameter_mask`): zeroes out probability mass for
  structurally invalid choices (e.g. `RemoveItemLimit` on a visualisation
  that has no limit enabled; changing a visualisation to its own current
  type; an item-limit value below 2 or above the visualisation's data-item
  count) before every categorical draw, in both sampling and prediction
  paths.

### B.2 State encoding

`core/DashboardRLModel/Dashboard/Encoding.py`, per visualisation (17
features): one-hot visualisation type (11 dims, `NUM_VISUALISATION_TYPES`),
`itemLimitEnabled` (bool), `itemLimitLarge` (bool, true if the limit ≥
`MAX_ITEM_LIMIT` = 100), `itemLimit` (integer, normalised by 100),
`manyDataItems` (bool, true if data items ≥ `MAX_DATA_ITEMS` = 250),
`dataItems` (integer, normalised by 250), `displayArea` (normalised by the
dashboard's total display area). The full state vector is
`17 × visualisation_capacity`, zero-padded beyond the dashboard's actual
visualisation count; `visualisation_capacity = max(20, round(1.2 ×
num_visualisations))` (`DashboardRLModel.__init__`). Network hidden size is
set equal to the input size (`num_hidden = num_inputs`).

### B.3 Action space

`core/DashboardRLModel/Dashboard/Actions/`: 3 action types —
`ChangeVisualisationType` (parameter: 1 of 11 target types),
`AddItemLimit` (parameter: an integer limit, 0–99), `RemoveItemLimit` (no
parameters). Every action also carries a `visualisationIndex`, chosen from
the same categorical head as the rest of the decision.

### B.4 Reward function

`core/DashboardRLModel/Dashboard/Environment.py`. All four components are
computed per-visualisation and averaged over the dashboard's visualisation
count, so each is naturally in roughly [0, 1]:

- **Decluttering** — `0.5 × itemLimitEnabled + 0.5 × max(0, (dataItems −
  itemLimit) / dataItems)`. Rewards both turning a limit on and setting it
  meaningfully below the current data-item count.
- **Data Completeness** — `1 − itemLimitEnabled`. Directly opposes
  Decluttering — the two components are in intentional tension.
- **Chart Variety** — a lookup on the *count of distinct visualisation
  types* present on the dashboard: 0.8 (1 type), 0.9 (2), 1.0 (3 or 4), then
  decreasing (0.8, 0.6, 0.3, 0.2, 0.1, 0.05 for 5–9+ types) — a moderate
  amount of variety is rewarded, both too little and too much is penalised.
- **Appropriate Visualisation Types** — per-type literature-derived
  thresholds on data-item count: `SINGLE` → 1 (reward 1 only if exactly 1
  item); `PROGRESS_BAR`/`RADIAL_PROGRESS_BAR` → 1 or 2 items; `FRACTIONAL` →
  exactly 2; `PIE` → 3–6 (peaking at 3, comment cites "Literature: 4, 5, 6");
  `BAR` → 3–15 (best at 7–15, comment cites "Literature: 10, 12, 15");
  `LINE` → 3–6 (partial credit), 7–15 (0.9), ≥16 (1.0, best for genuinely
  long series). `GROUPED_BAR`, `STACKED_BAR`, `TABLE`, and
  `MULTI_SERIES_LINE` have **no case in this function and always score 0**
  — worth flagging as an existing gap in the reward design (not something
  this evaluation changed), and consistent with those types never appearing
  in any of the 16 real dashboards pulled from the database.

Final combined reward: `R_Final = Σ(weight_f × R_f) / Σ(weight_f)`,
current production weights `{Decluttering: 1.0, Appropriate Visualisation
Types: 0.8, Chart Variety: 0.5, Data Completeness: 0.2}` (sum 2.5).

**Bug fixes applied during this evaluation (see `RL_Evaluation_Brief.md`
Goal 0).** Two genuine implementation bugs were found and fixed in
`Environment.py`, distinct from any weight-choice question (Goal 2):

1. **Weights were applied twice.** `collect_state_rewards()` multiplied
   each component by its weight, and `reward()` multiplied by the weight
   *again* when summing — net effect `R_Final = Σ(weight² × R_f) /
   Σ(weight)` instead of the intended `Σ(weight × R_f) / Σ(weight)`, which
   over-amplified higher-weighted components relative to lower-weighted
   ones beyond what the stated weights imply. Fixed by applying the weight
   exactly once (removed the multiplication in `collect_state_rewards()`).
   This affected *training itself* (`reward()` is what `env.step()` calls),
   not just post-hoc reward recomputation.
2. **Decluttering's excess-item term had a divide-by-zero / backwards edge
   case.** The formula is `0.5 × itemLimitEnabled + 0.5 × excess_term`,
   where `excess_term = (dataItems − itemLimit) / dataItems` when
   `dataItems > itemLimit`, else 0. With no item limit set (`itemLimit =
   0`, the default/most common state — including every visualisation's
   initial state), this evaluated to `(dataItems − 0) / dataItems = 1`,
   i.e. "no limit at all" was scored as near-maximum decluttering. Fixed by
   guarding `itemLimit ≤ 0 → 0`. (We also tried the brief's literal
   suggestion of dividing by `itemLimit` instead of `dataItems` — that
   makes the term *unbounded* and grows fastest exactly when the agent
   picks the most aggressive, most-desirable item limit, which breaks the
   [0,1]-per-component design used everywhere else in the reward and is
   very likely a transcription artifact rather than the intended formula.
   Reverted to the `dataItems` divisor, keeping only the zero-guard.)

Every reward component is confirmed to stay in `[0, 1]` after both fixes
(spot-checked numerically). All Goal 1-4 results were re-run against the
corrected reward; pre-fix results are preserved under
`RL_Evaluation/results/pre_bugfix/` for an explicit before/after comparison
(see README "Key findings").

### B.5 Training loop

`core/DashboardRLModel/DashboardRLModel.py::run_episode` /
`AgentNetwork.update_network_gradients`. Per episode: reset to the
dashboard's initial state; repeatedly sample an action (masked-invalid
samples don't consume a "valid" count but do consume a time step and are
retried); stop once ≥ 200 time steps have elapsed **and** more than 20 valid
actions have been taken (the ">10% success rate" criterion), i.e. the loop
can run past 200 steps if the valid-action rate is below 10%. Returns are
computed via the standard REINFORCE-with-baseline recipe: discounted
(γ = `GAMMA` = **1.0**, i.e. effectively undiscounted) cumulative return per
time step, normalised to zero mean / unit variance across the episode;
advantage = return − critic's value estimate (detached); policy loss =
`−log π(a) × advantage` per step; value loss = smooth-L1 between the
critic's estimate and the return; total loss = sum of both, backpropagated
once per episode with Adam (`LEARNING_RATE` = **0.01**). There is also a
(separate, optional) user-feedback pathway (`saved_user_actions` /
`user_rewards`) for incorporating explicit +1/−1 human feedback into the
same gradient step — unused in this evaluation (no user feedback was
simulated).

### B.6 The evaluation scripts (`RL_Evaluation/scripts/`)

- `rl_common.py` — shared, reused across Goals 1–4: environment
  construction, reward-component computation, candidate-action enumeration
  (respecting the live masks), the instrumented training loop (a faithful
  copy of `run_episode` with per-episode logging added, returning the live
  trained model rather than discarding it), frozen/greedy top-K evaluation
  (calls `forward_predict` directly), and the two Goal 4b baselines.
- `goal1_training_run.py` / `goal3_training_budget_summary.py` — Goal 1/3
  scripts (see the "Goals 1-3" section of `README.md` for what they produced
  before Goal 4 existed).
- `goal2_weight_sensitivity.py` — Goal 2's reweighting sensitivity check.
- `dashboard_fixture.py` / `export_dashboard_jsons.py` — the two synthetic
  dashboards, as Python constants and as exported JSON.
- `db_dashboard_loader.py` — connects to the local Postgres dev database
  (`esea_db`, via Django's ORM with `DJANGO_SETTINGS_MODULE=django_backend.settings`)
  and converts all 16 seeded "real" dashboards into the same JSON input
  format (see B.7 below for the conversion rule).
- `goal4_pipeline.py` — trains a fresh model per dashboard (same 100-episode
  protocol as Goal 1) and runs 4a (frozen greedy eval + determinism check),
  4b (baselines), 4c (per-dashboard convergence/robustness stats), and 4d
  (wall-clock timing), writing one row per dashboard into each of
  `goal4a_frozen_policy_eval.csv`, `goal4a_determinism_check.csv`,
  `goal4b_baselines.csv`, `goal4c_multi_dashboard_robustness.csv`,
  `goal4d_wallclock_timing.csv`.
- `goal4f_zero_out_ablation.py` — Goal 4f's stretch ablation (zeroing, not
  just reweighting, one reward component at a time).

### B.7 Real-dashboard conversion (database → RL model input)

Source: `openESEA_interpreter/backend/core/management/commands/seed_dummy_data.py`
seeds 5 organisations (Verdant Corp, Nexocraft GmbH, Circle Goods ApS, Solis
Group SA, BioMaterials Sp. z o.o.), each with exactly one finished survey
response per indicator per year across 4 years (2022–2025), and 16 dashboard
specifications (`Dashboard.specification`, a JSONField) modelled after real
ESG-reporting tools. Verified via direct query against the local `esea_db`
Postgres database (confirmed running as the native Windows service
`postgresql-x64-18`) that every seeded organisation has exactly 4 years of
data for every indicator (`QuestionResponse` count of 20 per indicator = 5
orgs × 4 years).

The conversion (`db_dashboard_loader.py`) walks each specification's
`Overviews → BodySection → Containers → Visualisations → DataDisplay →
DataConfiguration` and reproduces, field-for-field, the exact computation
`OrganisationDashboard.vue` (lines ~244–260) uses when building this same
RL-model payload live in the product:

```
amountOfValueFields = count of DataConfiguration keys containing "Value Field"
numberOfDataPoints   = 4  (years reported) if a "Category Field" is present
                       1  (a single current-value snapshot) otherwise
Data Items           = numberOfDataPoints × amountOfValueFields
Item Limit Enabled   = Category Limit > 0   (all 16 seeded dashboards: 0 everywhere)
Item Limit           = Category Limit
```

This yields, e.g., `Data Items = 1` for a Single Value Display (1 value
field, no category), `Data Items = 2` for a Radial/Progress Bar (current +
target value fields, no category), and `Data Items = 4` for a Bar/Pie/Line
chart (1 value field × 4 years). One dashboard, **"ESEA Standard"** (the
platform's own default dashboard rather than a tool-inspired one), was
excluded — its `DataConfiguration` uses a structurally different schema
(plural `Indicators`/`Values` lists rather than a single indicator + a
"Category Field") that the conversion rule above doesn't cover.

All 16 tool-inspired dashboards use only 6 of the model's 11 supported
visualisation types (Single Value Display, Radial Progress Bar, Progress
Bar, Bar Chart, Pie Chart, Line Chart) — `Fractional Value Display`,
`Table`, `Grouped Bar Chart`, `Stacked Bar Chart`, and `Multi-Series Line
Chart` never appear in any real seeded dashboard, only in the synthetic
"large" fixture.

### B.8 Dashboards actually trained and evaluated

| name | source | # visualisations | types used |
|---|---|---|---|
| `small` | synthetic fixture | 6 | Bar, Pie, Line, Single, Progress, Table |
| `large` | synthetic fixture | 15 | all 11 supported types |
| `real_energy_climate` | DB (generic) | 7 | Single, Radial, Progress |
| `real_cority_quality_monitor` | DB (Cority-inspired) | 6 | Radial, Bar, Line, Single |
| `real_accuvio_resource_overview` | DB (Accuvio-inspired) | 7 | Bar, Pie, Progress, Radial |
| `real_esgbook_score_analytics` | DB (ESGBook-inspired) | 6 | Radial, Line only |
| `real_rimm_topic_scorecard` | DB (RIMM-inspired) | 13 | Progress-heavy (8/13), Radial, Single |
| `real_measurabl_data_cards` | DB (Measurabl-inspired) | 14 | Single, Bar, Radial, Progress |

The other 10 real dashboards converted from the database (Social Workforce,
Sustainability Scorecard, ArcherIRM, Cority Compliance Tracker, Deloitte
Emissions Executive, Diligent GHG Analytics, Envizi Utility Performance,
Envizi Net Zero Pathway, Navex ESG Analytics, and one already excluded above)
are present as JSON in `RL_Evaluation/dashboards/` for future extension but
were not independently trained/evaluated in this pass, given the ~20-45
minute training cost per dashboard.

### B.9 Reproducibility

All training runs use `torch.manual_seed(42)` (the network's weight
initialisation and every exploratory sample during training are therefore
deterministic given the code as of this evaluation). `goal4_pipeline.py`
retrains `small` and `large` from scratch with the same seed as
`goal1_training_run.py` used, and logs the two runs' final-episode reward
side by side as an explicit reproducibility check.
