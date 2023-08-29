from Dashboard.Classes import Dashboard
from Dashboard.Environment import DashboardEnvironment

from Dashboard.Encoding import dashboardToArray
from Dashboard.Parser import parseDashboard

from Dashboard.Actions.Information import ACTIONS_PARAMETERS, NUM_ACTIONS

from AgentNetwork.AgentNetwork import AgentNetwork

class DashboardRLModel:
    def __init__(self):
        visualisations = [
            {
                'Item Limit Enabled': True,
                'Visualisation Type': 'Bar',
                'Item Limit': 40,
                'Data Items': 128
            },
            {
                'Item Limit Enabled': False,
                'Visualisation Type': 'Pie',
                'Item Limit': 10,
                'Data Items': 40
            },
            {
                'Item Limit Enabled': False,
                'Visualisation Type': 'Line',
                'Item Limit': 0,
                'Data Items': 30
            },
            {
                'Item Limit Enabled': False,
                'Visualisation Type': 'Line',
                'Item Limit': 0,
                'Data Items': 40
            }
        ]
        visualisations = visualisations * 1 # 30
        visualisations = [{
                'Item Limit Enabled': False,
                'Visualisation Type': 'Pie',
                'Data Items': i * 4
            } for i in range(0, 20)]

        dashboard: Dashboard = parseDashboard(visualisations)
        dashboardArray = dashboardToArray(dashboard)

        num_inputs = len(dashboardArray)
        num_hidden = num_inputs * 2
        num_actions = NUM_ACTIONS
        num_visualisations = len(dashboard.visualisations)
        num_params_list = ACTIONS_PARAMETERS

        # Create the agent network
        self.agent_network = AgentNetwork(num_inputs, num_hidden, num_actions, num_visualisations, num_params_list)
        # Create the dashboard environment
        self.dashboard_environment = DashboardEnvironment(dashboard)

        self.running_reward = 10

        self.num_episodes = 100
        self.num_time_steps = 10000
        self.render = False

    def run(self):

        # Run for `num_episodes` amount of episodes
        for episode_number in range(0, self.num_episodes):

            # Initialise the episode reward to 0
            episode_reward = 0

            # Reset the state of the environment for this episode
            state = self.dashboard_environment.initial()

            # For each episode, run a trajectory for `num_time_steps` time steps
            for t in range(0, self.num_time_steps):

                # Select/Sample an action from the agent network following the agent's policy
                outputs = self.agent_network.output_parameters_values(state)

                # Execute the action on the environment
                state, reward, done = self.dashboard_environment.step(outputs)

                # Save reward for updating gradient after episode 
                self.agent_network.rewards.append(reward)
                # Keep track of episode reward
                episode_reward += reward

                # If wanted, render the updated environment
                if self.render: self.dashboard_environment.render()

                # If the environment is in a final state, stop this episode
                if done: break

            # Update the running reward over the episodes
            self.running_reward = 0.05 * episode_reward + (1 - 0.05) * self.running_reward

            # Update the agent network based on the accumulated rewards and losses
            self.agent_network.update_network_gradients()

            # Print the episode reward and running episode reward
            if episode_number % 1 == 0:
                print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(episode_number, episode_reward, self.running_reward))

            # check if we have "solved" the cart pole problem
            if self.running_reward > 300 and False:
                print("Solved! Running reward is now {} and the last episode runs to {} time steps!".format(self.running_reward, t))
                break

            print(self.predict())
            # return
        # Temp return to not loop infinitely

    def predict(self):
        # Initialize starting environment
        start_environment = self.dashboard_environment.initial()
        # Select an (/the current best) action through the agent network
        outputs = self.agent_network.output_parameters_values(start_environment)
        # Convert parameter from tensors to simple values
        parameter_values = [output.item() for output in outputs]
        # Construct the action from the model outputs
        action = self.dashboard_environment.action_from_parameters(parameter_values)
        # Return action
        return action

def main():
    model = DashboardRLModel()
    model.run()
    # print(model.predict())

if __name__ == '__main__':
    main()
