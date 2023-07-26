from Dashboard.Classes import Dashboard
from Dashboard.Environment import DashboardEnvironment

from Dashboard.Encoding import dashboardToArray
from Dashboard.Parser import parseDashboard

from AgentNetwork.AgentNetwork import AgentNetwork

from Actions.Information import ACTIONS_PARAMETERS, NUM_ACTIONS

def main():

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
    agent_network = AgentNetwork(num_inputs, num_hidden, num_actions, num_visualisations, num_params_list)
    # Create the dashboard environment
    dashboard_environment = DashboardEnvironment(dashboard)

    running_reward = 10

    num_episodes = 100
    num_time_steps = 10000
    render = False

    # Run for `num_episodes` amount of episodes
    for episode_number in range(0, num_episodes):

        # Initialise the episode reward to 0
        episode_reward = 0

        # Reset the state of the environment for this episode
        state = dashboard_environment.reset()

        # For each episode, run a trajectory for `num_time_steps` time steps
        for t in range(0, num_time_steps):

            # Select/Sample an action from the agent network following the agent's policy
            action = agent_network.select_action(state)

            # Execute the action on the environment
            state, reward, done = dashboard_environment.step(action)

            # Save reward for updating gradient after episode 
            agent_network.rewards.append(reward)
            # Keep track of episode reward
            episode_reward += reward
            
            # If wanted, render the updated environment
            if render: dashboard_environment.render()

            # If the environment is in a final state, stop this episode
            if done: break

        # Update the running reward over the episodes
        running_reward = 0.05 * episode_reward + (1 - 0.05) * running_reward

        # Update the agent network based on the accumulated rewards and losses
        agent_network.update_network_gradients()

        # Print the episode reward and running episode reward
        if episode_number % 1 == 0:
            print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(episode_number, episode_reward, running_reward))

        # check if we have "solved" the cart pole problem
        if running_reward > 300 and False:
            print("Solved! Running reward is now {} and the last episode runs to {} time steps!".format(running_reward, t))
            break

        action = agent_network.select_action(dashboard_environment.reset())
        print(action)

if __name__ == '__main__':
    main()