from enum import IntEnum

from dataclasses import dataclass
from collections import deque
from typing import List, Dict

import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

#region Encoding and decoding different values into/from arrays
def encode_categorical(integer_value, num_categories):
    # Initialize zero-valued array for all categories
    array = np.zeros(num_categories, dtype=int)
    # Set category corresponding to given integer to 1
    array[integer_value] = 1
    # Return one hot array
    return array
def encode_boolean(boolean_value):
    # Convert to integer value
    value = int(boolean_value)
    # Return array with value
    return np.array([value])
def encode_and_normalise_value(integer_value, max_value):
    # Normalise value
    value = integer_value / max_value
    # Ensure that value is between 0 and 1
    value = max(0, min(1, value))
    # Return array with value
    return np.array([value])

def decode_categorical(array, offset, num_categories):
    # Get index where one hot array is one for the amount of categories
    return np.argmax(array[offset : offset + num_categories])
def decode_boolean(array, offset):
    # Get integer value from array
    integer_value = array[offset : offset + 1]
    # Cast back to boolean value
    boolean_value = bool(integer_value)
    # Return boolean value
    return boolean_value
def decode_normalised_value(array, offset, max_value):
    # Get normalised value from array
    value = array[offset : offset + 1]
    # Multiply and round back to original value
    original_value = round(max_value * value)
    # Return original value
    return original_value
#endregion

# Visualisation Types, length and mapping from names
class VisualisationType(IntEnum):
    PIE  = 0
    BAR  = 1
    LINE = 2
NUM_VISUALISATION_TYPES: int = len(VisualisationType)
VISUALISATION_TYPE_MAPPING: Dict[str, VisualisationType] = {
    'Pie': VisualisationType.PIE,
    'Bar': VisualisationType.BAR,
    'Line': VisualisationType.LINE
}

# Information about limits for variables
MAX_ITEM_LIMIT: int = 50
MAX_DATA_ITEMS: int = 250

#region Visualisation classes including mapping to arrays
@dataclass
class Visualisation:
    visualisationType: VisualisationType

    itemLimitEnabled: bool

    itemLimitLarge: bool
    itemLimit: int

    manyDataItems: bool
    dataItems: int

    def toArray(self):
        total_array = np.array([])
        
        array = encode_categorical(int(self.visualisationType), NUM_VISUALISATION_TYPES)
        total_array = np.append(total_array, array) 
        
        array = encode_boolean(self.itemLimitEnabled)
        total_array = np.append(total_array, array) 

        array = encode_boolean(self.itemLimitLarge)
        total_array = np.append(total_array, array) 

        array = encode_and_normalise_value(self.itemLimit, MAX_ITEM_LIMIT)
        total_array = np.append(total_array, array) 

        array = encode_boolean(self.manyDataItems)
        total_array = np.append(total_array, array) 

        array = encode_and_normalise_value(self.dataItems, MAX_DATA_ITEMS)
        total_array = np.append(total_array, array) 
        
        return total_array
@dataclass
class Visualisations:
    visualisations: List[Visualisation]

    def toArray(self):
        array = np.array([])
        for visualisation in self.visualisations:
            array = np.append(array, visualisation.toArray())
        return array
#endregion

#region Mapping from arrays to visualisations
def visualisationFromArray(array):
    offset = 0

    visualisationType = VisualisationType(decode_categorical(array, offset, len(VisualisationType)))
    offset += len(VisualisationType)

    itemLimitEnabled = decode_boolean(array, offset)
    offset += 1

    itemLimitLarge = decode_boolean(array, offset)
    offset += 1

    itemLimit = decode_normalised_value(array, offset, MAX_ITEM_LIMIT)
    offset += 1

    manyDataItems = decode_boolean(array, offset)
    offset += 1

    dataItems = decode_normalised_value(array, offset, MAX_DATA_ITEMS)
    offset += 1

    return Visualisation(visualisationType, itemLimitEnabled, itemLimitLarge, itemLimit, manyDataItems, dataItems)
def visualisationsFromArray(array):
    visualisationSize = len(VisualisationType) + 1 + 1 + 1 + 1 + 1
    arraySize = len(array)
    visualisations = []
    nr_of_visualisations = arraySize // visualisationSize
    for i in range(0, nr_of_visualisations):
        visualisationArray = array[i * visualisationSize : (i + 1) * visualisationSize]
        visualisations.append(visualisationFromArray(visualisationArray))
    return Visualisations(visualisations)
