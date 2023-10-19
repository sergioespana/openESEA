from .AgentNetwork.AgentNetwork import AgentNetwork

from .Dashboard.Classes import Dashboard
from .Dashboard.Environment import DashboardEnvironment

from .Dashboard.Encoding import dashboardToArray
from .Dashboard.Parser import parseDashboard, VISUALISATION_NAME_MAPPING

from .Dashboard.Actions.Information import ACTIONS_PARAMETERS, NUM_ACTIONS

from .AgentNetwork.AgentNetwork import ForwardPass

import torch

class DashboardRLModel:
    def __init__(self, dashboard):
        # print(visualisations)
        self.original_dashboard = dashboard

        # Create dashboard object from visualisations info and encode into array
        dashboard: Dashboard = parseDashboard(dashboard)
        dashboardArray = dashboardToArray(dashboard)

        # Determine the different sizes for the agent network
        num_visualisations = len(dashboard.visualisations)
        num_inputs = len(dashboardArray)
        num_hidden = num_inputs
        num_actions = NUM_ACTIONS
        num_params_list = ACTIONS_PARAMETERS

        # Create the dashboard environment
        self.dashboard_environment = DashboardEnvironment(dashboard)
        # Create the agent network
        self.agent_network = AgentNetwork(num_inputs, num_hidden, num_actions, num_visualisations, num_params_list, self.dashboard_environment)

        # Initialize running reward
        self.running_reward = 10

        # Set parameters
        self.num_episodes = None # 100
        self.num_time_steps = 200 # 10000
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
        sampled_actions = 0
        t = 0
        while True:
            t += 1
            # Select/Sample an action from the agent network following the agent's policy
            outputs, saved_action = self.agent_network.output_parameter_values(state)
            if outputs is None:
                continue # retry, consuming a time step
            else:
                sampled_actions += 1

            # Execute the action on the environment
            state, reward, done, flags = self.dashboard_environment.step(outputs)

            # Save action
            self.agent_network.saved_actions.append(saved_action)
            # Save reward for updating gradient after episode 
            self.agent_network.rewards.append(reward)
            # Keep track of episode reward
            episode_reward += reward

            # If wanted, render the updated environment
            if self.render: self.dashboard_environment.render()

            # If the environment is in a final state, stop this episode
            if done: break

            # Stop if we reached the final time step and have minimal success, otherwise continue
            if t >= self.num_time_steps and sampled_actions > self.num_time_steps / 10:
                break


        # Reset the state of the environment for the user actions
        state = self.dashboard_environment.initial()
        # List of actions with user feedback (+1/-1)
        user_actions = [] # [([torch.tensor(6), torch.tensor(2)], 1)]
        for action, reward in user_actions:
            # Emulate selection of this action
            outputs, saved_action = self.agent_network.emulate_output_parameter_values(state, action)
            # => No need to get reward from outputs
            # Store reward and action in agent network
            self.agent_network.user_rewards.append(reward)
            self.agent_network.saved_user_actions.append(saved_action)
        
        episode_reward = episode_reward if sampled_actions == 0 else episode_reward * self.num_time_steps / sampled_actions
        # Update the running reward over the episodes
        self.running_reward = 0.05 * episode_reward + (1 - 0.05) * self.running_reward

        # Update the agent network based on the accumulated rewards and losses
        self.agent_network.update_network_gradients()

        # Print the episode reward and running episode reward
        print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(episode_number, episode_reward, self.running_reward))

        # Get best actions every 2 episodes
        if episode_number % 1 == 0:
            self.best_actions = self.predict()


    def predict(self):
        # Initialize starting environment
        start_environment = self.dashboard_environment.initial()
        # Select an (/the current best) action through the agent network
        while True:    
            outputs_list = self.agent_network(ForwardPass.PREDICT, start_environment)
            if outputs_list is not None: break

        # Convert parameter from tensors to simple values
        actions_values = [[output.item() for output in outputs] for outputs in outputs_list]

        # Construct the action from the model outputs
        actions = [self.dashboard_environment.action_from_parameters(action_values) for action_values in actions_values]

        # Add reward + flags (etc.) to this action
        actions_info = [(action, self.dashboard_environment.perform_action_on_initial(action)) for action in actions] # [(state, reward, done, flags)]

        # Return actions
        actions_with_explanations = []
        for action_info in actions_info:
            action, state = action_info
            new_state, reward, done, flags = state
            explanation = flags.get('Explanation', '')

            visualisationIndex = action.visualisationIndex
            visualisationInfo = self.original_dashboard['Visualisations'][visualisationIndex]

            # print(self.original_dashboard)
            # print(visualisationIndex)
            # print(visualisationInfo)
            # print(action.to_dict())
            # input()

            actionInfo = action.to_dict()
            actionInfo['Explanation'] = explanation
            if actionInfo.get('Visualisation Type') is not None: actionInfo['Visualisation Type'] = VISUALISATION_NAME_MAPPING[actionInfo['Visualisation Type']]
            actionInfo['Visualisation Title'] = visualisationInfo['Visualisation Title']
            actionInfo['Selection Configuration'] = visualisationInfo['Selection Configuration']
            
            actions_with_explanations.append(actionInfo)
        return actions_with_explanations
