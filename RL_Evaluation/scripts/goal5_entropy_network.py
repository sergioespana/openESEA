"""
Goal 5 (design-review follow-up) - evaluation-only entropy-bonus variant of
the training loop, used ONLY by goal5_hyperparameter_sensitivity.py.

The design review flagged that AgentNetwork.py's policy loss has no entropy
regularisation term, plausibly contributing (together with GAMMA=1.0 and
LEARNING_RATE=1e-2) to the observed premature policy collapse (per-episode
reward_final becoming bit-for-bit identical across consecutive episodes).
To test that hypothesis we need the full categorical distribution (not just
the sampled action's log-prob) at each of the three hierarchical sampling
stages (visualisation / action / parameter), so we can compute its entropy
and add `-entropy_coef * mean_entropy` to the loss.

Per the Goal 5 brief, this is implemented as a **non-production, evaluation-
only subclass** of the shipped AgentNetork, not a change to AgentNetwork.py
itself:
- `EntropyAgentNetwork` overrides `forward_sample` (adds a `dist.entropy()`
  call at each stage - entropy() is a deterministic function of the already-
  computed probabilities, so it consumes no extra calls to the RNG and does
  not change the sequence of `Categorical(...).sample()` draws relative to
  the stock network) and `update_network_gradients` (identical REINFORCE-
  with-baseline recipe, plus the entropy-bonus term).
- `EntropyDashboardRLModel` re-implements the ~10 lines of
  `DashboardRLModel.__init__` needed to build an environment + network pair,
  substituting `EntropyAgentNetwork` for `AgentNetwork`.
- `train_entropy()` is a copy of `rl_common.train()`'s per-episode training
  loop (masking/sampling/action-space/gradient-update logic unchanged),
  extended only to also log each episode's mean sampling entropy.

GAMMA is read as `AgentNetworkModule.GAMMA` (not a bare imported name) inside
`update_network_gradients` so that goal5_hyperparameter_sensitivity.py's
module-attribute patching of `AgentNetworkModule.GAMMA` (see that script's
docstring) also applies here, exactly as it does for the stock network.
LEARNING_RATE patching works automatically: `EntropyAgentNetwork.__init__`
calls `AgentNetwork.__init__` via `super()`, which reads `LEARNING_RATE` from
the same module namespace at construction time.
"""
import os
import sys
import time

BACKEND_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..',
                                             'openESEA_interpreter', 'backend'))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import torch  # noqa: E402
import torch.nn.functional as F  # noqa: E402
from torch.distributions import Categorical  # noqa: E402

import core.DashboardRLModel.AgentNetwork.AgentNetwork as AgentNetworkModule  # noqa: E402
from core.DashboardRLModel.AgentNetwork.AgentNetwork import (  # noqa: E402
    AgentNetwork, mask_probabilities, one_hot_encode_categorical)
from core.DashboardRLModel.AgentNetwork.Constants import EPSILON  # noqa: E402
from core.DashboardRLModel.Dashboard.Environment import DashboardEnvironment  # noqa: E402
from core.DashboardRLModel.Dashboard.Parser import parseDashboard  # noqa: E402
from core.DashboardRLModel.Dashboard.Encoding import dashboardToArray  # noqa: E402
from core.DashboardRLModel.Dashboard.Actions.Information import ACTIONS_PARAMETERS, NUM_ACTIONS  # noqa: E402


