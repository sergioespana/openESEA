"""
Goal 1 - Training / Reward Convergence Log.

Re-implements the per-episode training loop from
core/DashboardRLModel/DashboardRLModel.py::run_episode with added
instrumentation: per-episode mean R_Final, per-episode mean of each of the
four *unweighted* reward components, and valid/invalid action counts.

The underlying algorithm (masking, sampling, action space, network
architecture, gradient update) and the reward weights are untouched - this
script only adds read-only logging around the existing training loop.

Usage:
    python goal1_training_run.py --episodes 100 --time-steps 200 \
        --output ../results/goal1_training_log_100ep.csv --seed 42
"""
import argparse
import csv
import os
import sys

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
sys.path.insert(0, BACKEND_DIR)

import torch  # noqa: E402

from core.DashboardRLModel.DashboardRLModel import DashboardRLModel  # noqa: E402
from core.DashboardRLModel.Dashboard.Environment import DashboardEnvironment  # noqa: E402

from dashboard_fixture import TRAINING_DASHBOARD, TRAINING_DASHBOARD_LARGE  # noqa: E402

DASHBOARDS = {
    'small': TRAINING_DASHBOARD,
    'large': TRAINING_DASHBOARD_LARGE,
}


def run_training(dashboard, num_episodes, num_time_steps, seed=42, log_every=10):
    torch.manual_seed(seed)

    model = DashboardRLModel(dashboard)
    model.num_episodes = num_episodes
    model.num_time_steps = num_time_steps

    env = model.dashboard_environment
    net = model.agent_network

    # Safety valve only - normal operation never approaches this, since the
    # action mask always keeps at least one valid (visualisation, action)
    # combination available.
    hard_cap = num_time_steps * 20

    rows = []
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

        # Update the agent network based on the accumulated rewards and losses
        # (identical call to the live training loop).
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

        if episode % log_every == 0 or episode == 1:
            print('Episode {}\treward_final={:.4f}\tvalid={}\tinvalid={}'.format(
                episode, row['reward_final'], sampled_actions, invalid_attempts))

    return rows


def write_csv(rows, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print('Wrote {} rows to {}'.format(len(rows), output_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=100)
    parser.add_argument('--time-steps', type=int, default=200)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--dashboard', type=str, choices=list(DASHBOARDS.keys()), default='small')
    parser.add_argument('--output', type=str, required=True)
    args = parser.parse_args()

    rows = run_training(DASHBOARDS[args.dashboard], args.episodes, args.time_steps, seed=args.seed)
    write_csv(rows, args.output)
