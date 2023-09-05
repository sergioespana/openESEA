from .AgentNetwork.AgentNetwork import AgentNetwork

from .Dashboard.Classes import Dashboard
from .Dashboard.Environment import DashboardEnvironment

from .Dashboard.Encoding import dashboardToArray
from .Dashboard.Parser import parseDashboard

from .Dashboard.Actions.Information import ACTIONS_PARAMETERS, NUM_ACTIONS

from datetime import datetime, timedelta
import time

class DashboardRLModel:
    def __init__(self, visualisations):
        visualisations = visualisations
        print('-------------------------------')
        print('-------------------------------')
        print('-------------------------------')
        print(visualisations)
        print('-------------------------------')
        print('-------------------------------')
        print('-------------------------------')
        # visualisations = [
        #     {
        #         'Item Limit Enabled': True,
        #         'Visualisation Type': 'Bar',
        #         'Item Limit': 40,
        #         'Data Items': 128
        #     },
        #     {
        #         'Item Limit Enabled': False,
        #         'Visualisation Type': 'Pie',
        #         'Item Limit': 10,
        #         'Data Items': 40
        #     },
        #     {
        #         'Item Limit Enabled': False,
        #         'Visualisation Type': 'Line',
        #         'Item Limit': 0,
        #         'Data Items': 30
        #     },
        #     {
        #         'Item Limit Enabled': False,
        #         'Visualisation Type': 'Line',
        #         'Item Limit': 0,
        #         'Data Items': 40
        #     }
        # ]
        # visualisations = visualisations * 1 # 30
        # visualisations = [{
        #         'Item Limit Enabled': False,
        #         'Visualisation Type': 'Pie',
        #         'Data Items': i * 4
        #     } for i in range(0, 20)]

        dashboard: Dashboard = parseDashboard(visualisations)
        dashboardArray = dashboardToArray(dashboard)

        num_inputs = len(dashboardArray)
        num_hidden = num_inputs
        num_actions = NUM_ACTIONS
        num_visualisations = len(dashboard.visualisations)
        num_params_list = ACTIONS_PARAMETERS

        # Create the agent network
        self.agent_network = AgentNetwork(num_inputs, num_hidden, num_actions, num_visualisations, num_params_list)
        # Create the dashboard environment
        self.dashboard_environment = DashboardEnvironment(dashboard)

        self.running_reward = 10

        self.num_episodes = None # 100
        self.num_time_steps = 1000 # 10000
        self.render = False
        self.updating = True # to lock predicting at first
        self.predicting = False

        self.stop = False
        self.setLastRequestTime()

    def run(self):
        print('running')
        episode_number = 0
        while True:
            print('episode: ' + str(episode_number))
            self.run_episode(episode_number)
            print('episode finished')
            episode_number += 1

        # Run for num_episodes, otherwise run indefinetely
            if self.num_episodes is not None and episode_number >= self.num_episodes: return
        # If model is stopped, return
            if self.stop: return
        # If model is inactive, return
            if self.inactive(): return

    def kill(self):
        self.stop = True

    def setLastRequestTime(self):
        self.lastRequestTime = datetime.now()
    
    # After 1 minute of no request, set model to inactive, to stop running the model
    def inactive(self):
        currentTime = datetime.now()
        timeSinceLastRequest = currentTime - self.lastRequestTime

        if timeSinceLastRequest >= timedelta(minutes = 1):
            return True
        return False

    def run_episode(self, episode_number):

        # Reset the state of the environment for this episode
        state = self.dashboard_environment.initial()

        # Initialise the episode reward to 0
        episode_reward = 0

        # For each episode, run a trajectory for `num_time_steps` time steps
        for t in range(0, self.num_time_steps):

            # Select/Sample an action from the agent network following the agent's policy
            outputs = self.agent_network.output_parameter_values(state, sampling = True)

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
        print('updating gradients')
        while self.predicting:
            time.sleep(0.5)
            pass
        print('really updating gradients')
        self.updating = True
        self.agent_network.update_network_gradients()
        self.updating = False
        print('done updating gradients')

        # Print the episode reward and running episode reward
        if episode_number % 1 == 0:
            print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(episode_number, episode_reward, self.running_reward))

        # check if we the reward is above some threshold
        # if self.running_reward > 300:
        #     print("Solved! Running reward is now {} and the last episode runs to {} time steps!".format(self.running_reward, t))
        #     return

    def predict(self):
        # Initialize starting environment
        start_environment = self.dashboard_environment.initial()
        # Select an (/the current best) action through the agent network
        while self.updating:
            time.sleep(0.5)
            pass
        self.predicting = True
        outputs = self.agent_network.output_parameter_values(start_environment, sampling = False)
        self.predicting = False
        # Convert parameter from tensors to simple values
        parameter_values = [output.item() for output in outputs]
        # Construct the action from the model outputs
        action = self.dashboard_environment.action_from_parameters(parameter_values)

        self.setLastRequestTime()
        # Return action
        return action

def main():
    model = DashboardRLModel()
    print('Running...')
    model.run()
    print(model.predict())

if __name__ == '__main__':
    main()