class EntropyAgentNetwork(AgentNetwork):
    """Evaluation-only variant of AgentNetwork - see module docstring."""

    def __init__(self, *args, entropy_coef=0.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.entropy_coef = entropy_coef
        self.saved_entropies = []

    def forward_sample(self, state):
        log_probabilities = []
        sampled_values = []
        extra_inputs = []
        entropies = []

        ### Feed forward: Visualisation Layer ###
        hidden_state, visualisation_probs = self.visualisation_layer(state)

        ### Masking probabilities: Visualisation ###
        visualisation_probs = mask_probabilities(visualisation_probs, self.get_visualisation_mask())
        if visualisation_probs is None:
            return None, None, None, None

        ### Sampling: Visualisation ###
        dist = Categorical(visualisation_probs)
        sampled_visualisation = dist.sample()
        log_prob_vis = dist.log_prob(sampled_visualisation)
        entropies.append(dist.entropy())
        sampled_values.append(sampled_visualisation)
        log_probabilities.append(log_prob_vis)
        extra_inputs.append(one_hot_encode_categorical(visualisation_probs, sampled_visualisation))

        ### Feed forward: Action layer ###
        hidden_state, action_probs = self.action_layer(hidden_state, extra_inputs)

        ### Masking probabilities: Action ###
        action_probs = mask_probabilities(action_probs, self.get_action_mask(sampled_visualisation))

        ### Sampling: Action ###
        dist = Categorical(action_probs)
        sampled_action = dist.sample()
        log_prob_action = dist.log_prob(sampled_action)
        entropies.append(dist.entropy())
        sampled_values.append(sampled_action)
        log_probabilities.append(log_prob_action)
        extra_inputs.append(one_hot_encode_categorical(action_probs, sampled_action))

        ### Parameter layers ###
        for param_index, param_layer in enumerate(self.action_layers_list[sampled_action][0]):
            hidden_state, parameter_probs = param_layer(hidden_state, extra_inputs)

            parameter_probs = mask_probabilities(
                parameter_probs,
                self.get_parameter_mask(sampled_visualisation, sampled_action, sampled_values[2:], param_index))
            if parameter_probs is None:
                return None, None, None, None

            dist = Categorical(parameter_probs)
            sampled_parameter = dist.sample()
            log_prob_parameter = dist.log_prob(sampled_parameter)
            entropies.append(dist.entropy())
            sampled_values.append(sampled_parameter)
            log_probabilities.append(log_prob_parameter)
            extra_inputs.append(one_hot_encode_categorical(parameter_probs, sampled_parameter))

        ### Critic layer ###
        critic_value = self.action_layers_list[sampled_action][1](hidden_state, extra_inputs)

        # Joint entropy of the hierarchical decision = sum of each stage's
        # conditional entropy (chain rule for entropy; later stages already
        # condition on earlier ones' one-hot-encoded sampled values).
        total_entropy = torch.stack(entropies).sum()
        return sampled_values, log_probabilities, critic_value, total_entropy

    def output_parameter_values(self, state):
        tensor_state = torch.as_tensor(state, dtype=torch.float)
        parameter_values, parameter_probabilities, critic_value, entropy = self.forward_sample(tensor_state)
        if parameter_values is None:
            return None, None
        saved_action = (parameter_probabilities, critic_value)
        self.saved_entropies.append(entropy)
        return parameter_values, saved_action

    def update_network_gradients(self):
        if len(self.rewards) < 2:
            del self.rewards[:]
            del self.saved_actions[:]
            del self.user_rewards[:]
            del self.saved_user_actions[:]
            del self.saved_entropies[:]
            return

        R = 0
        returns = []
        for r in self.rewards[::-1]:
            R = r + AgentNetworkModule.GAMMA * R
            returns.insert(0, R)

        returns = torch.tensor(returns).float()
        returns = (returns - returns.mean()) / (returns.std() + EPSILON)

        user_weight = len(self.rewards) / (len(self.user_rewards) + EPSILON)
        user_returns = torch.tensor(self.user_rewards).float()
        user_returns = torch.mul(user_returns, torch.tensor(user_weight))

        returns = torch.cat([returns, user_returns], dim=0)
        saved_actions = self.saved_actions + self.saved_user_actions

        policy_losses = []
        value_losses = []
        for (log_probs, critic_value), R in zip(saved_actions, returns):
            advantage = R - critic_value.detach()
            log_prob = torch.stack(log_probs).sum()
            policy_losses.append(-log_prob * advantage)
            value_losses.append(F.smooth_l1_loss(critic_value, torch.tensor([R])))

        mean_entropy = (torch.stack(self.saved_entropies).mean()
                        if len(self.saved_entropies) > 0 else torch.tensor(0.0))

        loss = (torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()
                - self.entropy_coef * mean_entropy)

        self.optimizer.zero_grad()
        torch.autograd.set_detect_anomaly(True)
        loss.backward()
        self.optimizer.step()

        del self.rewards[:]
        del self.saved_actions[:]
        del self.user_rewards[:]
        del self.saved_user_actions[:]
        del self.saved_entropies[:]


class EntropyDashboardRLModel:
    """Re-implements the handful of lines of DashboardRLModel.__init__ needed
    to build an (environment, network) pair, substituting EntropyAgentNetwork
    for the shipped AgentNetwork. Nothing about dashboard parsing, state
    encoding, or environment construction is changed."""

    def __init__(self, dashboard_dict, entropy_coef):
        self.visualisation_capacity = max(20, int(len(dashboard_dict['Visualisations']) * 1.2))
        dashboard = parseDashboard(dashboard_dict)
        dashboard_array = dashboardToArray(dashboard, self.visualisation_capacity)
        num_inputs = len(dashboard_array)
        num_hidden = num_inputs

        self.dashboard_environment = DashboardEnvironment(dashboard, self.visualisation_capacity)
        self.agent_network = EntropyAgentNetwork(
            num_inputs, num_hidden, NUM_ACTIONS, self.visualisation_capacity,
            ACTIONS_PARAMETERS, self.dashboard_environment, entropy_coef=entropy_coef)


def train_entropy(dashboard_dict, num_episodes, entropy_coef, num_time_steps=200, seed=42,
                   log_every=10, verbose=True):
    """Same per-episode training loop as rl_common.train(), using
    EntropyAgentNetwork instead of the stock AgentNetwork, and additionally
    logging each episode's mean sampling entropy (mean over valid steps of
    the summed per-stage entropy)."""
    torch.manual_seed(seed)

    model = EntropyDashboardRLModel(dashboard_dict, entropy_coef)
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

        # Capture mean entropy for this episode BEFORE update_network_gradients
        # clears the buffer.
        if len(net.saved_entropies) > 0:
            mean_entropy = sum(e.item() for e in net.saved_entropies) / len(net.saved_entropies)
        else:
            mean_entropy = float('nan')

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
            'mean_entropy': mean_entropy,
        }
        rows.append(row)
        elapsed_per_episode.append(time.time() - start_time)

        if verbose and (episode % log_every == 0 or episode == 1):
            print('Episode {}\treward_final={:.4f}\tmean_entropy={:.4f}\tvalid={}\tinvalid={}\telapsed={:.1f}s'.format(
                episode, row['reward_final'], mean_entropy, sampled_actions, invalid_attempts,
                elapsed_per_episode[-1]))

    return model, rows, elapsed_per_episode
