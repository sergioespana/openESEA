"""
Shared helpers for the RL evaluation scripts (Goals 1-4). Centralises:
- backend import path setup
- environment construction from a dashboard dict
- reward component computation (unweighted, and weighted/normalised)
- candidate-action enumeration and human-readable action descriptions
- training (re-implements DashboardRLModel.run_episode with logging, see
  Goal 1's original goal1_training_run.py - kept here so goal4 scripts can
  get the live trained model object back, not just a CSV)
- frozen/greedy policy evaluation (Goal 4a)
- random-policy and rule-based baselines (Goal 4b)

Nothing here changes the reward formulas, weights, action space, or state
encoding used by the live model - it only wraps the existing code for
repeated, instrumented, read-only use.
"""
import copy
import os
import random
import sys
import time

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import torch  # noqa: E402

from core.DashboardRLModel.DashboardRLModel import DashboardRLModel  # noqa: E402
from core.DashboardRLModel.Dashboard.Environment import DashboardEnvironment  # noqa: E402
from core.DashboardRLModel.Dashboard.Classes import VisualisationType  # noqa: E402
from core.DashboardRLModel.Dashboard.Parser import parseDashboard, VISUALISATION_NAME_MAPPING  # noqa: E402
from core.DashboardRLModel.Dashboard.Actions.Classes import ChangeVisualisationType, AddItemLimit, RemoveItemLimit  # noqa: E402
from core.DashboardRLModel.Dashboard.Actions.Information import ACTIONS  # noqa: E402
from core.DashboardRLModel.AgentNetwork.AgentNetwork import ForwardPass  # noqa: E402

DEFAULT_WEIGHTS = {
    'Decluttering': 1.0,
    'Appropriate Visualisation Types': 0.8,
    'Chart Variety': 0.5,
    'Data Completeness': 0.2,
}

CHANGE_TYPE_ACTION_INDEX = ACTIONS.index(ChangeVisualisationType)
ADD_LIMIT_ACTION_INDEX = ACTIONS.index(AddItemLimit)
REMOVE_LIMIT_ACTION_INDEX = ACTIONS.index(RemoveItemLimit)


# --------------------------------------------------------------------------
# Environment / reward helpers
# --------------------------------------------------------------------------

def build_env(dashboard_dict):
    dashboard = parseDashboard(dashboard_dict)
    capacity = max(20, int(len(dashboard_dict['Visualisations']) * 1.2))
    return DashboardEnvironment(dashboard, capacity)


def compute_components(env, dashboard):
    """Unweighted (raw) reward component values for a given Dashboard object."""
    return {
        'Decluttering': DashboardEnvironment.reward_decluttering(env, dashboard),
        'Chart Variety': DashboardEnvironment.reward_visualisation_variety(env, dashboard),
        'Data Completeness': DashboardEnvironment.reward_data_completeness(env, dashboard),
        'Appropriate Visualisation Types': DashboardEnvironment.reward_appropriate_visualisation_types(env, dashboard),
    }


def weighted_final_reward(components, weights=None):
    """R_Final: weighted-and-normalised combination, matching DashboardEnvironment.reward()."""
    weights = weights or DEFAULT_WEIGHTS
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0
    weighted_sum = sum(components[name] * weight for name, weight in weights.items())
    return weighted_sum / total_weight


def describe_action(action):
    if action is None:
        return 'NoOp'
    if isinstance(action, RemoveItemLimit):
        return 'RemoveItemLimit(vis={})'.format(action.visualisationIndex)
    if isinstance(action, AddItemLimit):
        return 'AddItemLimit(vis={}, limit={})'.format(action.visualisationIndex, action.itemLimit)
    if isinstance(action, ChangeVisualisationType):
        name = VISUALISATION_NAME_MAPPING[VisualisationType(action.visualisationType)]
        return 'ChangeVisualisationType(vis={}, to={})'.format(action.visualisationIndex, name)
    return str(action)


def evaluate_action(env, action, weights=None):
    """Apply `action` (or None for no-op) to a fresh copy of the initial
    dashboard and return (reward, components)."""
    resulting = copy.deepcopy(env.initial_dashboard)
    if action is not None:
        action.act(resulting)
    components = compute_components(env, resulting)
    reward = weighted_final_reward(components, weights)
    return reward, components


