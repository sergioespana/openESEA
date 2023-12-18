import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

import numpy as np
from enum import IntEnum

from .Constants import EPSILON

from .Parameters import GAMMA, LEARNING_RATE

from ..Dashboard.Environment import DashboardEnvironment

# Functions for categorical variables
# Sample a value according to probabilities
def sample_categorical(value_probabilities):
    dist = Categorical(value_probabilities)
    value = dist.sample() # Sample according to probabilities
    log_prob = dist.log_prob(value)
    return value, log_prob

# Get the value with the highest probability
def argmax_categorical(value_probabilities):
    dist = Categorical(value_probabilities)
    value = torch.argmax(value_probabilities) # Get value with highest probability
    log_prob = dist.log_prob(value)
    return value, log_prob

# Enforce getting the given value
def get_categorical(value_probabilities, value):
    dist = Categorical(value_probabilities)
    value = torch.tensor(value.item()).long()
    log_prob = dist.log_prob(value)
    return value, log_prob

# Get a random value with the highest probability
def argmax_categorical_random(value_probabilities):
    dist = Categorical(value_probabilities)
    value = torch.argmax(value_probabilities)
    # Find all indices with max value
    max_indices = torch.where(value_probabilities == value_probabilities[value])[0]
    # Select random index position
    selected_index = torch.randint(0, max_indices.size(0), (1,))[0]
    # Get index
    value = max_indices[selected_index]
    log_prob = dist.log_prob(value)
    return value, log_prob

# Collect all values with their probabilities
def collect_categorical(value_probabilities):
    dist = Categorical(value_probabilities)
    values_and_log_probs = []
    for value in range(len(value_probabilities)):
        value = torch.tensor(value)
        prob = value_probabilities[value]
        log_prob = dist.log_prob(value)
        one_hot = one_hot_encode_categorical(value_probabilities, value)

        values_and_log_probs.append({ "value": value, "one_hot": one_hot, "log_prob": log_prob, "prob": prob })
    return values_and_log_probs
    
# One hot encode a categorical variable
def one_hot_encode_categorical(value_probabilities, sampled_value):
    num_values = value_probabilities.size(dim = 0)
    one_hot_encoded_value = F.one_hot(sampled_value, num_classes = num_values)
    return one_hot_encoded_value

# Mask probabilities and return possibilities
def mask_probabilities(probabilities, mask):
    # If there are no possibilities -> return None
    if mask is None or torch.sum(mask) == 0: return None
    # Otherwise apply mask to probabilities
    probabilities = probabilities * mask
    # If the available options have no probability, return to mask to sample from possible options
    if torch.sum(probabilities) == 0: return mask
    # Else return probabilities
    return probabilities

class FeedForwardLayer(nn.Module):
    def __init__(self, num_inputs, num_outputs, num_extra_inputs = None, num_hidden = None, num_lstm_hidden = None, bidirectionalembedding = False):
        super(FeedForwardLayer, self).__init__()
        if num_hidden is None: num_hidden = num_inputs
        if num_lstm_hidden is None: num_lstm_hidden = num_hidden
        if num_extra_inputs is not None: num_inputs += num_extra_inputs
        self.embedding_layer = LSTMEmbeddingLayer(num_inputs, num_lstm_hidden, bidirectional = bidirectionalembedding)
        if bidirectionalembedding: num_lstm_hidden *= 2
        self.linear_activation_layer = nn.Linear(num_lstm_hidden, num_hidden)
        self.softmax_probs_layer = nn.Linear(num_hidden, num_outputs)

    def forward(self, input_state, sampled_values = []):
        # print(input_state, sampled_values)
        current_state = torch.cat(sampled_values + [input_state], dim = 0)
        embedding = self.embedding_layer(current_state)
        hidden_state = F.relu(self.linear_activation_layer(embedding))
        output_probs = F.softmax(self.softmax_probs_layer(hidden_state), dim = -1)
        return hidden_state, output_probs
    
class CriticLayer(nn.Module):
    def __init__(self, num_inputs, num_extra_inputs = None, num_hidden = None, bidirectionalembedding = False):
        super(CriticLayer, self).__init__()
        if num_hidden is None: num_hidden = num_inputs
        if num_extra_inputs is not None: num_inputs += num_extra_inputs
        self.embedding_layer = LSTMEmbeddingLayer(num_inputs, num_hidden, bidirectional = bidirectionalembedding)
        if bidirectionalembedding: num_hidden *= 2
        self.critic_layer = nn.Linear(num_hidden, 1)

    def forward(self, input_state, sampled_values = []):
        current_state = torch.cat(sampled_values + [input_state], dim = 0)
        embedding = self.embedding_layer(current_state)
        critic_value = self.critic_layer(embedding)
        return critic_value

