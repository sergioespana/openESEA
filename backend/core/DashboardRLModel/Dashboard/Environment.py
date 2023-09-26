from .Classes import VisualisationType, Dashboard

from .Encoding import dashboardToArray

from .Information import MAX_DATA_ITEMS

from .Actions.Information import ACTIONS

import copy

class DashboardEnvironment:
    def __init__(self, dashboard: Dashboard):
        self.initial_dashboard: Dashboard = dashboard

        self.dashboard: Dashboard = copy.deepcopy(self.initial_dashboard)
        self.state = dashboardToArray(self.dashboard)

        self.rewards_info = [
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
        action_index = parameter_values[0]
        visualisation_index = parameter_values[1]
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
        flags = { 'Explanation': None }

        # Always keep going
        done = False

        # Return state and reward
        return self.state, reward, done, flags

    def reward(self, previous_dashboard, action):
        
        sum_of_reward_weights = 0
        reward = 0
        for reward_info in self.rewards_info:
            reward_weight = reward_info['Weight']
            reward_function = reward_info['Function']
            reward += reward_weight * reward_function(self, previous_dashboard, action)
            sum_of_reward_weights += reward_weight
        
        if sum_of_reward_weights == 0:
            return 0, None
        
        normalized_reward = reward / sum_of_reward_weights
        explanation = None

        return normalized_reward, explanation

    def reward_data_completeness(self, previous_dashboard, action):
        current_dashboard = self.dashboard
        reward = 0
        for visualisation in current_dashboard.visualisations:
            reward += 1 - int(visualisation.itemLimitEnabled)
            # Already weighted less because of weights
        normalized_reward = reward / len(current_dashboard.visualisations)
        return normalized_reward

    def reward_decluttering(self, previous_dashboard, action):
        current_dashboard = self.dashboard
        reward = 0
        for visualisation in current_dashboard.visualisations:
            reward += 1 - visualisation.dataItems / MAX_DATA_ITEMS
            # The less items, the higher reward
        normalized_reward = reward / len(current_dashboard.visualisations)
        return normalized_reward
    
    def reward_appropriate_visualisation_types(self, previous_dashboard, action):
        current_dashboard = self.dashboard
        reward = 0
        for visualisation in current_dashboard.visualisations:
            if visualisation.visualisationType in [VisualisationType.SINGLE]:
                if visualisation.dataItems == 1:
                    reward += 1
            elif visualisation.visualisationType in [VisualisationType.PROGRESS_BAR, VisualisationType.RADIAL_PROGRESS_BAR]:
                if visualisation.dataItems == 1 or visualisation.dataItems == 2:
                    reward += 1
            elif visualisation.visualisationType in [VisualisationType.FRACTIONAL]:
                if visualisation.dataItems == 2:
                    reward += 1
            elif visualisation.visualisationType in [VisualisationType.PIE]:
                if visualisation.dataItems >= 3 and visualisation.dataItems <= 8:
                    reward += 1 - (visualisation.dataItems - 3) / 10
                    # (3 -> 1, 4 -> 0.9, ..., 8 -> 0.5)
            elif visualisation.visualisationType in [VisualisationType.BAR]:
                if visualisation.dataItems >= 3:
                    reward += 1
            elif visualisation.visualisationType in [VisualisationType.LINE]:
                if visualisation.dataItems >= 3:
                    reward += 1
        normalized_reward = reward / len(current_dashboard.visualisations)
        return normalized_reward

    def render(self):
        # No need to render visualisations
        pass
