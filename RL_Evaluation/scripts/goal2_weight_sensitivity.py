"""
Goal 2 - Reward Weight Sensitivity Check.

For each test dashboard state, enumerates every valid candidate action
(respecting the exact same action/parameter masking the trained agent uses -
see DashboardEnvironment.get_action_mask / get_parameter_mask), applies it to
a copy of the initial state, and recomputes R_Final for that resulting state
under four weight sets. Only the weights differ between weight sets - the
reward formulas themselves (reward_decluttering, reward_data_completeness,
reward_visualisation_variety, reward_appropriate_visualisation_types) are
untouched and identical to the live model's.

This intentionally does NOT re-train the network - see the brief's note that
recomputing the reward formulas for candidate actions is sufficient to answer
the sensitivity question.
"""
import copy
import csv
import os
import sys

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
sys.path.insert(0, BACKEND_DIR)

from core.DashboardRLModel.Dashboard.Environment import DashboardEnvironment  # noqa: E402
from core.DashboardRLModel.Dashboard.Parser import parseDashboard, VISUALISATION_NAME_MAPPING  # noqa: E402
from core.DashboardRLModel.Dashboard.Actions.Classes import ChangeVisualisationType, AddItemLimit, RemoveItemLimit  # noqa: E402
from core.DashboardRLModel.Dashboard.Actions.Information import ACTIONS  # noqa: E402

from dashboard_fixture import SENSITIVITY_STATE_BAR_5, SENSITIVITY_STATE_PIE_9  # noqa: E402

WEIGHT_SETS = {
    1: {'Decluttering': 1.0, 'Appropriate Visualisation Types': 0.8, 'Chart Variety': 0.5, 'Data Completeness': 0.2},
    2: {'Decluttering': 0.5, 'Appropriate Visualisation Types': 0.8, 'Chart Variety': 0.5, 'Data Completeness': 0.2},
    3: {'Decluttering': 1.0, 'Appropriate Visualisation Types': 0.8, 'Chart Variety': 0.5, 'Data Completeness': 0.5},
    4: {'Decluttering': 1.0, 'Appropriate Visualisation Types': 1.0, 'Chart Variety': 1.0, 'Data Completeness': 1.0},
}


def build_env(dashboard_dict):
    dashboard = parseDashboard(dashboard_dict)
    capacity = max(20, int(len(dashboard_dict['Visualisations']) * 1.2))
    return DashboardEnvironment(dashboard, capacity)


def enumerate_candidate_actions(env, visualisation_index=0):
    candidates = []
    action_mask = env.get_action_mask(visualisation_index)
    for action_index, action_class in enumerate(ACTIONS):
        if not action_mask[action_index]:
            continue
        if action_class is RemoveItemLimit:
            candidates.append(RemoveItemLimit(visualisation_index))
        elif action_class is AddItemLimit:
            param_mask = env.get_parameter_mask(visualisation_index, action_index, [], 0)
            for value, valid in enumerate(param_mask):
                if valid:
                    candidates.append(AddItemLimit(visualisation_index, value))
        elif action_class is ChangeVisualisationType:
            param_mask = env.get_parameter_mask(visualisation_index, action_index, [], 0)
            for value, valid in enumerate(param_mask):
                if valid:
                    candidates.append(ChangeVisualisationType(visualisation_index, value))
    return candidates


def describe_action(action):
    if isinstance(action, RemoveItemLimit):
        return 'RemoveItemLimit'
    if isinstance(action, AddItemLimit):
        return 'AddItemLimit(limit={})'.format(action.itemLimit)
    if isinstance(action, ChangeVisualisationType):
        name = VISUALISATION_NAME_MAPPING[action.visualisationType]
        return 'ChangeVisualisationType(to={})'.format(name)
    return str(action)


def compute_final_reward(env, dashboard, weights):
    components = {
        'Decluttering': DashboardEnvironment.reward_decluttering(env, dashboard),
        'Chart Variety': DashboardEnvironment.reward_visualisation_variety(env, dashboard),
        'Data Completeness': DashboardEnvironment.reward_data_completeness(env, dashboard),
        'Appropriate Visualisation Types': DashboardEnvironment.reward_appropriate_visualisation_types(env, dashboard),
    }
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0
    weighted_sum = sum(components[name] * weight for name, weight in weights.items())
    return weighted_sum / total_weight


def rank_within(values):
    # values: list of floats. Returns 1-indexed ranks, ties broken by stable
    # sort (higher reward => rank 1).
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    ranks = [0] * len(values)
    for rank, index in enumerate(order, start=1):
        ranks[index] = rank
    return ranks


def evaluate_state(state_id, dashboard_dict):
    env = build_env(dashboard_dict)
    candidates = enumerate_candidate_actions(env, visualisation_index=0)

    rows = []
    rewards_by_weightset = {ws_id: [] for ws_id in WEIGHT_SETS}

    for action in candidates:
        resulting_dashboard = copy.deepcopy(env.initial_dashboard)
        action.act(resulting_dashboard)

        row = {'dashboard_state_id': state_id, 'candidate_action': describe_action(action)}
        for ws_id, weights in WEIGHT_SETS.items():
            reward = compute_final_reward(env, resulting_dashboard, weights)
            row['reward_weightset_{}'.format(ws_id)] = reward
            rewards_by_weightset[ws_id].append(reward)
        rows.append(row)

    for ws_id in WEIGHT_SETS:
        ranks = rank_within(rewards_by_weightset[ws_id])
        for row, rank in zip(rows, ranks):
            row['rank_weightset_{}'.format(ws_id)] = rank

    return rows


def write_csv(rows, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = ['dashboard_state_id', 'candidate_action',
                  'reward_weightset_1', 'reward_weightset_2', 'reward_weightset_3', 'reward_weightset_4',
                  'rank_weightset_1', 'rank_weightset_2', 'rank_weightset_3', 'rank_weightset_4']
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print('Wrote {} rows to {}'.format(len(rows), output_path))


if __name__ == '__main__':
    all_rows = []
    all_rows += evaluate_state('bar_chart_5items', SENSITIVITY_STATE_BAR_5)
    all_rows += evaluate_state('pie_chart_9items', SENSITIVITY_STATE_PIE_9)

    for row in all_rows:
        print(row)

    output_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'results',
                                                  'goal2_weight_sensitivity.csv'))
    write_csv(all_rows, output_path)