#endregion

#region Initialization of visualisations from objects
def parseVisualisation(visualisation) -> Visualisation:
    # Get visualisation type and lookup enum value
    visualisationTypeString = visualisation['Visualisation Type']
    visualisationType = VISUALISATION_TYPE_MAPPING[visualisationTypeString]

    # Get config -> if item limit is enabled
    itemLimitEnabled = visualisation['Item Limit Enabled']

    # Get item limit
    itemLimit = visualisation.get('Item Limit', 0)
    itemLimitLarge = itemLimit >= MAX_ITEM_LIMIT
    if itemLimitLarge: itemLimit = MAX_ITEM_LIMIT

    # Get amount of data items
    dataItems = visualisation['Data Items']
    manyDataItems = dataItems >= MAX_DATA_ITEMS
    if manyDataItems: dataItems = MAX_DATA_ITEMS

    return Visualisation(visualisationType, itemLimitEnabled, itemLimitLarge, itemLimit, manyDataItems, dataItems)
def parseVisualisations(visualisations) -> Visualisations:
    return Visualisations([parseVisualisation(visualisation) for visualisation in visualisations])
#endregion

#region Actions
@dataclass
class ChangeVisualisationType:
    visualisationIndex: int
    visualisationType: int

    def act(self, visualisations: Visualisations):
        visualisations.visualisations[self.visualisationIndex].visualisationType = VisualisationType(self.visualisationType)
@dataclass
class RemoveItemLimit:
    visualisationIndex: int

    def act(self, visualisations: Visualisations):
        visualisations.visualisations[self.visualisationIndex].itemLimitEnabled = False
        visualisations.visualisations[self.visualisationIndex].itemLimit = 0
@dataclass
class AddItemLimit:
    visualisationIndex: int
    itemLimit: int

    def act(self, visualisations: Visualisations):
        visualisations.visualisations[self.visualisationIndex].itemLimitEnabled = True
        visualisations.visualisations[self.visualisationIndex].itemLimit = self.itemLimit
#endregion

# Action information + parameters
ACTION_INFORMATION_LIST = [
    {
        'Action': AddItemLimit,
        'Parameters': [{ 'values': MAX_ITEM_LIMIT, 'type': 'numerical' }]
    },
    {
        'Action': RemoveItemLimit,
        'Parameters': []
    },
    {
        'Action': ChangeVisualisationType,
        'Parameters': [{ 'values': NUM_VISUALISATION_TYPES, 'type': 'categorical' }]
    }
]
ACTION_LIST        = [action_information['Action']     for action_information in ACTION_INFORMATION_LIST]
ACTION_PARAMS_LIST = [action_information['Parameters'] for action_information in ACTION_INFORMATION_LIST] #  for example [[{8, 'numerical'}], [], [{4, 'categorical'}]]
NUM_ACTIONS        = len(ACTION_INFORMATION_LIST)

# Functions for categorical variables
def sample_categorical(value_probabilities):
    dist = Categorical(value_probabilities)
    value = dist.sample()
    log_prob = dist.log_prob(value)
    return value, log_prob
def one_hot_encode_categorical(value_probabilities, sampled_value):
    num_values = value_probabilities.size(dim = 0)
    one_hot_encoded_value = F.one_hot(sampled_value, num_classes = num_values)
    return one_hot_encoded_value

class VisualisationsEnvironment:
    def __init__(self, visualisations: Visualisations):
        self.visualisations: Visualisations = visualisations
        self.initial_visualisations = self.visualisations
        self.state = visualisations.toArray()

    def reset(self):
        return self.initial_visualisations.toArray()

    def step(self, parameters):
        # Convert parameter from tensors to simple values
        parameter_values = [parameter.item() for parameter in parameters]

        # Determine action, visualisation index and other parameters
        action_index = parameter_values[0]
        visualisation_index = parameter_values[1]
        other_parameters = parameter_values[2:]

        # Construct the action from the parameters
        action = ACTION_LIST[action_index](visualisation_index, *other_parameters)

        # Perform the action
        action.act(self.visualisations)

        # Update state from acted on visualisations object
        self.state = self.visualisations.toArray()

        # Determine reward for this step
        reward = self.reward(action)

        # Always keep going
        done = False

        # Return state and reward
        return self.state, reward, done, None

    def reward(self, action):
        
        less_items_reward = 0
        all_values_shown_reward = 0
        correct_visualisation_type_reward = 0
        for visualisation in self.visualisations.visualisations:

            all_values_shown_reward += 1 - int(visualisation.itemLimitEnabled)

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
        reward = total_reward / (3 * len(self.visualisations.visualisations)) # Divide by the amount of visualisations and different rewards
        return reward

    def render(self):
        # No need to render visualisations
        pass

