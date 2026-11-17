# Goal 5 — Hyperparameter Sensitivity (design-review follow-up)

This is a follow-up evaluation, not part of the original Goals 1-4 pass. It
tests three specific, previously **untested** hypotheses flagged by the
thesis's own Phase 2b critical design review as plausible-but-unverified
limitations:

1. `GAMMA = 1.0` (no discounting, `Parameters.py`) over up-to-200-step
   episodes makes credit assignment very diffuse.
2. `LEARNING_RATE = 1e-2` (`Parameters.py`) is high for Adam + policy
   gradients, and combined with `GAMMA = 1.0`, plausibly explains both the
   very fast convergence (episode ~10-28, see Goal 1/3) **and** the fact that
   `reward_final` becomes **bit-for-bit identical across consecutive
   episodes** after convergence — i.e. the policy doesn't just stabilise, it
   collapses to full determinism (visually confirmed in
   `Assets/Treatment Design/RL Model/RL_Training_Convergence.png` in the
   thesis repo, built from the Goal 1 CSVs).
3. No entropy bonus in the loss (a standard technique to sustain
   exploration) is consistent with that collapse.

**Bottom line, stated up front:** the evidence **partially supports** the
hypothesis, but not evenly across its three parts. Learning rate is the
dominant, and the only cleanly beneficial, lever tested. Gamma and the
entropy bonus, tested in isolation *at the current high learning rate*, do
not deliver the hoped-for fix — each instead triggers a **different and
arguably worse** failure mode (near-total loss of the ability to sample a
single structurally valid action, not just "premature but functional"
convergence). Full detail below.

## Step 1 — the policy-collapse metric (defined before running anything)

Per run, two reward-based signals are computed from the per-episode
`reward_final` column (mean step-reward per episode — same column Goal 1
already logs):

- **`collapse_episode`** — the 1-indexed episode at which `reward_final`
  settles into its **longest run of bit-for-bit-identical values that
  extends all the way to the end of the run**, reported only if that run
  covers at least 10% of the episode budget (10 episodes out of 100 here);
  otherwise `"never"`. (Implementation note: this is a "longest constant
  tail" search, not a naive "first adjacent repeat" search — the baseline
  run's tail is *mostly* constant with occasional 1-episode blips, so a
  naive search would badly under- or over-estimate the collapse point. See
  `compute_collapse_episode()` in `goal5_hyperparameter_sensitivity.py`.)
- **`std_last20pct`** — population standard deviation of `reward_final` over
  the last 20% of episodes — a softer, continuous companion signal that
  still shows near-collapse even when `collapse_episode` is `"never"`.
- **`mean_entropy_last20pct`** (bonus signal, entropy-bonus run only) — mean
  summed per-decision-stage categorical entropy (nats), captured by the
  evaluation-only `EntropyAgentNetwork` subclass (`goal5_entropy_network.py`)
  used for the entropy-bonus experiment. Not computed for the stock-network
  runs (LR sweep / gamma sweep / combined configs), per the brief's explicit
  allowance to skip this where it would require invasive instrumentation —
  the two reward-based signals above are used uniformly across all runs.

**Important finding about the metric itself, discovered while interpreting
results (see below): the two reward-based signals are not sufficient on
their own.** Several configurations tested here score well on both
(`collapse_episode = "never"`, small `std_last20pct`) for a reason that has
nothing to do with healthy exploration — the policy has instead lost almost
all ability to sample a single structurally-valid action, so `reward_final`
is being averaged over only 1-2 valid steps per episode and happens to land
in a narrow band by chance. Every existing per-episode log already has
`valid_actions` / `invalid_attempts` columns (same schema Goal 1 introduced
for the 10%-validity-floor check) — those turned out to be **load-bearing**
for correctly interpreting Goal 5, not just a Goal 1/3 footnote. Two more
columns, `min_valid_actions` and `max_invalid_attempts` (across the whole
100-episode run), were added to every Goal 5 summary CSV for this reason.

## Runs, protocol, and files

