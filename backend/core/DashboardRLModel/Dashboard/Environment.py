from .Classes import VisualisationType, Dashboard

from .Encoding import dashboardToArray

from .Information import MAX_DATA_ITEMS

from .Actions.Information import ACTIONS


class DashboardEnvironment:
    def __init__(self, dashboard: Dashboard):
        self.initial_dashboard: Dashboard = dashboard

        self.dashboard: Dashboard = self.initial_dashboard
        self.state = dashboardToArray(self.dashboard)

    def initial(self):
        return dashboardToArray(self.initial_dashboard)
    # Item limit in segments of 5
    # Item limit must not be larger than amount of data items
    def action_from_parameters(self, parameter_values):
        # Determine action, visualisation index and other parameters
        action_index = parameter_values[0]
        visualisation_index = parameter_values[1]
        other_parameters = parameter_values[2:]

        # Construct the action from the parameters
        action = ACTIONS[action_index](visualisation_index, *other_parameters)

        return action

    def step(self, outputs):
        # Convert parameter from tensors to simple values
        parameter_values = [output.item() for output in outputs]
        
        # Construct the action from the model outputs
        action = self.action_from_parameters(parameter_values)

        # Perform the action
        action.act(self.dashboard)

        # Update state from acted on visualisations object
        self.state = dashboardToArray(self.dashboard)

        # Determine reward for this step
        reward = self.reward(action)

        # Always keep going
        done = False

        # Return state and reward
        return self.state, reward, done

    def reward(self, action):
        
        less_items_reward = 0
        all_values_shown_reward = 0
        correct_visualisation_type_reward = 0
        for visualisation in self.dashboard.visualisations:

            all_values_shown_reward += (1 - int(visualisation.itemLimitEnabled)) / 10

            less_items_reward += 1 - visualisation.dataItems / MAX_DATA_ITEMS

            if visualisation.visualisationType == VisualisationType.PIE:
                if visualisation.dataItems >= 6:
                    correct_visualisation_type_reward = 0
                elif visualisation.dataItems >= 1:
                    correct_visualisation_type_reward = (6 - visualisation.dataItems) / 5
            elif visualisation.visualisationType == VisualisationType.BAR:
                if visualisation.dataItems < 3:
                    correct_visualisation_type_reward = 0
                else:
                    correct_visualisation_type_reward = 1
            elif visualisation.visualisationType == VisualisationType.LINE:
                if visualisation.dataItems < 6:
                    correct_visualisation_type_reward = 0
                else:
                    correct_visualisation_type_reward = 1


        total_reward = less_items_reward + all_values_shown_reward + correct_visualisation_type_reward
        reward = total_reward / (3 * len(self.dashboard.visualisations)) # Divide by the amount of visualisations and different rewards
        return reward

    def render(self):
        # No need to render visualisations
        pass
