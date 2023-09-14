from .AgentNetwork.AgentNetwork import AgentNetwork

from .Dashboard.Classes import Dashboard
from .Dashboard.Environment import DashboardEnvironment

from .Dashboard.Encoding import dashboardToArray
from .Dashboard.Parser import parseDashboard

from .Dashboard.Actions.Information import ACTIONS_PARAMETERS, NUM_ACTIONS

class DashboardRLModel:
    def __init__(self, visualisations):
        print(visualisations)

        # Create dashboard object from visualisations info and encode into array
        dashboard: Dashboard = parseDashboard(visualisations)
        dashboardArray = dashboardToArray(dashboard)

        # Determine the different sizes for the agent network
        num_visualisations = len(dashboard.visualisations)
        num_inputs = len(dashboardArray)
        num_hidden = num_inputs
        num_actions = NUM_ACTIONS
        num_params_list = ACTIONS_PARAMETERS

        # Create the agent network
        self.agent_network = AgentNetwork(num_inputs, num_hidden, num_actions, num_visualisations, num_params_list)
        # Create the dashboard environment
        self.dashboard_environment = DashboardEnvironment(dashboard)

        # Initialize running reward
        self.running_reward = 10

        # Set parameters
        self.num_episodes = None # 100
        self.num_time_steps = 1000 # 10000
        self.render = False

        # Set control variables
        self.stop = False

        # Set best actions
        self.best_actions = []

    def run(self):
        # Set initial episode number
        episode_number = 0
        # Run until model is stopped or num_episodes is reached
        while True:
            # Run episode
            self.run_episode(episode_number)
            # Increment episode number for next run
            episode_number += 1

        # If model is stopped, return from running loop
            if self.stop: return
        # Run indefinetely or for num_episodes
            if self.num_episodes is not None and episode_number >= self.num_episodes: return

    def kill(self):
        self.stop = True

    def run_episode(self, episode_number):

        # Reset the state of the environment for this episode
        state = self.dashboard_environment.initial()

        # Initialise the episode reward to 0
        episode_reward = 0

        # For each episode, run a trajectory for `num_time_steps` time steps
        for t in range(0, self.num_time_steps):

            # Select/Sample an action from the agent network following the agent's policy
            outputs = self.agent_network.output_parameter_values(state)

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
        print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(episode_number, episode_reward, self.running_reward))

        # Get best actions every 2 episodes
        if episode_number % 2 == 0:
            self.best_actions = self.predict()


    def predict(self):
        # Initialize starting environment
        start_environment = self.dashboard_environment.initial()
        # Select an (/the current best) action through the agent network
        outputs = self.agent_network.forward_collect(start_environment)
        # Convert parameter from tensors to simple values
        parameter_values = [output.item() for output in outputs]
        # Construct the action from the model outputs
        action = self.dashboard_environment.action_from_parameters(parameter_values)
        actions = [action]

        # Return actions
        return actions

def main():
    model = DashboardRLModel()
    print('Running...')
    model.run()
    print(model.predict())

if __name__ == '__main__':
    main()
