"""
Goal 5 - Hyperparameter Sensitivity (design-review follow-up).

The Phase 2b critical design review flagged, as an UNTESTED hypothesis, that
GAMMA=1.0 (no discounting) + LEARNING_RATE=1e-2 (high, for Adam + policy
gradients) + no entropy bonus plausibly causes the training policy to
collapse to full determinism prematurely: per-episode reward_final becomes
bit-for-bit identical across consecutive episodes from some episode onward
(already visually confirmed for the Goal 1 baseline runs). This script runs
one training configuration per invocation (small or large fixture dashboard,
a given learning rate / gamma / entropy-bonus coefficient) using the exact
same 100-episode / seed-42 protocol as Goal 1, and reports:

  1. `collapse_episode` - the episode from which reward_final first settles
     into a run of >=10% of the episode budget's worth of bit-for-bit
     identical values that persists through the end of the run (the
     "longest constant tail" the run ever reaches), or "never" if no such
     run exists within the episode budget.
  2. `std_last20pct` - the (population) standard deviation of reward_final
     over the last 20% of episodes - a softer, continuous companion metric
     that still shows near-collapse (frequent tiny oscillations that never
     quite lock down, as seen on the `large` dashboard baseline) even when
     `collapse_episode` is "never" or arrives late.

plus the same first-10%/last-10% mean and %-change convergence stats Goal 3
used, for direct comparability with the existing goal1/goal3 baselines
(`goal1_training_log_100ep.csv` = LEARNING_RATE=1e-2, GAMMA=1.0 baseline for
`small`; `goal1_training_log_100ep_large_dashboard.csv` = the same baseline
for `large` - both reused as-is, NOT re-run, per the brief).

HOW HYPERPARAMETERS ARE VARIED (read this before changing the script):
`LEARNING_RATE` / `GAMMA` live in
`core/DashboardRLModel/AgentNetwork/Parameters.py` and are imported into
`AgentNetwork.py`'s own module namespace via
`from .Parameters import GAMMA, LEARNING_RATE`. Patching Parameters.py itself
would have no effect on the already-imported AgentNetwork module, and this
script never edits Parameters.py. Instead:
  - `LEARNING_RATE` is only read once, at `AgentNetwork.__init__` time
    (`optim.Adam(self.parameters(), lr=LEARNING_RATE)`), as a lookup of the
    bare name `LEARNING_RATE` in AgentNetwork.py's own module globals. So
    setting `AgentNetworkModule.LEARNING_RATE = <value>` BEFORE constructing
    a model (via rl_common.train() or goal5_entropy_network.train_entropy())
    changes what that constructor sees.
  - `GAMMA` is read from the same module globals EVERY TIME
    `update_network_gradients` runs (once per episode), so patching
    `AgentNetworkModule.GAMMA` continues to take effect for the whole run.
  - Both are restored to their original values in a `finally` block after
    every run, so configurations never leak into each other, and
    Parameters.py's committed values are never touched.

Two training backends are used, matching the brief's scope restrictions:
  - LR sweep / gamma sweep / combined configs: the UNMODIFIED, shipped
    AgentNetwork/DashboardRLModel, via rl_common.train() (already used
    unchanged by Goals 1 and 4).
  - Entropy-bonus variant: goal5_entropy_network.train_entropy(), an
    evaluation-only subclass (see that file's docstring) - never wired into
    the shipped AgentNetwork.py.

Usage:
    python goal5_hyperparameter_sensitivity.py --run-label lr_1e-3 \
        --dashboard small --lr 1e-3 --gamma 1.0 \
        --log-output ../results/goal5_training_log_lr1e-3.csv \
        --summary-csv ../results/goal5a_learning_rate_sweep.csv

    python goal5_hyperparameter_sensitivity.py --run-label entropy_c0.01_default \
        --dashboard small --lr 1e-2 --gamma 1.0 --entropy-coef 0.01 \
        --log-output ../results/goal5_training_log_entropy_default_c0.01.csv \
        --summary-csv ../results/goal5d_entropy_bonus.csv
"""
import argparse
import csv
import os
import sys
import time

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import torch  # noqa: E402
import core.DashboardRLModel.AgentNetwork.AgentNetwork as AgentNetworkModule  # noqa: E402

import rl_common  # noqa: E402
import goal5_entropy_network as entropy_net  # noqa: E402
from dashboard_fixture import TRAINING_DASHBOARD, TRAINING_DASHBOARD_LARGE  # noqa: E402

# This script is designed to be launched many times concurrently (one OS
# process per hyperparameter config, see the sweep-runner notes in
# RL_Evaluation/README.md's Goal 5 section) on a multi-core machine. Each
# individual model here is tiny, so there is no benefit to multi-threaded
# BLAS/OMP within a single run, and every extra thread just adds contention
# against the other concurrently-running configs. Pin each process to one
# thread; parallelism comes from running many processes side by side instead.
torch.set_num_threads(1)

DASHBOARDS = {
    'small': TRAINING_DASHBOARD,
    'large': TRAINING_DASHBOARD_LARGE,
}


# --------------------------------------------------------------------------
# Step 1: the policy-collapse metric (see module docstring for definitions)
# --------------------------------------------------------------------------