def enumerate_candidate_actions(env):
    """All actions that pass the model's own action/parameter masks, across
    every visualisation in the dashboard (not just index 0)."""
    candidates = []
    num_vis = len(env.dashboard.visualisations)
    for vis_index in range(num_vis):
        action_mask = env.get_action_mask(vis_index)
        for action_index, action_class in enumerate(ACTIONS):
            if not action_mask[action_index]:
                continue
            if action_class is RemoveItemLimit:
                candidates.append(RemoveItemLimit(vis_index))
            elif action_class is AddItemLimit:
                param_mask = env.get_parameter_mask(vis_index, action_index, [], 0)
                candidates += [AddItemLimit(vis_index, v) for v, ok in enumerate(param_mask) if ok]
            elif action_class is ChangeVisualisationType:
                param_mask = env.get_parameter_mask(vis_index, action_index, [], 0)
                candidates += [ChangeVisualisationType(vis_index, v) for v, ok in enumerate(param_mask) if ok]
    return candidates


# --------------------------------------------------------------------------
# Training (Goal 1's instrumented loop, but returns the live model too)
# --------------------------------------------------------------------------

def train(dashboard_dict, num_episodes, num_time_steps=200, seed=42, log_every=10, verbose=True):
    """Re-implements DashboardRLModel.run_episode's per-episode training loop
    (unmodified masking/sampling/action-space/network/gradient-update logic)
    with per-episode logging. Returns (model, rows, elapsed_seconds_per_episode)."""
    torch.manual_seed(seed)

    model = DashboardRLModel(dashboard_dict)
    model.num_episodes = num_episodes
    model.num_time_steps = num_time_steps

    env = model.dashboard_environment
    net = model.agent_network

    hard_cap = num_time_steps * 20

    rows = []
    elapsed_per_episode = []
    start_time = time.time()

    for episode in range(1, num_episodes + 1):
        state = env.initial()

        sampled_actions = 0
        invalid_attempts = 0
        t = 0

        sum_reward_final = 0.0
        sum_decluttering = 0.0
        sum_data_completeness = 0.0
        sum_chart_variety = 0.0
        sum_appropriate_vis = 0.0

        while True:
            t += 1
            outputs, saved_action = net.output_parameter_values(state)
            if outputs is None:
                invalid_attempts += 1
                if t >= hard_cap:
                    break
                continue
            sampled_actions += 1

            state, reward, done, flags = env.step(outputs)

            net.saved_actions.append(saved_action)
            net.rewards.append(reward)

            sum_reward_final += reward
            current_dashboard = env.dashboard
            sum_decluttering += DashboardEnvironment.reward_decluttering(env, current_dashboard)
            sum_data_completeness += DashboardEnvironment.reward_data_completeness(env, current_dashboard)
            sum_chart_variety += DashboardEnvironment.reward_visualisation_variety(env, current_dashboard)
            sum_appropriate_vis += DashboardEnvironment.reward_appropriate_visualisation_types(env, current_dashboard)

            if done:
                break
            if t >= num_time_steps and sampled_actions > num_time_steps / 10:
                break

        net.update_network_gradients()

        denom = sampled_actions if sampled_actions > 0 else 1
        row = {
            'episode': episode,
            'reward_final': sum_reward_final / denom,
            'reward_decluttering': sum_decluttering / denom,
            'reward_data_completeness': sum_data_completeness / denom,
            'reward_chart_variety': sum_chart_variety / denom,
            'reward_appropriate_vis_types': sum_appropriate_vis / denom,
            'valid_actions': sampled_actions,
            'invalid_attempts': invalid_attempts,
        }
        rows.append(row)
        elapsed_per_episode.append(time.time() - start_time)

        if verbose and (episode % log_every == 0 or episode == 1):
            print('Episode {}\treward_final={:.4f}\tvalid={}\tinvalid={}\telapsed={:.1f}s'.format(
                episode, row['reward_final'], sampled_actions, invalid_attempts, elapsed_per_episode[-1]))

    return model, rows, elapsed_per_episode


# --------------------------------------------------------------------------
# Goal 4a: frozen / greedy policy evaluation
# --------------------------------------------------------------------------

def greedy_top_k(model, top=10):
    """Deterministic top-K actions from the trained (frozen) network, using
    the same enumeration path as DashboardRLModel.predict() /
    AgentNetwork.forward_predict (no gradient updates, no random sampling -
    forward_predict only ever enumerates categorical options and sorts by
    probability, it never calls torch.distributions.Categorical.sample())."""
    env = model.dashboard_environment
    tensor_state = torch.as_tensor(env.initial(), dtype=torch.float)
    outputs_list = model.agent_network(ForwardPass.PREDICT, tensor_state, top=top)

    results = []
    for values in outputs_list:
        parameter_values = [v.item() for v in values]
        action = env.action_from_parameters(parameter_values)
        reward, components = evaluate_action(env, action)
        results.append({'action': action, 'reward': reward, 'components': components})
    return results


