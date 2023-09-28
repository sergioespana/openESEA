from .Classes import VisualisationType, Dashboard

from .Encoding import dashboardToArray

from .Information import MAX_DATA_ITEMS, MAX_ITEM_LIMIT

from .Actions.Information import ACTIONS
from .Actions.Classes import *

import copy
import torch

class DashboardEnvironment:
    def __init__(self, dashboard: Dashboard):
        self.initial_dashboard: Dashboard = copy.deepcopy(dashboard)

        self.dashboard: Dashboard = copy.deepcopy(dashboard)
        self.state = dashboardToArray(dashboard)

        self.state_rewards_info = [
            {
                'Name': 'Decluttering',
                'Weight': 1,
                'Function': DashboardEnvironment.reward_decluttering
            },
            {
                'Name': 'Data Completeness',
                'Weight': 0.1,
                'Function': DashboardEnvironment.reward_data_completeness
            },
            {
                'Name': 'Appropriate Visualisation Types',
                'Weight': 0.5,
                'Function': DashboardEnvironment.reward_appropriate_visualisation_types
            }
        ]
        self.action_rewards_info = [
            {
                'Name': 'Valid Action',
                'Weight': 1,
                'Function': DashboardEnvironment.reward_valid_action
            }
        ]

    def initial(self):
        return dashboardToArray(self.initial_dashboard)

    def step(self, outputs):
        # Construct the action from the model outputs
        action = self.action_from_outputs(outputs)

        # Perform action
        return self.perform_action(action)

    def action_from_outputs(self, outputs):
        # Convert parameter from tensors to simple values
        parameter_values = [output.item() for output in outputs]
        
        # Construct the action from the model outputs
        return self.action_from_parameters(parameter_values)
    
    def action_from_parameters(self, parameter_values):
        # Determine action, visualisation index and other parameters
        visualisation_index = parameter_values[0]
        action_index = parameter_values[1]
        other_parameters = parameter_values[2:]

        # Construct the action from the parameters
        action = ACTIONS[action_index](visualisation_index, *other_parameters)

        return action

    def perform_action(self, action):
        # Save dashboard before action
        previous_dashboard = copy.deepcopy(self.dashboard)

        # Perform the action on the dashboard
        action.act(self.dashboard)

        # Update state for new dashboard
        self.state = dashboardToArray(self.dashboard)

        # Determine reward for this step
        reward, explanation = self.reward(previous_dashboard, action)

        # Flags
        flags = { 'Explanation': None }

        # Always keep going
        done = False

        # Return state and reward
        return self.state, reward, done, flags

    def perform_action_on_initial(self, action):
        # Get initial dashboard
        dashboard = copy.deepcopy(self.initial_dashboard)

        # Perform the action on the dashboard
        action.act(dashboard)

        # Update state for new dashboard
        self.state = dashboardToArray(dashboard)

        # Determine reward for this step
        reward, explanation = self.reward(self.initial_dashboard, action)

        # Flags
        flags = { 'Explanation': explanation }

        # Always keep going
        done = False

        # Return state and reward
        return self.state, reward, done, flags

    def reward(self, previous_dashboard, action):
        current_dashboard = self.dashboard
        current_state_rewards  = self.collect_state_rewards(current_dashboard)
        previous_state_rewards = self.collect_state_rewards(previous_dashboard)
        
        # action_reward_weights = []
        # action_rewards = []
        # for action_reward_info in self.action_rewards_info:
        #     action_reward_weight = action_reward_info['Weight']
        #     action_reward_function = action_reward_info['Function']
        #     action_reward = action_reward_weight * action_reward_function(self, previous_dashboard, action)

        #     action_rewards.append(action_reward)
        #     action_reward_weights.append(action_reward_weight)

        current_state_reward_weight = 0
        current_state_reward = 0
        for reward, weight in current_state_rewards:
            current_state_reward += weight * reward
            current_state_reward_weight += weight

        if current_state_reward_weight == 0:
            return 0, ""
        
        normalized_reward = current_state_reward / current_state_reward_weight
        explanation = "Action chosen because of higher rewards w.r.t.:\n"
        # print(current_state_rewards, previous_state_rewards)
        for i in range(len(current_state_rewards)):
            c_reward, c_reward_weight = current_state_rewards[i]
            p_reward, p_reward_weight = previous_state_rewards[i]
            if c_reward > p_reward:
                # print('Unequal!')
                # print('Dashboard')
                # print(current_dashboard)
                # print('Dashboard prev')
                # print(previous_dashboard)
                # print('Action')
                # print(action)
                # print('Rewards')
                # print(current_state_rewards)
                # print('Rewards prev')
                # print(previous_state_rewards)
                # input()
                explanation += "\t" + self.state_rewards_info[i]["Name"] + "\t" + "Reward difference: " + str(c_reward - p_reward) + "\t" + "Weighted: " + str(c_reward_weight * (c_reward - p_reward)) + "\n"
        # print(explanation)
        return normalized_reward, explanation

    def collect_state_rewards(self, state):
        state_rewards = []
        for state_reward_info in self.state_rewards_info:
            state_reward_weight = state_reward_info['Weight']
            state_reward_function = state_reward_info['Function']
            state_reward = state_reward_weight * state_reward_function(self, state)

            state_rewards.append((state_reward, state_reward_weight))
        return state_rewards
    
    def reward_data_completeness(self, state):
        reward = 0
        for visualisation in state.visualisations:
            reward += 1 - int(visualisation.itemLimitEnabled)
            # Already weighted less because of weights
        normalized_reward = reward / len(state.visualisations)
        return normalized_reward

    def reward_decluttering(self, state):
        reward = 0
        for visualisation in state.visualisations:
            reward += 0.5 * int(visualisation.itemLimitEnabled)
            reward += 0.5 * (0 if visualisation.dataItems <= visualisation.itemLimit else ((visualisation.dataItems - visualisation.itemLimit) / visualisation.dataItems))
            # The less items (the lower the item limit), the higher the reward
        normalized_reward = reward / len(state.visualisations)
        return normalized_reward
    
    def reward_appropriate_visualisation_types(self, state):
        reward = 0
        for visualisation in state.visualisations:
            visualisationType = visualisation.visualisationType
            dataItems = visualisation.dataItems
            if visualisationType in [VisualisationType.SINGLE]:
                if dataItems == 1:
                    reward += 1
            elif visualisationType in [VisualisationType.PROGRESS_BAR, VisualisationType.RADIAL_PROGRESS_BAR]:
                if dataItems == 1 or dataItems == 2:
                    reward += 1
            elif visualisationType in [VisualisationType.FRACTIONAL]:
                if dataItems == 2:
                    reward += 1
            elif visualisationType in [VisualisationType.PIE]: # Literature: 4, 5, 6
                if dataItems >= 3 and dataItems <= 6:
                    reward += 1 - (dataItems - 3) / 10
                    # (3 -> 1, 4 -> 0.9, 5 -> 0.8, 6 -> 0.7)
            elif visualisationType in [VisualisationType.BAR]: # Literature: 10, 12, 15
                if dataItems >= 3 and dataItems <= 6:
                    reward += 1 - (7 - dataItems) / 10
                    # (3 -> 0.6, 4 -> 0.7, 5 -> 0.8, 6 -> 0.9)
                elif dataItems >= 7 and dataItems <= 15:
                    reward += 1
            elif visualisationType in [VisualisationType.LINE]:
                if dataItems >= 3 and dataItems <= 6:
                    reward += 1 - (7 - dataItems) / 10
                    # (3 -> 0.6, 4 -> 0.7, 5 -> 0.8, 6 -> 0.9)
                elif dataItems >= 7 and dataItems <= 15:
                    reward += 0.9
                elif dataItems >= 16:
                    reward += 1
        normalized_reward = reward / len(state.visualisations)
        return normalized_reward

    def reward_valid_action(previous_dashboard, action):
        return 1

    def render(self):
        # No need to render visualisations
        pass


    ### MASKING
    def get_action_mask(self, visualisation_index):

        visualisation = self.dashboard.visualisations[visualisation_index]

        def valid_action(action):
            if action == RemoveItemLimit:
                return visualisation.itemLimitEnabled
            elif action == AddItemLimit:
                return not visualisation.itemLimitEnabled
            else:
                return True

        mask_list = [int(valid_action(action)) for action in ACTIONS]
        return torch.tensor(mask_list, dtype = float)
