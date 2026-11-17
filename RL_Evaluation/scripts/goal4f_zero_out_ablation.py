"""
Goal 4f (stretch) - Deeper ablation: zero out one reward component at a time
(rather than just reweighting, as Goal 2 did) and check how much the #1
recommended action changes per test dashboard state. Like Goal 2, this does
not retrain the network - only recomputes the existing, unmodified reward
formulas under different weight configurations.
"""
import copy
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import rl_common as rc  # noqa: E402
from dashboard_fixture import SENSITIVITY_STATE_BAR_5, SENSITIVITY_STATE_PIE_9  # noqa: E402

DASHBOARDS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'dashboards'))
RESULTS_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'results'))

BASELINE = rc.DEFAULT_WEIGHTS

ABLATIONS = {
    'baseline': dict(BASELINE),
    'zero_decluttering': {**BASELINE, 'Decluttering': 0.0},
    'zero_appropriate_vis_types': {**BASELINE, 'Appropriate Visualisation Types': 0.0},
    'zero_chart_variety': {**BASELINE, 'Chart Variety': 0.0},
    'zero_data_completeness': {**BASELINE, 'Data Completeness': 0.0},
}

with open(os.path.join(DASHBOARDS_DIR, 'small.json')) as f:
    SMALL_DASHBOARD = json.load(f)
with open(os.path.join(DASHBOARDS_DIR, 'real_energy_climate.json')) as f:
    REAL_ENERGY_CLIMATE = json.load(f)

TEST_STATES = {
    'bar_chart_5items': SENSITIVITY_STATE_BAR_5,
    'pie_chart_9items': SENSITIVITY_STATE_PIE_9,
    'small_dashboard': SMALL_DASHBOARD,
    'real_energy_climate': REAL_ENERGY_CLIMATE,
}


def rank_within(values):
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    ranks = [0] * len(values)
    for rank, index in enumerate(order, start=1):
        ranks[index] = rank
    return ranks


def evaluate_state(state_id, dashboard_dict):
    env = rc.build_env(dashboard_dict)
    candidates = rc.enumerate_candidate_actions(env)

    per_ablation_rewards = {name: [] for name in ABLATIONS}
    rows = []
    for action in candidates:
        row = {'dashboard_state_id': state_id, 'candidate_action': rc.describe_action(action)}
        for name, weights in ABLATIONS.items():
            reward, _ = rc.evaluate_action(env, action, weights)
            row['reward_' + name] = reward
            per_ablation_rewards[name].append(reward)
        rows.append(row)

    ranks_by_ablation = {name: rank_within(per_ablation_rewards[name]) for name in ABLATIONS}
    for i, row in enumerate(rows):
        for name in ABLATIONS:
            row['rank_' + name] = ranks_by_ablation[name][i]
        row['top1_changed_vs_baseline'] = any(
            ranks_by_ablation[name][i] == 1 and ranks_by_ablation['baseline'][i] != 1
            for name in ABLATIONS if name != 'baseline'
        ) or (ranks_by_ablation['baseline'][i] == 1 and any(
            ranks_by_ablation[name][i] != 1 for name in ABLATIONS if name != 'baseline'))

    top1_by_ablation = {name: rows[ranks_by_ablation[name].index(1)]['candidate_action'] for name in ABLATIONS}
    print('[{}] top-1 per ablation:'.format(state_id))
    for name, action_desc in top1_by_ablation.items():
        marker = '' if action_desc == top1_by_ablation['baseline'] else '  <-- CHANGED vs baseline'
        print('  {:30s} {}{}'.format(name, action_desc, marker))

    return rows


if __name__ == '__main__':
    os.makedirs(RESULTS_DIR, exist_ok=True)
    all_rows = []
    for state_id, dashboard_dict in TEST_STATES.items():
        all_rows += evaluate_state(state_id, dashboard_dict)

    fieldnames = ['dashboard_state_id', 'candidate_action'] + \
        ['reward_' + name for name in ABLATIONS] + \
        ['rank_' + name for name in ABLATIONS] + \
        ['top1_changed_vs_baseline']

    output_path = os.path.join(RESULTS_DIR, 'goal4f_zero_out_ablation.csv')
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print('\nWrote {} rows to {}'.format(len(all_rows), output_path))
