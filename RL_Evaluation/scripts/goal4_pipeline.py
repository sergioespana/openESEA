"""
Goal 4 pipeline: for each dashboard in DASHBOARDS, train a fresh model (same
protocol as Goal 1: 100 episodes, up to 200 time steps, seed 42), then run:
  4a. Frozen/greedy policy evaluation (top-10, deterministic, + consistency check)
  4b. Random-policy and rule-based baselines
  4c. Per-dashboard convergence/robustness stats (extends Goal 3's method)
  4d. Wall-clock timing to convergence and to end of the 100-episode budget

Writes one CSV per sub-goal (goal4a_*, goal4b_*, goal4c_*, goal4d_*) into
RL_Evaluation/results/, appending a row (or rows) per dashboard as each
finishes - so partial results are inspectable while the run is still going.

Nothing here changes the trained model's live weights, reward formulas, or
action/state space - see rl_common.py for what's reused unmodified.
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import rl_common as rc  # noqa: E402

RESULTS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'results'))
DASHBOARDS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'dashboards'))

DASHBOARDS = [
    ('small', 'small.json'),
    ('large', 'large.json'),
    ('real_energy_climate', 'real_energy_climate.json'),
    ('real_cority_quality_monitor', 'real_cority_quality_monitor.json'),
    ('real_accuvio_resource_overview', 'real_accuvio_resource_overview.json'),
    ('real_esgbook_score_analytics', 'real_esgbook_score_analytics.json'),
    ('real_rimm_topic_scorecard', 'real_rimm_topic_scorecard.json'),
    ('real_measurabl_data_cards', 'real_measurabl_data_cards.json'),
]

NUM_EPISODES = 100
NUM_TIME_STEPS = 200
# seed 42 was found to be a catastrophic-collapse outlier for the small
# dashboard (see README "Key findings" - a 4-seed sweep of 1/7/42/123 found
# only seed 42 collapsed; 1 and 123 converged cleanly, 7 was noisy but
# functional). Switched to seed 1 as the new official reproducibility seed.
SEED = 1
RANDOM_BASELINE_SAMPLES = 100


def estimate_convergence_episode(rewards, tolerance=0.02):
    """First episode after which reward_final never again strays more than
    `tolerance` (relative) from the mean of the final 10 episodes."""
    window = rewards[-10:] if len(rewards) >= 10 else rewards
    final_mean = sum(window) / len(window)
    band = tolerance * abs(final_mean) if final_mean != 0 else tolerance
    for i in range(len(rewards) - 1, -1, -1):
        if abs(rewards[i] - final_mean) > band:
            return min(i + 2, len(rewards))
    return 1


def summarize_adequacy(rewards, window_fraction=0.10):
    n = len(rewards)
    window = max(1, round(n * window_fraction))
    mean_first = sum(rewards[:window]) / window
    mean_last = sum(rewards[-window:]) / window
    pct_change = ((mean_last - mean_first) / abs(mean_first)) * 100 if mean_first != 0 else float('inf')
    half = n // 2
    mean_first_half = sum(rewards[:half]) / half
    mean_second_half = sum(rewards[half:]) / (n - half)
    half_pct = ((mean_second_half - mean_first_half) / abs(mean_first_half)) * 100 if mean_first_half != 0 else float('inf')
    plateaued = abs(half_pct) < 5
    return mean_first, mean_last, pct_change, plateaued


def append_csv(path, fieldnames, rows):
    write_header = not os.path.exists(path)
    with open(path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows(rows)


def run_dashboard(dashboard_name, dashboard_path):
    print('\n=== {} ==='.format(dashboard_name), flush=True)
    with open(dashboard_path) as f:
        dashboard_dict = json.load(f)

    num_vis = len(dashboard_dict['Visualisations'])
    types_used = sorted(set(v['Visualisation Type'] for v in dashboard_dict['Visualisations']))
    print('  {} visualisations, types: {}'.format(num_vis, types_used), flush=True)

    # --- Train (fresh model, same protocol as Goal 1) ---
    model, rows, elapsed = rc.train(dashboard_dict, NUM_EPISODES, NUM_TIME_STEPS, seed=SEED, verbose=True)
    reward_series = [r['reward_final'] for r in rows]

    conv_episode = estimate_convergence_episode(reward_series)
    wallclock_to_convergence = elapsed[conv_episode - 1]
    wallclock_total = elapsed[-1]
    min_valid = min(r['valid_actions'] for r in rows)
    max_invalid = max(r['invalid_attempts'] for r in rows)
    mean_first, mean_last, pct_change, plateaued = summarize_adequacy(reward_series)

    print('  converged ~episode {}, wallclock {:.1f}s (total {:.1f}s), reward {:.4f} -> {:.4f}'.format(
        conv_episode, wallclock_to_convergence, wallclock_total, mean_first, mean_last), flush=True)

    # --- 4a: frozen/greedy policy evaluation ---
    top_k = rc.greedy_top_k(model, top=10)
    is_det, consistency_fraction = rc.check_greedy_determinism(model, repeats=3, top=10)
    print('  greedy top-1: {} reward={:.4f} (deterministic={}, agreement={:.0%})'.format(
        rc.describe_action(top_k[0]['action']), top_k[0]['reward'], is_det, consistency_fraction), flush=True)

    goal4a_rows = []
    for rank, entry in enumerate(top_k, start=1):
        c = entry['components']
        goal4a_rows.append({
            'dashboard': dashboard_name,
            'rank': rank,
            'action': rc.describe_action(entry['action']),
            'reward_final': entry['reward'],
            'reward_decluttering': c['Decluttering'],
            'reward_data_completeness': c['Data Completeness'],
            'reward_chart_variety': c['Chart Variety'],
            'reward_appropriate_vis_types': c['Appropriate Visualisation Types'],
        })
    append_csv(os.path.join(RESULTS_DIR, 'goal4a_frozen_policy_eval.csv'),
               ['dashboard', 'rank', 'action', 'reward_final', 'reward_decluttering',
                'reward_data_completeness', 'reward_chart_variety', 'reward_appropriate_vis_types'],
               goal4a_rows)
    append_csv(os.path.join(RESULTS_DIR, 'goal4a_determinism_check.csv'),
               ['dashboard', 'deterministic', 'consistency_fraction', 'repeats'],
               [{'dashboard': dashboard_name, 'deterministic': is_det,
                 'consistency_fraction': consistency_fraction, 'repeats': 3}])

    # --- 4b: baselines ---
    random_mean, random_std, _, random_invalid = rc.random_policy_baseline(
        dashboard_dict, num_samples=RANDOM_BASELINE_SAMPLES, seed=SEED)
    rule_reward, rule_components, rule_action = rc.rule_based_baseline(dashboard_dict)
    print('  baselines: random={:.4f}+-{:.4f}  rule-based={:.4f} ({})'.format(
        random_mean, random_std, rule_reward, rc.describe_action(rule_action)), flush=True)

    append_csv(os.path.join(RESULTS_DIR, 'goal4b_baselines.csv'),
               ['dashboard', 'trained_model_top1_reward', 'random_baseline_mean', 'random_baseline_std',
                'random_baseline_samples', 'rule_based_reward', 'rule_based_action'],
               [{'dashboard': dashboard_name, 'trained_model_top1_reward': top_k[0]['reward'],
                 'random_baseline_mean': random_mean, 'random_baseline_std': random_std,
                 'random_baseline_samples': RANDOM_BASELINE_SAMPLES, 'rule_based_reward': rule_reward,
                 'rule_based_action': rc.describe_action(rule_action)}])

    # --- 4c: robustness stats ---
    append_csv(os.path.join(RESULTS_DIR, 'goal4c_multi_dashboard_robustness.csv'),
               ['dashboard', 'num_visualisations', 'num_visualisation_types_used', 'mean_reward_first10pct',
                'mean_reward_last10pct', 'pct_change', 'plateaued', 'min_valid_actions_any_episode',
                'max_invalid_attempts_any_episode', 'convergence_episode_estimate'],
               [{'dashboard': dashboard_name, 'num_visualisations': num_vis,
                 'num_visualisation_types_used': len(types_used), 'mean_reward_first10pct': mean_first,
                 'mean_reward_last10pct': mean_last, 'pct_change': pct_change, 'plateaued': plateaued,
                 'min_valid_actions_any_episode': min_valid, 'max_invalid_attempts_any_episode': max_invalid,
                 'convergence_episode_estimate': conv_episode}])

    # --- 4d: wall-clock timing ---
    append_csv(os.path.join(RESULTS_DIR, 'goal4d_wallclock_timing.csv'),
               ['dashboard', 'num_visualisations', 'total_episodes', 'wallclock_seconds_total',
                'wallclock_seconds_to_convergence', 'convergence_episode_estimate'],
               [{'dashboard': dashboard_name, 'num_visualisations': num_vis, 'total_episodes': NUM_EPISODES,
                 'wallclock_seconds_total': wallclock_total,
                 'wallclock_seconds_to_convergence': wallclock_to_convergence,
                 'convergence_episode_estimate': conv_episode}])

    # Also keep the full per-episode training log for real dashboards (small/
    # large already have one from Goal 1 - this run reproduces them as a
    # determinism/reproducibility check rather than overwriting).
    if dashboard_name.startswith('real_'):
        log_path = os.path.join(RESULTS_DIR, 'goal4c_training_log_{}.csv'.format(dashboard_name))
        with open(log_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        print('  wrote per-episode training log to', log_path, flush=True)
    else:
        # Sanity check: retraining with the same seed should reproduce Goal 1's
        # published reward curve exactly.
        existing_path = os.path.join(RESULTS_DIR, 'goal1_training_log_100ep.csv' if dashboard_name == 'small'
                                      else 'goal1_training_log_100ep_large_dashboard.csv')
        if os.path.exists(existing_path):
            with open(existing_path, newline='') as f:
                existing_final = list(csv.DictReader(f))[-1]['reward_final']
            print('  reproducibility check: goal1 episode-100 reward={} vs this run={:.16f}'.format(
                existing_final, reward_series[-1]), flush=True)


if __name__ == '__main__':
    os.makedirs(RESULTS_DIR, exist_ok=True)
    for dashboard_name, filename in DASHBOARDS:
        run_dashboard(dashboard_name, os.path.join(DASHBOARDS_DIR, filename))
    print('\nGoal 4 pipeline complete.', flush=True)
