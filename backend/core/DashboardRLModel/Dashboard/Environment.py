from .Classes import VisualisationType, Dashboard, Visualisation

from .Encoding import dashboardToArray

from .Information import MAX_DATA_ITEMS, MAX_ITEM_LIMIT, NUM_VISUALISATION_TYPES

from .Actions.Information import ACTIONS, ACTIONS_PARAMETERS
from .Actions.Classes import *

import copy

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
                'Name': 'Chart Variety',
                'Weight': 0.5,
                'Function': DashboardEnvironment.reward_visualisation_variety
            },
            {
                'Name': 'Data Completeness',
                'Weight': 0.2,
                'Function': DashboardEnvironment.reward_data_completeness
            },
            {
                'Name': 'Appropriate Visualisation Types',
                'Weight': 0.8,
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
        self.dashboard = copy.deepcopy(self.initial_dashboard)

        # Perform the action on the dashboard
        action.act(self.dashboard)

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
                explanation += "\t" + self.state_rewards_info[i].get("Name", "Reward " + str(i)) + "\t" + "Reward difference: " + str(c_reward - p_reward) + "\t" + "Weighted: " + str(c_reward_weight * (c_reward - p_reward)) + "\n"
        # print(explanation)
        return normalized_reward, explanation

    def collect_state_rewards(self, state):
        state_rewards = []
        for state_reward_info in self.state_rewards_info:
            state_reward_function = state_reward_info.get('Function')
            if state_reward_function is None: continue
            state_reward_weight = state_reward_info.get('Weight', 1)
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

    def reward_visualisation_variety(self, state):
        chart_types = set()
        for visualisation in state.visualisations:
            visualisation: Visualisation = visualisation
            chart_types.add(visualisation.visualisationType)
        if len(chart_types) == 1:
            return 0.8
        elif len(chart_types) == 2:
            return 0.9
        elif len(chart_types) == 3:
            return 1
        elif len(chart_types) == 4:
            return 1
        elif len(chart_types) == 5:
            return 0.8
        elif len(chart_types) == 6:
            return 0.6
        elif len(chart_types) == 7:
            return 0.3
        elif len(chart_types) == 8:
            return 0.2
        elif len(chart_types) == 9:
            return 0.1
        return 0.05

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
                # Visualisation groups
                progressBarVisualisations = [VisualisationType.PROGRESS_BAR, VisualisationType.RADIAL_PROGRESS_BAR]
                fractionalVisualisations = [VisualisationType.FRACTIONAL] + progressBarVisualisations
                visualisation_type = visualisation.visualisationType
                if visualisation_type == VisualisationType.SINGLE:
                    return False
                if visualisation_type in fractionalVisualisations:
                    return False
                # For all other visualisations:
                return not visualisation.itemLimitEnabled
            else:
                return True

        return [int(valid_action(action)) for action in ACTIONS]
    
    def get_parameter_mask(self, visualisation_index, action_index, sampled_params, param_index):
        visualisation = self.dashboard.visualisations[visualisation_index]
        action = ACTIONS[action_index]
        # print(visualisation_index, action_index, param_index, ACTIONS_PARAMETERS)
        param_values = ACTIONS_PARAMETERS[action_index][param_index]['Values']

        # Visualisation groups
        progressBarVisualisations = [VisualisationType.PROGRESS_BAR, VisualisationType.RADIAL_PROGRESS_BAR]
        fractionalVisualisations = [VisualisationType.FRACTIONAL] + progressBarVisualisations
        categoricalVisualisations = [VisualisationType.PIE, VisualisationType.BAR]
        groupedBarVisualisations = [VisualisationType.GROUPED_BAR, VisualisationType.STACKED_BAR]
        temporalVisualisations = [VisualisationType.LINE]

        # Should not be reached, since there are no parameters
        if action == RemoveItemLimit:
            return None
        # Item limit up to data_items and starting from 2
        elif action == AddItemLimit:
            data_items = visualisation.dataItems
            max_values = param_values
            return [0 if value < 2 or value > data_items else 1 for value in range(max_values)]
        # Visualisation type which is possible
        if action == ChangeVisualisationType:
            visualisation_type = visualisation.visualisationType
            data_items = visualisation.dataItems
            def valid_change(newType):
                # Discourage changing to existing type
                if visualisation_type == newType:
                    return 0.01
                # Single to single
                if visualisation_type == VisualisationType.SINGLE:
                    return newType == VisualisationType.SINGLE
                    # or if percentage -> progress bar
                # Fractional to fractional/progress_bars or pie
                if visualisation_type == VisualisationType.FRACTIONAL:
                    return newType in fractionalVisualisations or newType == VisualisationType.PIE
                # Progress bars to progress bars or if 1 item -> single, 2 items -> fractional/pie
                if visualisation_type in progressBarVisualisations:
                    if data_items == 1:
                        return newType in progressBarVisualisations or newType == VisualisationType.SINGLE
                    return newType in fractionalVisualisations or newType == VisualisationType.PIE
                # Categorical to categorical/table or if 1 item -> single
                if visualisation_type in categoricalVisualisations:
                    if newType in categoricalVisualisations or newType == VisualisationType.TABLE:
                        return True
                    if data_items == 1:
                        return newType == VisualisationType.SINGLE
                # Grouped/stacked bar to grouped/stacked bar or table
                if visualisation in groupedBarVisualisations:
                    if newType in groupedBarVisualisations or newType == VisualisationType.TABLE:
                        return True
                # Line to categorical/temporal/table or if 1 item -> single
                if visualisation_type == VisualisationType.LINE:
                    if newType in categoricalVisualisations or newType in temporalVisualisations or newType == VisualisationType.TABLE:
                        return True
                    if data_items == 1:
                        return newType == VisualisationType.SINGLE
                # Multi series line
                if visualisation_type == VisualisationType.MULTI_SERIES_LINE:
                    if newType == VisualisationType.MULTI_SERIES_LINE or newType == VisualisationType.TABLE:
                        return True
                # Table
                ### table to grouped bar or others if fields correspond
                if visualisation_type == VisualisationType.TABLE:
                    if newType == VisualisationType.TABLE:
                        return True
                return False
            return [int(valid_change(visualisation_type.value)) for visualisation_type in VisualisationType]