Small fixture dashboard (6 viz), 100 episodes, seed 42, same protocol as
Goal 1, for every run below. `LEARNING_RATE` / `GAMMA` are varied by patching
`AgentNetworkModule.LEARNING_RATE` / `AgentNetworkModule.GAMMA` (the
already-imported `AgentNetwork.py` module's own attributes) immediately
before/around each run and restoring the originals in a `finally` block —
`Parameters.py` itself is never edited (see
`goal5_hyperparameter_sensitivity.py`'s module docstring for exactly why
this is necessary and how it works). The `lr=1e-2/gamma=1.0` baseline in
every table below is **not** a new run — it's `goal1_training_log_100ep.csv`,
reused and passed through the same `summarize_run()` function for an
apples-to-apples comparison (confirms `first10`/`last10`/`pct_change`
reproduce the published Goal 1 numbers: 0.4077 → 0.4252, +4.3%).

New files:
- `scripts/goal5_hyperparameter_sensitivity.py` — CLI driver: one run per
  invocation, patches LR/GAMMA, calls either the stock `rl_common.train()`
  or the entropy-bonus backend, computes collapse metrics, writes a
  per-episode CSV (Goal-1-style) and appends a summary row.
- `scripts/goal5_entropy_network.py` — evaluation-only `EntropyAgentNetwork`
  subclass (entropy-bonus variant, never wired into shipped `AgentNetwork.py`
  — see its docstring) + a copy of the training loop that also logs mean
  sampling entropy per episode.
- `results/goal5a_learning_rate_sweep.csv`, `results/goal5b_gamma_sweep.csv`,
  `results/goal5c_combined_configs.csv`, `results/goal5d_entropy_bonus.csv` —
  one summary row per config (+ the reused baseline row in each).
- `results/goal5_training_log_lr1e-3.csv`, `..._lr1e-4.csv`,
  `..._gamma0.99.csv`, `..._gamma0.95.csv`,
  `..._combined_lr1e-3_gamma0.99.csv`, `..._combined_lr1e-4_gamma0.95.csv`,
  `..._entropy_default_c0.01.csv` — full per-episode logs, one per run.

**Wall-clock comparability caveat.** The LR sweep and the two combined
configs were originally launched as part of an 8-way parallel batch on this
machine; 4 of those 8 processes (`gamma_0.99`, `gamma_0.95`,
`entropy_c0.01_default`, `entropy_c0.05_default`) stalled for many hours with
zero visible progress (Python fully buffers stdout when redirected to a
file, so nothing was flushed until process exit) and, combined with heavy
CPU contention across 8 concurrent processes, were killed with no usable
partial results and re-run **sequentially, one at a time, with unbuffered
output** (`python -u`). So: `wallclock_seconds` for `lr_1e-3`, `lr_1e-4`, and
both `goal5c` combined runs reflects an 8-way-contended batch; the gamma
sweep and the entropy run reflect uncontended sequential execution. **Treat
wall-clock figures across sections as rough orders of magnitude only, not a
controlled comparison** — the reward/collapse/validity numbers are unaffected
by this (each run's own RNG trajectory is deterministic given its seed and
hyperparameters, independent of what else was running on the machine).

## Results

### 5a — Learning-rate sweep (γ = 1.0 unchanged)

| lr | first10 | last10 | %Δ | final | collapse_ep | std\_last20% | min valid | max invalid | wallclock |
|---|---|---|---|---|---|---|---|---|---|
| 1e-2 (baseline, reused) | 0.4077 | 0.4252 | +4.3% | 0.4252 | **31** | ~0 | 32 | 421 | — |
| 1e-3 | 0.4043 | **0.4606** | **+13.9%** | 0.4428 | **never** | 0.0168 | 21 | 3,968 | 4,359s (~73min, contended) |
| 1e-4 | 0.4116 | 0.3951 | −4.0% | 0.4057 | **never** | 0.0135 | 47 | 172 | 2,902s (~48min, contended) |

Lower learning rate is the one intervention tested here that is **cleanly,
unambiguously beneficial**: both `1e-3` and `1e-4` prevent the bit-identical
collapse within the 100-episode budget, and neither pushes `valid_actions`
anywhere near danger (`min_valid_actions` 21 and 47, both close to or better
than the baseline's own 32-action minimum). `1e-3` also ends with a
materially **higher** last-10-episode mean reward than the collapsed
baseline (+13.9% vs. the baseline's own +4.3%, and 0.4606 vs. 0.4252 in
absolute terms) — i.e. it isn't just "less collapsed," it's a better final
policy. `1e-4` is simply too slow: its last-10 mean is still *below* its
own first-10 mean (−4.0%), meaning it hasn't meaningfully improved on its
initial (mostly random) policy within 100 episodes.

`1e-3` does show a genuine, reproducible **mid-training rough patch**:
`invalid_attempts` climbs into the thousands (peak 3,968 out of the 4,000
hard cap) across roughly episodes 25-55, before the policy recovers to
healthy, varied episode lengths (60-180+ valid actions) for the remainder of
the run. This is a real, if temporary, training-time cost of the lower
learning rate, not a free lunch — flagged here rather than smoothed over.

### 5b — Gamma sweep (lr = 1e-2 unchanged, i.e. the current production default)

| γ | first10 | last10 | %Δ | final | collapse_ep | std\_last20% | min valid | max invalid | wallclock |
|---|---|---|---|---|---|---|---|---|---|
| 1.0 (baseline, reused) | 0.4077 | 0.4252 | +4.3% | 0.4252 | 31 | ~0 | 32 | 421 | — |
| 0.99 | 0.4285 | **0.0851** | **−80.1%** | 0.4254 | never | **0.1954** | **0** | **4,000** | 23,956s (~6.65h, uncontended) |
| 0.95 | 0.4223 | **0.0** | **−100.0%** | **0.0** | **44** | 0.0 | **0** | **4,000** | 14,329s (~3.98h, uncontended) |

**This is the opposite of what the hypothesis predicted, and it's the
single most important finding of Goal 5.** At the unchanged, high production
learning rate, reducing gamma alone does not produce a healthier,
less-prematurely-converged policy — it produces a **catastrophic, different**
failure. For `γ = 0.95`: from episode 44 through the end of the 100-episode
run, the policy samples **zero valid actions in the full 4,000-attempt hard
cap, every single episode** — `reward_final` is permanently 0.0, and by the
letter of the collapse metric this *is* a "collapse" (`collapse_episode =
44`, `std_last20pct = 0.0`), just not the benign kind the design review had
in mind: it's a collapse to total inaction, not to a static-but-functional
policy. For `γ = 0.99`: equally severe but doesn't fully lock in — the run
oscillates for its last ~40 episodes between the same 0-valid/4,000-invalid
dead state and single-valid-action episodes, which is exactly why
`std_last20pct = 0.1954` is the largest value observed anywhere in Goal 5
(next-largest is two orders of magnitude smaller) and why `collapse_episode`
reads `"never"` — a technicality, not a sign of health.

**Conclusion for this section: discounting alone, at the current learning
rate, is not a safe fix and should not be adopted in isolation.**

### 5c — Combined configs (LR lowered + γ lowered together)

| config | first10 | last10 | %Δ | final | collapse_ep | std\_last20% | min valid | max invalid | wallclock |
|---|---|---|---|---|---|---|---|---|---|
| lr=1e-2/γ=1.0 (baseline, reused) | 0.4077 | 0.4252 | +4.3% | 0.4252 | 31 | ~0 | 32 | 421 | — |
| lr=1e-4 / γ=0.95 | 0.4114 | 0.4079 | −0.8% | 0.3928 | never | 0.0160 | 21 | 294 | 2,850s (~47.5min, contended) |
| lr=1e-3 / γ=0.99 | 0.4060 | **0.4656** | **+14.7%** | **0.4658** | never | 0.0181 | 21 | 3,977 | 49,611s (~13.8h — see caveat below) |

This is the comparison that isolates whether a lower learning rate
*protects against* gamma's destructive effect. **It does, for both pairs
tested.** `lr=1e-3/γ=0.99` uses the exact same `γ=0.99` that, alone, produced
0-valid-action episodes for roughly the last 40 episodes of section 5b — yet
combined with `lr=1e-3` it never once drops to 0 valid actions (`min_valid
= 21`) and produces the single best final/last-10 reward of anything tested
in Goal 5 (0.4658 / +14.7%). It does inherit `lr=1e-3`'s mid-training rough
patch (`max_invalid = 3,977`, essentially identical in magnitude and episode
window — ~47-55 — to the `lr=1e-3`-alone run's own 3,968 spike), which is the
real, non-contention-driven reason this run took so long even before
scheduling contention is accounted for (see the sanity-check note below).
`lr=1e-4/γ=0.95` is unremarkable and healthy, similar in magnitude to
`lr=1e-4` alone.

**Conclusion for this section: gamma's harmful effect (5b) appears to be
conditional on the current high learning rate, not intrinsic to discounting
itself.** This is a genuinely useful, non-obvious interaction finding — but
it is based on exactly two (lr, γ) pairs, not a full grid, so "conditional
on LR" should be read as "true for the two points tested," not proven in
general.

**Sanity check on the 13.8h wall-clock (requested explicitly): is this
scheduling contention, or a real training-time effect?** Comparing peak
`invalid_attempts` in any single episode across the relevant runs:

| run | max invalid_attempts | episode | wallclock |
|---|---|---|---|
| baseline (lr=1e-2/γ=1.0) | 421 | 16 | — |
| lr=1e-4 alone | 172 | — | 2,902s |
| lr=1e-4/γ=0.95 combined | 294 | — | 2,850s |
| **lr=1e-3 alone** | **3,968** | **47** | **4,359s (~73min, uncontended-relative-to-this-comparison)** |
| **lr=1e-3/γ=0.99 combined** | **3,977** | **49** | **49,611s (~13.8h)** |

The invalid-attempts spike is essentially identical in size and episode
location whether or not `γ` is also changed — it is an `lr=1e-3` effect, not
a `γ=0.99` effect, and it's real (present, and costly — ~73 minutes just for
that one run — even with `lr=1e-3` tested completely alone). The 13.8h
figure for the combined run is best explained as **that same genuine
per-episode compute cost, further multiplied by the 8-way CPU contention**
this run happened to be caught in before the stuck processes were killed —
both factors are real; neither alone explains the full gap.

**Follow-up: does the combined run's rough patch (episodes ~46-54) show the
*same* pathology as the standalone gamma runs (5b), or a milder one?**
Pulling `valid_actions`/`invalid_attempts` directly for that window:

| episode | valid_actions | invalid_attempts |
|---|---|---|
| 46 | 90 | 3,910 |
| 47 | 60 | 3,940 |
| 48 | 24 | 3,976 |
| 49 | 23 | 3,977 |
| 50 | 45 | 3,955 |
| 51 | 25 | 3,975 |
| 53 | 38 | 3,962 |
| 54 | 25 | 3,975 |

**Milder, not identical.** `invalid_attempts` does climb to essentially the
same near-hard-cap levels seen throughout the standalone `γ=0.99`/`γ=0.95`
bad episodes (~3,900-3,977 vs. the hard cap of 4,000) — the same underlying
stress signature (the mask rejecting almost every sampled action) is clearly
present. But `valid_actions` in this window stays in the 23-90 range, never
once dropping to the 0-2 range that characterises *every* bad episode in the
standalone gamma runs. So this run gets stressed by the same mechanism, but
never actually dies the way gamma-alone does — and by episode 55 it exits
this window for good, settling into a healthy 39-184-valid-action regime for
the rest of the run (5c's summary row also shows `min_valid_actions = 21`
for the *entire* 100-episode run, vs. `0` for both standalone gamma runs).
**Answer to the sanity check: partially confirmed, not fully** — the
combined run visibly touches the same gamma-driven failure signature, but
the lower learning rate keeps it from tipping into the standalone runs' much
more severe, sustained breakdown.

### 5d — Entropy-bonus variant (evaluation-only `EntropyAgentNetwork`)

**Scope note:** the brief called for two entropy coefficients (e.g. 0.01 and
a second value "if time allows") tested at both the current defaults and the
most-promising sweep config. Given the wall-clock already spent recovering
from the parallel-batch incident above, this was cut to **one
run: coefficient 0.01, at the current defaults only** (`lr=1e-2/γ=1.0`).
Coefficient 0.05 and an entropy-bonus run at the `lr=1e-3/γ=0.99` candidate
were both **not** run — flagged here as an explicit gap versus the original
plan, not silently dropped.

| entropy_coef | first10 | last10 | %Δ | final | collapse_ep | std\_last20% | mean entropy (last 20%) | min valid | max invalid | wallclock |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.0 (baseline, reused) | 0.4077 | 0.4252 | +4.3% | 0.4252 | 31 | ~0 | — | 32 | 421 | — |
| 0.01 | 0.4239 | 0.4380 | +3.3% | 0.4427 | **never** | 0.0045 | 0.834 nats | **1** | **3,999** | 18,658s (~5.18h, uncontended) |

**On the surface this looks like a clean win** (never bit-collapses, small
`std_last20pct`, final reward slightly above baseline) — **but it isn't**.
Cross-checking `valid_actions`: from episode ~16 onward, this run almost
never samples more than 1-2 valid actions per 200-step episode — **89 of the
100 episodes fall below the 20-action (10%) validity floor, 87 of the 100
have ≤5 valid actions**, and `invalid_attempts` sits at 3,998-3,999 out of
the 4,000 hard cap for most of the run's second half. `reward_final`'s small
`std_last20pct` is not evidence of a stable, well-exploring policy — it's an
artefact of averaging over just 1-2 samples per episode that happen to land
in a narrow reward band. This is the **same failure mode as the gamma-alone
sweep** (near-total loss of the ability to sample a structurally valid
action), just short of gamma=0.95's fully-dead 0-valid extreme.

Per-decision entropy did decay over training (episode 1 mean ≈3.35 nats
summed across the 3 sampling stages, down to ≈0.3-1.4 nats by the end) —
some exploration decay is expected and not itself a problem — but it
co-occurs with, and plausibly directly causes, the validity collapse: adding
the same entropy bonus uniformly to all three hierarchical stages
(visualisation / action / parameter) doesn't distinguish between "useful
extra randomness among options the mask will accept" and "extra randomness
that the mask immediately zeroes out, forcing a retry" — so it can simply
make the network sample into the mask far more often, without necessarily
making its *valid* choices any more diverse. Whether a much smaller
coefficient (e.g. 0.001) would recover the intended exploration benefit
without this side effect is an **open, explicitly flagged question** — not
tested here, for time.

**Conclusion for this section: the entropy bonus, as implemented and at the
one coefficient tested, is not a safe fix at the current learning rate
either — like gamma-alone, it trades the narrow "bit-identical collapse"
signature for a worse practical failure (near-total loss of valid-action
sampling), not for healthier exploration.**

### 5e — Large-dashboard confirmation

**Skipped entirely**, per revised scope (see "Deviations from the original
plan" below) — not attempted, no file produced.

## Overall verdict on the design-review hypothesis

*"High LR + no discounting + no entropy bonus causes premature policy
collapse"* — **partially supported**, with an important correction to how
evenly the blame should be assigned across the three factors:

- **Learning rate is confirmed as the dominant, and the only cleanly
  beneficial, lever.** Lowering it alone (`1e-3` or `1e-4`) reliably
  delays/prevents the bit-for-bit-identical `reward_final` collapse without
  ever pushing valid-action sampling into danger, and at `1e-3` also
  improves the final converged reward by nearly 14% over the collapsed
  baseline.
- **Discounting (lower γ), tested alone at the current high learning rate,
  does not fix anything — it makes training substantially worse**, driving
  the policy into a qualitatively different and more severe failure (losing
  the ability to sample any structurally valid action at all, up to and
  including complete, permanent breakdown for `γ=0.95`).
- **The entropy bonus, tested alone at the current high learning rate and at
  one coefficient, likewise does not fix anything — it produces a milder
  version of the same validity-collapse failure gamma-reduction causes.**
- **Discounting's harmful effect appears conditional on the high learning
  rate**, not intrinsic to discounting itself: the one combined config
  tested (`lr=1e-3/γ=0.99`) uses the very γ that alone caused total
  breakdown, yet trains cleanly and ends with the best reward of anything in
  this evaluation. Whether the same is true for the entropy bonus (i.e.
  would `entropy_coef=0.01` combined with `lr=1e-3` also stop being harmful)
  is the natural next experiment and was **not** tested here, for time.

**In short: this evaluation does not support "all three factors are equally
culpable, and any one of them could be fixed independently."** It supports a
narrower, more useful claim for the thesis: **the observed premature,
fully-deterministic convergence is best explained by the learning rate
specifically**, and the other two design-review concerns (no discounting, no
entropy bonus), while reasonable things to have flagged as untested
limitations, turn out — at least at the coefficients/values tested here, in
isolation, at the current learning rate — to be net **negative** changes,
not net-positive ones, and should not be adopted as standalone fixes without
also lowering the learning rate.

## Deviations from the original plan (explicit, not smoothed over)

- **Entropy-bonus coefficient sweep cut from 2 (+ a candidate-config re-run)
  down to 1.** Only `entropy_coef=0.01` at production defaults was run;
  `0.05`, and any entropy-bonus run at the `lr=1e-3/γ=0.99` candidate
  config, were not attempted. Cut for time, given the wall-clock already
  spent on the parallel-batch incident and its sequential recovery (see
  below).
- **Large-dashboard confirmation (section 6 of the original brief) skipped
  entirely.** Not attempted, no file produced. The core hypothesis is
  reasonably well-tested on the small dashboard alone between the LR sweep,
  gamma sweep, and combined configs; a second dashboard was cut as a
  nice-to-have given time spent elsewhere.
- **Operational incident:** the first attempt at this evaluation launched
  all 8 small-dashboard wave-1 configs (LR sweep ×2, gamma sweep ×2,
  combined ×2, entropy-at-defaults ×2) simultaneously as background
  processes with default (buffered) stdout redirection. Buffered output
  meant 4 of the 8 (both gamma runs, both entropy runs) showed zero visible
  progress in their log files for close to 23 hours of real elapsed time,
  making it impossible to distinguish "slow" from "hung" from the outside;
  combined with heavy 8-way CPU contention (one of the other 4 runs,
  `combined_lr1e-3_gamma0.99`, took 13.8h wall-clock for what turned out to
  be a ~73-minute-uncontended computation, see the 5c sanity check above),
  those 4 processes were killed with no usable partial results and re-run
  sequentially, one at a time, with unbuffered (`python -u`) output. The LR
  sweep and combined-config results themselves are unaffected (each run's
  outcome is deterministic given its own seed/hyperparameters, independent
  of what else was running) — only the `wallclock_seconds` figures across
  sections are not on a level footing, as noted above.

## Assumptions / provenance notes (Goal-5-specific, in addition to the ones
in `README.md`)

- All Goal 5 training runs use `torch.manual_seed(42)`, same as Goals 1-4.
- The `lr=1e-2/γ=1.0` baseline row in every Goal 5 summary CSV is
  `goal1_training_log_100ep.csv` reused (not re-run), passed through this
  evaluation's own `summarize_run()` for exact metric comparability; its
  `wallclock_seconds` field is left blank since it predates this evaluation
  and was never timed under the same conditions.
- Every Goal 5 run is on the `small` (6-visualisation) synthetic fixture
  only — no real-dashboard or `large`-fixture runs were performed for Goal 5.
- The entropy-bonus backend (`goal5_entropy_network.py`) is confirmed
  numerically equivalent to the stock network for identical inputs before
  any gradient update: episode 1's `reward_final` is bit-identical between
  the entropy-variant smoke test and the stock-network smoke test at the
  same seed, confirming that computing `Categorical(...).entropy()`
  alongside `.sample()` does not perturb the RNG draw sequence.