def check_greedy_determinism(model, repeats=3, top=10):
    """Empirical confirmation that greedy_top_k is deterministic: run it
    `repeats` times and check the #1 action + reward are identical every
    time. Returns (is_deterministic, fraction_agreeing_with_first_run)."""
    runs = [greedy_top_k(model, top=top) for _ in range(repeats)]
    first_top1 = describe_action(runs[0][0]['action'])
    agreements = sum(1 for r in runs if describe_action(r[0]['action']) == first_top1)
    return agreements == repeats, agreements / repeats


# --------------------------------------------------------------------------
# Goal 4b: baselines
# --------------------------------------------------------------------------

def _sample_uniform_valid_action(env, rng):
    """Uniform-random draw from the same hierarchical masked action space
    the network samples from (visualisation -> action -> parameter), but
    with a uniform distribution at each stage instead of the network's
    learned probabilities. Returns None if the drawn (visualisation, action)
    combination turns out to have zero valid parameter values (the same
    edge case the trained network's own sampler treats as an invalid
    attempt and retries from - see AgentNetwork.forward_sample's `if
    parameter_probs is None: return None, None, None`)."""
    num_vis = len(env.dashboard.visualisations)
    vis_index = rng.randrange(num_vis)

    action_mask = env.get_action_mask(vis_index)
    valid_action_indices = [i for i, ok in enumerate(action_mask) if ok]
    action_index = rng.choice(valid_action_indices)
    action_class = ACTIONS[action_index]

    if action_class is RemoveItemLimit:
        return RemoveItemLimit(vis_index)

    param_mask = env.get_parameter_mask(vis_index, action_index, [], 0)
    valid_param_values = [v for v, ok in enumerate(param_mask) if ok]
    if not valid_param_values:
        return None
    param_value = rng.choice(valid_param_values)

    if action_class is AddItemLimit:
        return AddItemLimit(vis_index, param_value)
    return ChangeVisualisationType(vis_index, param_value)


def random_policy_baseline(dashboard_dict, num_samples=100, seed=42, weights=None, max_retries=1000):
    rng = random.Random(seed)
    rewards = []
    invalid_attempts = 0
    for _ in range(num_samples):
        env = build_env(dashboard_dict)
        action = None
        for _retry in range(max_retries):
            action = _sample_uniform_valid_action(env, rng)
            if action is not None:
                break
            invalid_attempts += 1
        if action is None:
            raise RuntimeError('Could not sample a valid random action within max_retries')
        reward, _ = evaluate_action(env, action, weights)
        rewards.append(reward)
    mean = sum(rewards) / len(rewards)
    variance = sum((r - mean) ** 2 for r in rewards) / len(rewards)
    return mean, variance ** 0.5, rewards, invalid_attempts


def _ideal_visualisation_type(data_items):
    """Simple, non-learned threshold rule (single value -> single-value
    display; a handful of values -> pie; more -> bar; a lot / time-series
    scale -> line), matching the thresholds already used as the literature
    basis for `reward_appropriate_visualisation_types`."""
    if data_items == 1:
        return VisualisationType.SINGLE
    if data_items <= 6:
        return VisualisationType.PIE
    if data_items <= 15:
        return VisualisationType.BAR
    return VisualisationType.LINE


def rule_based_action(env):
    """Scans visualisations in dashboard order and returns a
    ChangeVisualisationType action for the first one whose current type
    doesn't match the threshold rule's ideal type for its data-item count
    (and where that change is actually valid under the model's own masking).
    Returns None if every visualisation already matches (no-op)."""
    for vis_index, vis in enumerate(env.dashboard.visualisations):
        ideal = _ideal_visualisation_type(vis.dataItems)
        if vis.visualisationType == ideal:
            continue
        action_mask = env.get_action_mask(vis_index)
        if not action_mask[CHANGE_TYPE_ACTION_INDEX]:
            continue
        param_mask = env.get_parameter_mask(vis_index, CHANGE_TYPE_ACTION_INDEX, [], 0)
        if not param_mask[int(ideal)]:
            continue
        return ChangeVisualisationType(vis_index, int(ideal))
    return None


def rule_based_baseline(dashboard_dict, weights=None):
    env = build_env(dashboard_dict)
    action = rule_based_action(env)
    reward, components = evaluate_action(env, action, weights)
    return reward, components, action