class AgentNetwork(nn.Module):
    def __init__(self, num_inputs: int, num_hidden: int, num_actions: int, num_visualisations: int, list_of_param_lists: List[List[int]]):
        # Initialise base nn.Module class
        super(AgentNetwork, self).__init__()

        # Build neural network
        self.build_network(num_inputs, num_hidden, num_actions, num_visualisations, list_of_param_lists)

        # Initialise optimizer and epsilon value
        self.optimizer = optim.Adam(self.parameters(), lr = 1e-2)
        self.eps = np.finfo(np.float32).eps.item()

        # Lists for saving action probabilities and rewards
        self.saved_actions = []
        self.rewards = []

    def build_network(self, num_inputs: int, num_hidden: int, num_actions: int, num_visualisations: int, list_of_param_lists: List[List[int]]):

        self.list_of_param_lists = list_of_param_lists
        num_extra_inputs = 0

        # Inputs to hidden state
        self.action_hidden_layer = nn.Linear(num_inputs, num_hidden)

        # Hidden state to action prediction
        self.action_prediction_layer = nn.Linear(num_hidden, num_actions)

        num_extra_inputs += num_actions

        # Sampled action + hidden state to next hidden state
        self.visualisation_hidden_layer = nn.Linear(num_hidden + num_extra_inputs, num_hidden)
    
        # Hidden state to visualisation prediction
        self.visualisation_prediction_layer = nn.Linear(num_hidden, num_visualisations)

        num_extra_inputs += num_visualisations

        start_num_extra_inputs = num_extra_inputs
        for action_index, list_of_params in enumerate(list_of_param_lists):
            num_extra_inputs = start_num_extra_inputs
            for param_index, param in enumerate(list_of_params):
                param_size = param['values']
                param_type = param['type']

                hidden_layer = nn.Linear(num_hidden + num_extra_inputs, num_hidden)
                prediction_layer = nn.Linear(num_hidden, param_size)

                setattr(self, f'action_{action_index}_param_{param_index}_hidden', hidden_layer)
                setattr(self, f'action_{action_index}_param_{param_index}_prediction', prediction_layer)

                if param_index < len(list_of_params) - 1:
                    num_extra_inputs += param_size
            
            critic_layer = nn.Linear(num_hidden, 1)
            setattr(self, f'action_{action_index}_critic', critic_layer)

    # @torch.jit.script_method
    def forward(self, state):
        extra_inputs = []

        # Feed input and process activation layer, input hidden state and get action probabilities with softmax as well as critic value 
        hidden_state = F.relu(self.action_hidden_layer(state))
        action_probs = F.softmax(self.action_prediction_layer(hidden_state), dim = -1)

        # Sample an action from action probabilities, one hot encode the sampled action and add to hidden state
        sampled_action, log_prob_action = sample_categorical(action_probs)
        one_hot_action = one_hot_encode_categorical(action_probs, sampled_action)
        extra_inputs.append(one_hot_action)
        concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        # Feed hidden state and process activation layer, input hidden state and get visualisation probabilities with softmax
        hidden_state = F.relu(self.visualisation_hidden_layer(concatenated_hidden_state))
        visualisation_probs = F.softmax(self.visualisation_prediction_layer(hidden_state), dim = -1)

        # Sample a visualisation index from visualisation probabilities
        sampled_visualisation, log_prob_vis = sample_categorical(visualisation_probs)
        one_hot_visualisation = one_hot_encode_categorical(visualisation_probs, sampled_visualisation)
        extra_inputs.append(one_hot_visualisation)
        concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        # Get branch corresponding to chosen action
        param_list = self.list_of_param_lists[sampled_action]

        sampled_values = [sampled_action, sampled_visualisation]
        value_probabilities = [log_prob_action, log_prob_vis]
        for param_index, param in enumerate(param_list):
            hidden_layer     = getattr(self, f'action_{sampled_action.item()}_param_{param_index}_hidden')
            prediction_layer = getattr(self, f'action_{sampled_action.item()}_param_{param_index}_prediction')

            hidden_state = F.relu(hidden_layer(concatenated_hidden_state))
            param_probs = F.softmax(prediction_layer(hidden_state), dim = -1)

            sampled_param, log_prob_param = sample_categorical(param_probs)
            value_probabilities.append(log_prob_param)
            sampled_values.append(sampled_param)

            if param_index < len(param_list) - 1:
                encoded_param = one_hot_encode_categorical(param_probs, sampled_param)
                extra_inputs.append(encoded_param)
                concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        critic_layer = getattr(self, f'action_{sampled_action.item()}_critic')
        critic_value = critic_layer(hidden_state)

        return sampled_values, value_probabilities, critic_value

    # @torch.jit.script_method
    def select_action(self, state):
        # Pytorch Tensor from Numpy array state
        tensor_state = torch.as_tensor(state, dtype = torch.float)

        # Sample action parameters using the current model(/policy) by feeding state to itself
        parameter_values, parameter_probabilities, critic_value = self(tensor_state)

        # Save the parameter probabilities and critic value in the saved actions list
        saved_action = (parameter_probabilities, critic_value)
        self.saved_actions.append(saved_action)

        # Return action parameters values
        return parameter_values
    
    # @torch.jit.script
    def finish_episode(self):
        R = 0
        policy_losses = []
        value_losses = []
        returns = []
        gamma = 1
        # Calculate the true (return?) value using rewards returned from the environment
        for r in self.rewards[::-1]:
            # Calculate the discounted value
            R = r + gamma * R
            returns.insert(0, R)

        returns = torch.tensor(returns).float()
        returns = (returns - returns.mean()) / (returns.std() + self.eps)

        for (log_probs, critic_value), R in zip(self.saved_actions, returns):
            advantage = R - critic_value.item()

            log_prob = sum(log_probs)

            # Calculate actor (policy) loss
            policy_losses.append(-log_prob * advantage)

            # Calculate critic (value) loss using L1 smooth loss
            value_losses.append(F.smooth_l1_loss(critic_value, torch.tensor([R])))

        # Sum up all the policy losses and value losses
        loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()

        # Reset gradients to zero
        self.optimizer.zero_grad()
        # Calculate the gradients by backpropagating loss
        loss.backward()
        # Apply the calculated gradients to the network
        self.optimizer.step()

        # Reset the reward and saved action buffers
        del self.rewards[:]
        del self.saved_actions[:]

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
    visualisations: Visualisations = parseVisualisations(visualisations)
    num_visualisations = len(visualisations.visualisations)
    visualisationsArray = visualisations.toArray()
        
    num_params_list = ACTION_PARAMS_LIST

    num_inputs = len(visualisationsArray)
    num_hidden = num_inputs * 2
    num_actions = NUM_ACTIONS


    model = AgentNetwork(num_inputs, num_hidden, num_actions, num_visualisations, num_params_list)
    env = VisualisationsEnvironment(visualisations)

    render = False
    num_episodes = 100
    running_reward = 10
    time_steps = 10000

    # run infinitely many episodes
    for i_episode in range(0, num_episodes):

        # reset environment and episode reward
        state = env.reset()
        ep_reward = 0

        # for each episode, only run 9999 steps so that we don't
        # infinite loop while learning
        for t in range(0, time_steps):

            # select action from policy
            action = model.select_action(state)

            # take the action
            state, reward, done, _ = env.step(action)
            # https://ai.stackexchange.com/questions/38336/pytorchs-actor-critic-implementation-seems-to-be-implemented-in-a-monte-carlo-f
            model.rewards.append(reward)
            ep_reward += reward
            
            if render:
                env.render()

            if done:
                break

        # update cumulative reward
        running_reward = 0.05 * ep_reward + (1 - 0.05) * running_reward

        # perform backprop
        #for name, param in model.state_dict().items():
        #    print('Name: ', name)
        #    print('Param: ', param)
        model.finish_episode()
        print(['------------------------\n']*3)
        #for name, param in model.state_dict().items():
        #    print('Name: ', name)
        #    print('Param: ', param)

        # log results
        if i_episode % 1 == 0:
            print('Episode {}\tLast reward: {:.2f}\tAverage reward: {:.2f}'.format(
                  i_episode, ep_reward, running_reward))

        # check if we have "solved" the cart pole problem
        if running_reward > 300 and False:
            print("Solved! Running reward is now {} and "
                  "the last episode runs to {} time steps!".format(running_reward, t))
            break

        action = model.select_action(env.reset())
        print(action)

if __name__ == '__main__':
    main()