def compute_collapse_episode(reward_finals, min_run_length=None):
    """Longest run of bit-for-bit identical reward_final values that extends
    all the way to the end of the run. Returns the 1-indexed episode the run
    starts at, or None if that run is shorter than `min_run_length` (default:
    max(10, 10% of episodes)) - i.e. "no sustained collapse detected"."""
    n = len(reward_finals)
    if min_run_length is None:
        min_run_length = max(10, round(0.1 * n))
    if n == 0:
        return None
    last_val = reward_finals[-1]
    i = n - 1
    while i > 0 and reward_finals[i - 1] == last_val:
        i -= 1
    run_length = n - i
    if run_length >= min_run_length:
        return i + 1  # 1-indexed episode number
    return None


def std_last_k_percent(reward_finals, fraction=0.2):
    n = len(reward_finals)
    k = max(1, round(fraction * n))
    tail = reward_finals[-k:]
    mean_tail = sum(tail) / len(tail)
    variance = sum((v - mean_tail) ** 2 for v in tail) / len(tail)
    return variance ** 0.5


def summarize_run(rows):
    reward_finals = [r['reward_final'] for r in rows]
    n = len(reward_finals)
    k10 = max(1, round(0.1 * n))
    first10_mean = sum(reward_finals[:k10]) / k10
    last10_mean = sum(reward_finals[-k10:]) / k10
    pct_change = ((last10_mean - first10_mean) / first10_mean * 100) if first10_mean != 0 else float('nan')
    collapse_episode = compute_collapse_episode(reward_finals)
    std_last20 = std_last_k_percent(reward_finals, 0.2)

    mean_entropy_last20 = ''
    if 'mean_entropy' in rows[0]:
        k20 = max(1, round(0.2 * n))
        tail_entropies = [r['mean_entropy'] for r in rows[-k20:] if r['mean_entropy'] == r['mean_entropy']]  # drop NaN
        if tail_entropies:
            mean_entropy_last20 = sum(tail_entropies) / len(tail_entropies)

    return {
        'first10_mean': first10_mean,
        'last10_mean': last10_mean,
        'pct_change': pct_change,
        'final_reward': reward_finals[-1],
        'collapse_episode': collapse_episode if collapse_episode is not None else 'never',
        'std_last20pct': std_last20,
        'mean_entropy_last20pct': mean_entropy_last20,
    }


# --------------------------------------------------------------------------
# CSV I/O
# --------------------------------------------------------------------------

def write_episode_csv(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print('Wrote {} rows to {}'.format(len(rows), path))


def append_summary_row(path, row):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file_exists = os.path.exists(path)
    with open(path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    print('Appended summary row to {}'.format(path))


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dashboard', choices=list(DASHBOARDS.keys()), default='small')
    parser.add_argument('--episodes', type=int, default=100)
    parser.add_argument('--time-steps', type=int, default=200)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--lr', type=float, default=1e-2)
    parser.add_argument('--gamma', type=float, default=1.0)
    parser.add_argument('--entropy-coef', type=float, default=0.0,
                         help='0.0 (default) uses the unmodified shipped AgentNetwork. '
                              '>0 uses the evaluation-only EntropyAgentNetwork variant.')
    parser.add_argument('--run-label', required=True, help='Identifier for this config in the summary CSV.')
    parser.add_argument('--log-output', required=True, help='Per-episode CSV path (like goal1_training_log_*.csv).')
    parser.add_argument('--summary-csv', required=True, help='Summary CSV to append this run\'s row to.')
    args = parser.parse_args()

    dashboard_dict = DASHBOARDS[args.dashboard]

    original_lr = AgentNetworkModule.LEARNING_RATE
    original_gamma = AgentNetworkModule.GAMMA

    print('Starting run "{}": dashboard={} episodes={} seed={} lr={} gamma={} entropy_coef={}'.format(
        args.run_label, args.dashboard, args.episodes, args.seed, args.lr, args.gamma, args.entropy_coef))

    start = time.time()
    try:
        AgentNetworkModule.LEARNING_RATE = args.lr
        AgentNetworkModule.GAMMA = args.gamma
        if args.entropy_coef > 0:
            model, rows, elapsed = entropy_net.train_entropy(
                dashboard_dict, args.episodes, args.entropy_coef,
                num_time_steps=args.time_steps, seed=args.seed)
        else:
            model, rows, elapsed = rl_common.train(
                dashboard_dict, args.episodes, num_time_steps=args.time_steps, seed=args.seed)
    finally:
        AgentNetworkModule.LEARNING_RATE = original_lr
        AgentNetworkModule.GAMMA = original_gamma
    wallclock_seconds = time.time() - start

    write_episode_csv(rows, args.log_output)

    stats = summarize_run(rows)
    summary_row = {
        'run_label': args.run_label,
        'dashboard': args.dashboard,
        'episodes': args.episodes,
        'seed': args.seed,
        'learning_rate': args.lr,
        'gamma': args.gamma,
        'entropy_coef': args.entropy_coef,
        'first10_mean': stats['first10_mean'],
        'last10_mean': stats['last10_mean'],
        'pct_change': stats['pct_change'],
        'final_reward': stats['final_reward'],
        'collapse_episode': stats['collapse_episode'],
        'std_last20pct': stats['std_last20pct'],
        'mean_entropy_last20pct': stats['mean_entropy_last20pct'],
        'wallclock_seconds': wallclock_seconds,
        'log_file': os.path.basename(args.log_output),
    }
    append_summary_row(args.summary_csv, summary_row)

    print('DONE run="{}" collapse_episode={} std_last20pct={:.8f} final_reward={:.6f} wallclock={:.1f}s'.format(
        args.run_label, stats['collapse_episode'], stats['std_last20pct'], stats['final_reward'], wallclock_seconds))


if __name__ == '__main__':
    main()