class LSTMEmbeddingLayer(nn.Module):
    def __init__(self, num_inputs, num_hidden, bidirectional):
        super(LSTMEmbeddingLayer, self).__init__()
        self.lstm_embedding_layer = nn.LSTM(num_inputs, num_hidden, bidirectional = bidirectional)

    def forward(self, state):
        # Unsqueeze to match lstm dimensions
        unsqueezed_state = state.unsqueeze(0).unsqueeze(0)
        # Forward into lstm layer
        unsqueezed_embedding, (_, _) = self.lstm_embedding_layer(unsqueezed_state)
        # Squeeze back into 1d tensor
        embedding = unsqueezed_embedding.squeeze()
        return embedding
    
class ForwardPass(IntEnum):
    SAMPLE = 0
    PREDICT = 1
    EMULATE = 2

class AgentNetwork(nn.Module):
    def __init__(self, num_inputs: int, num_hidden: int, num_actions: int, num_visualisations: int, list_of_param_lists, dashboard_environment: DashboardEnvironment):
        # Initialise base nn.Module class
        super(AgentNetwork, self).__init__()

        # For getting masks
        self.dashboard_environment = dashboard_environment

        # Build neural network
        self.build_network(num_inputs, num_hidden, num_actions, num_visualisations, list_of_param_lists)

        # Initialise optimizer and epsilon value
        self.optimizer = optim.Adam(self.parameters(), lr = LEARNING_RATE)

        # Lists for saving action probabilities and rewards
        self.saved_actions = []
        self.rewards = []

        self.saved_user_actions = []
        self.user_rewards = []

    def build_network(self, num_inputs: int, num_hidden: int, num_actions: int, num_visualisations: int, list_of_param_lists):
        self.list_of_param_lists = list_of_param_lists

        num_extra_inputs = 0

        self.visualisation_layer = FeedForwardLayer(num_inputs, num_visualisations, bidirectionalembedding = True, num_hidden = num_hidden)
        num_extra_inputs += num_visualisations

        self.action_layer = FeedForwardLayer(num_hidden, num_actions, num_extra_inputs = num_extra_inputs)
        num_extra_inputs += num_actions

        # Prepare module lists and num_extra_inputs
        self.action_layers_list = nn.ModuleList()

        # Layers for list of params of every action
        for list_of_params in list_of_param_lists:
            num_extra_inputs_with_params = num_extra_inputs

            parameter_layers = nn.ModuleList()

            # Layer for every param
            for param in list_of_params:
                param_size = param['Values']
                param_type = param['Type']

                # Hidden & Prediction layer
                param_layer = FeedForwardLayer(num_hidden, param_size, num_extra_inputs = num_extra_inputs_with_params)

                # Add current parameter to this action list
                parameter_layers.append(param_layer)
                
                # If more params, append params to extra inputs
                num_extra_inputs_with_params += param_size

            # Critic layer
            critic_layer = CriticLayer(num_hidden, num_extra_inputs = num_extra_inputs_with_params)

            # Add modules for this action
            self.action_layers_list.append(nn.ModuleList([parameter_layers, critic_layer]))

    # @torch.jit.script_method
    def forward_emulate(self, state, action_values):
        # Get values from action values 
        visualisation = action_values[0]
        action = action_values[1]
        parameters = action_values[2:]

        # Lists for storing extra inputs and value probabilities
        log_probabilities = []
        sampled_values = []
        extra_inputs = []

        ### Feed forward: Visualisation Layer ###
        hidden_state, visualisation_probs = self.visualisation_layer(state)

        ### Sampling: Visualisation ###
        sampled_visualisation, log_prob_vis = get_categorical(visualisation_probs, visualisation)
        # Keep track of probabilities, sampled value and encoded input
        sampled_values.append(sampled_visualisation)
        log_probabilities.append(log_prob_vis)
        extra_inputs.append(one_hot_encode_categorical(visualisation_probs, sampled_visualisation))


        ### Feed forward: Action layer ###
        hidden_state, action_probs = self.action_layer(hidden_state, extra_inputs)

        ### Sampling: Action ###
        sampled_action, log_prob_action = get_categorical(action_probs, action)
        # Keep track of probabilities, sampled value and encoded input
        sampled_values.append(sampled_action)
        log_probabilities.append(log_prob_action)
        extra_inputs.append(one_hot_encode_categorical(action_probs, sampled_action))


        ### Parameter layers ###
        for param_index, param_layer in enumerate(self.action_layers_list[sampled_action][0]): # [0] to get parameter layers

            ### Feed forward: Parameter layer ###
            hidden_state, parameter_probs = param_layer(hidden_state, extra_inputs)

            ### Sampling: Parameter ###
            sampled_parameter, log_prob_parameter = get_categorical(parameter_probs, parameters[param_index])
            # Keep track of probabilities, sampled value and encoded input
            sampled_values.append(sampled_parameter)
            log_probabilities.append(log_prob_parameter)
            extra_inputs.append(one_hot_encode_categorical(parameter_probs, sampled_parameter))


        ### Critic layer ###
        critic_value = self.action_layers_list[sampled_action][1](hidden_state, extra_inputs) # [1] to get critic layer

        return sampled_values, log_probabilities, critic_value
    
    # @torch.jit.script_method
    def forward(self, forward_pass: ForwardPass, *args, **kwargs):
        if forward_pass == ForwardPass.SAMPLE:
            return self.forward_sample(*args, **kwargs)
        elif forward_pass == ForwardPass.PREDICT:
            return self.forward_predict(*args, **kwargs)
        elif forward_pass == ForwardPass.EMULATE:
            return self.forward_emulate(*args, **kwargs)

    def forward_sample(self, state):
        # Lists for storing extra inputs, sampled values and value probabilities
        log_probabilities = []
        sampled_values = []
        extra_inputs = []

        ### Feed forward: Visualisation Layer ###
        hidden_state, visualisation_probs = self.visualisation_layer(state)

        ### Sampling: Visualisation ###
        sampled_visualisation, log_prob_vis = sample_categorical(visualisation_probs)
        # Keep track of probabilities, sampled value and encoded input
        sampled_values.append(sampled_visualisation)
        log_probabilities.append(log_prob_vis)
        extra_inputs.append(one_hot_encode_categorical(visualisation_probs, sampled_visualisation))


        ### Feed forward: Action layer ###
        hidden_state, action_probs = self.action_layer(hidden_state, extra_inputs)

        ### Masking probabilities: Action ###
        action_probs = mask_probabilities(action_probs, self.get_action_mask(sampled_visualisation))
        # If no options, return
        if action_probs is None: return None, None, None

        ### Sampling: Action ###
        sampled_action, log_prob_action = sample_categorical(action_probs)
        # Keep track of probabilities, sampled value and encoded input
        sampled_values.append(sampled_action)
        log_probabilities.append(log_prob_action)
        extra_inputs.append(one_hot_encode_categorical(action_probs, sampled_action))


        ### Parameter layers ###
        for param_index, param_layer in enumerate(self.action_layers_list[sampled_action][0]): # [0] to get parameter layers

            ### Feed forward: Parameter layer ###
            hidden_state, parameter_probs = param_layer(hidden_state, extra_inputs)

            ### Masking probabilities: Parameter ###
            parameter_probs = mask_probabilities(parameter_probs, self.get_parameter_mask(sampled_visualisation, sampled_action, sampled_values[2:], param_index))
            # If no options, return
            if parameter_probs is None: return None, None, None

            ### Sampling: Parameter ###
            sampled_parameter, log_prob_parameter = sample_categorical(parameter_probs)
            # Keep track of probabilities, sampled value and encoded input
            sampled_values.append(sampled_parameter)
            log_probabilities.append(log_prob_parameter)
            extra_inputs.append(one_hot_encode_categorical(parameter_probs, sampled_parameter))


        ### Critic layer ###
        critic_value = self.action_layers_list[sampled_action][1](hidden_state, extra_inputs) # [1] to get critic layer

        return sampled_values, log_probabilities, critic_value
    
    def get_action_mask(self, sampled_visualisation):
        mask_list = self.dashboard_environment.get_action_mask(sampled_visualisation)
        return torch.tensor(mask_list, dtype = float)
    
    def get_parameter_mask(self, sampled_visualisation, sampled_action, sampled_params, param_index):
        mask_list = self.dashboard_environment.get_parameter_mask(sampled_visualisation, sampled_action, sampled_params, param_index)
        if mask_list is None: return None
        return torch.tensor(mask_list, dtype = float)
    
    def forward_predict(self, state, top = 10):
        # Pytorch Tensor from Numpy array state
        tensor_state = torch.as_tensor(state, dtype = torch.float)
        TESTING = True
        if not TESTING:

            # Sample action parameters using the current model(/policy) by feeding state to itself
            parameter_values, _, _ = self(ForwardPass.PREDICT, tensor_state)

            # Return action parameters values
            return parameter_values
        
        ### Feed forward: Visualisation Layer ###
        hidden_state, visualisation_probs = self.visualisation_layer(tensor_state)

        ### Sampling: Visualisation ###
        sampled_visualisations = collect_categorical(visualisation_probs)
        sampled_information_list = []
        for sampled_visualisation in sampled_visualisations:
            sampled_information_list.append(
                { 
                    "values": [sampled_visualisation["value"]], 
                    "one_hots": [sampled_visualisation["one_hot"]], 
                    "log_probs": [sampled_visualisation["log_prob"]], 
                    "probs": [sampled_visualisation["prob"]] 
                }
            )
        # If top is set, sort by probability and get top K
        if top is not None:
            # print(sampled_information_list)
            # print(top)
            # print('regel 328')
            # input()
            # print(sampled_information_list)
            sampled_information_list.sort(key = lambda x: np.prod([0 if val is None else val.item() for val in x.get('probs')]), reverse = True)
            sampled_information_list = sampled_information_list[0:top]
            # print(sampled_information_list)
            # input()

        new_sampled_information_list = []
        # Keep track of probabilities, sampled value and encoded input
        for sampled_information in sampled_information_list:
            extra_inputs = sampled_information['one_hots']

            ### Feed forward: Action layer ###
            hidden_state, action_probs = self.action_layer(hidden_state, extra_inputs)

            ### Masking probabilities: Action ###
            action_probs = mask_probabilities(action_probs, self.get_action_mask(sampled_information['values'][0]))
            # If no options, skip this action
            if action_probs is None: continue

            ### Sampling: Action ###
            sampled_actions = collect_categorical(action_probs)
            for sampled_action in sampled_actions:
                new_information = sampled_action
                new_sampled_information_list.append(
                    { 
                        "values": sampled_information["values"] + [new_information['value']], 
                        "one_hots": sampled_information["one_hots"] + [new_information['one_hot']], 
                        "log_probs": sampled_information["log_probs"] + [new_information['log_prob']], 
                        "probs": sampled_information["probs"] + [new_information['prob']] 
                    }
                )

        sampled_information_list = new_sampled_information_list
        # If top is set, sort by probability and get top K
        if top is not None: 
            # print(sampled_information_list)
            # print('regel 363')
            # input()
            # print(sampled_information_list)
            sampled_information_list.sort(key = lambda x: np.prod([0 if val is None else val.item() for val in x.get('probs')]), reverse = True)
            sampled_information_list = sampled_information_list[0:top]
            # print(sampled_information_list)
            # input()

        new_sampled_information_list = []
        for sampled_information in sampled_information_list:
            sampled_values = sampled_information['values']
            sampled_visualisation = sampled_values[0]
            sampled_action = sampled_values[1]
            extra_inputs = sampled_information['one_hots']

            ### FOR NOW 1 PARAM, BUT MAY BECOME MORE COMPLEX
            ### Parameter layers ###
            for param_index, param_layer in enumerate(self.action_layers_list[sampled_action][0]): # [0] to get parameter layers

                ### Feed forward: Parameter layer ###
                hidden_state, parameter_probs = param_layer(hidden_state, extra_inputs)

                ### Masking probabilities: Parameter ###
                parameter_probs = mask_probabilities(parameter_probs, self.get_parameter_mask(sampled_visualisation, sampled_action, sampled_values[2:], param_index))
                # If no options, return
                if parameter_probs is None: continue

                ###### divide by max value to compensate for dimensionality of parameters (scale to where max = 1)
                # parameter_probs = torch.div(parameter_probs, torch.max(parameter_probs))

                ### Sampling: Parameter ###
                sampled_parameters = collect_categorical(parameter_probs)
                # for sampled_parameter in sampled_parameters:
                sampled_parameters.sort(key = lambda x: 0 if x.get('prob') is None else x['prob'], reverse = True)
                new_information = sampled_parameters[0]
                new_sampled_information_list.append(
                    { 
                        "values": sampled_information["values"] + [new_information['value']], 
                        "one_hots": sampled_information["one_hots"] + [new_information['one_hot']], 
                        "log_probs": sampled_information["log_probs"] + [new_information['log_prob']], 
                        "probs": sampled_information["probs"] + [new_information['prob']] 
                    }
                )

        sampled_information_list = new_sampled_information_list
        # If top is set, sort by probability and get top K
        if top is not None: 
            # print(sampled_information_list)
            sampled_information_list.sort(key = lambda x: np.prod([0 if val is None else val.item() for val in x.get('probs')]), reverse = True)
            sampled_information_list = sampled_information_list[0:top]
            # print(sampled_information_list)
            # input()
        # print(sampled_information_list)
        # input()

        return [sampled_information['values'] for sampled_information in sampled_information_list]

    # @torch.jit.script_method
    def output_parameter_values(self, state):
        # Pytorch Tensor from Numpy array state
        tensor_state = torch.as_tensor(state, dtype = torch.float)

        # Sample action parameters using the current model(/policy) by feeding state to itself
        parameter_values, parameter_probabilities, critic_value = self(ForwardPass.SAMPLE, tensor_state)
        if parameter_values is None: return None, None
        
        # Save the parameter probabilities and critic value in the saved actions list
        saved_action = (parameter_probabilities, critic_value)

        # Return action parameters values
        return parameter_values, saved_action
    
    def emulate_output_parameter_values(self, state, action):
        # Pytorch Tensor from Numpy array state
        tensor_state = torch.as_tensor(state, dtype = torch.float)

        # Sample action parameters using the current model(/policy) by feeding state to itself
        parameter_values, parameter_probabilities, critic_value = self(ForwardPass.EMULATE, tensor_state, action)
        if parameter_values is None: return None, None
        
        # Save the parameter probabilities and critic value in the saved actions list
        saved_action = (parameter_probabilities, critic_value)

        # Return action parameters values
        return parameter_values, saved_action
    
    # @torch.jit.script
    def update_network_gradients(self):
        # Initialise return value to 0 and create a list for the accumulated returns
        R = 0
        returns = []
        # print(self.rewards, self.saved_actions)
        # Calculate the accumulated return value using rewards returned from the environment
        for r in self.rewards[::-1]:
            # Calculate the discounted return over the trajectory
            R = r + GAMMA * R
            # Insert return value
            returns.insert(0, R)

        # Convert returns to pytorch tensor and normalise the return values
        returns = torch.tensor(returns).float()
        returns = (returns - returns.mean()) / (returns.std() + EPSILON)

        # Add user feedback
        # Weight to give more value to user rewards, user rewards -> 50%
        user_weight = len(self.rewards) / (len(self.user_rewards) + EPSILON)
        # Create reward tensor and multiply rewards by this weight
        user_returns = torch.tensor(self.user_rewards).float()
        user_returns = torch.mul(user_returns, torch.tensor(user_weight))

        returns = torch.cat([returns, user_returns], dim = 0)
        saved_actions = self.saved_actions + self.saved_user_actions

        # Create lists for storing value and policy losses
        policy_losses = []
        value_losses = []
        # Calculate losses for each time step
        for (log_probs, critic_value), R in zip(saved_actions, returns):
            advantage = R - critic_value.item()

            log_prob = sum(log_probs)

            # Calculate actor (policy) loss
            policy_losses.append(-log_prob * advantage)

            # Calculate critic (value) loss using L1 smooth loss
            value_losses.append(F.smooth_l1_loss(critic_value, torch.tensor([R])))

        # Sum up the policy losses and value losses over all time steps
        loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()

        # Reset gradients to zero
        self.optimizer.zero_grad()
        torch.autograd.set_detect_anomaly(True)
        # Calculate the gradients by backpropagating loss
        loss.backward()
        # Apply the calculated gradients to the network
        self.optimizer.step()

        # input()
        # Reset the reward and saved action buffers
        del self.rewards[:]
        del self.saved_actions[:]
        del self.user_rewards[:]
        del self.saved_user_actions[:]
