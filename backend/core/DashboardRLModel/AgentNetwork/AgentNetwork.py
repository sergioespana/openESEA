import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

from .Constants import EPSILON

from .Parameters import GAMMA, LEARNING_RATE

from ..Dashboard.Environment import DashboardEnvironment

# Functions for categorical variables
def sample_categorical(value_probabilities):
    dist = Categorical(value_probabilities)
    value = dist.sample() # Sample according to probabilities
    log_prob = dist.log_prob(value)
    return value, log_prob

def argmax_categorical(value_probabilities):
    dist = Categorical(value_probabilities)
    value = torch.argmax(value_probabilities) # Get value with highest probability
    log_prob = dist.log_prob(value)
    return value, log_prob

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

def collect_categorical(value_probabilities, top = None):
    dist = Categorical(value_probabilities)
    values_and_log_probs = [{ "value": value, "log_prob": dist.log_prob(value) } for value in range(len(value_probabilities))]
    sorted_values_and_log_probs = values_and_log_probs.sort(key = lambda x: x.get('log_prob'), reverse = True)
    if top is not None:
        return sorted_values_and_log_probs[0:top]
    return sorted_values_and_log_probs
    
def one_hot_encode_categorical(value_probabilities, sampled_value):
    num_values = value_probabilities.size(dim = 0)
    one_hot_encoded_value = F.one_hot(sampled_value, num_classes = num_values)
    return one_hot_encoded_value

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

    def forward(self, input_state, extra_inputs = []):
        current_state = torch.cat(extra_inputs + [input_state], dim = 0)
        embedding = self.embedding_layer(current_state)
        hidden_state = F.relu(self.linear_activation_layer(embedding))
        output_probs = F.softmax(self.softmax_probs_layer(hidden_state), dim = -1)
        return hidden_state, output_probs

class LSTMEmbeddingLayer(nn.Module):
    def __init__(self, num_inputs, num_hidden, bidirectional):
        super(LSTMEmbeddingLayer, self).__init__()
        self.lstm_embedding_layer = nn.LSTM(num_inputs, num_hidden, bidirectional = bidirectional)

    def forward(self, state):
        unsqueezed_state = state.unsqueeze(0).unsqueeze(0)
        unsqueezed_embedding, (_, _) = self.lstm_embedding_layer(unsqueezed_state)
        embedding = unsqueezed_embedding.squeeze()
        return embedding
    
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
                param_size = param['values']
                param_type = param['type']

                # Hidden & Prediction layer
                param_layer = FeedForwardLayer(num_hidden, param_size, num_extra_inputs = num_extra_inputs_with_params)

                # Add current parameter to this action list
                parameter_layers.append(param_layer)
                
                # If more params, append params to extra inputs
                num_extra_inputs_with_params += param_size

            # Critic layer
            critic_layer = FeedForwardLayer(num_hidden, 1, num_extra_inputs = num_extra_inputs_with_params)

            # Add modules for this action
            self.action_layers_list.append(nn.ModuleList([parameter_layers, critic_layer]))

    # @torch.jit.script_method
    def forward(self, state):
        extra_inputs = []

        ### Visualisation Layer
        hidden_state, visualisation_probs = self.visualisation_layer(state)

        ### Sampling visualisation ###

        # Sample a visualisation index from the visualisation probabilities
        sampled_visualisation, log_prob_vis = sample_categorical(visualisation_probs)
        # One hot encode the sampled visualisation and add to the extra inputs
        extra_inputs.append(one_hot_encode_categorical(visualisation_probs, sampled_visualisation))

        ### Action layer
        hidden_state, action_probs = self.action_layer(state, extra_inputs)

        ### Sampling action ###

        # Masking actions
        action_mask = self.get_action_mask(sampled_visualisation)
        # If there are no possible actions -> return
        if torch.sum(action_mask) == 0: return None, None, None
        # Otherwise apply mask to probabilities
        action_probs *= action_mask
        # If there are no available options, select a random valid action from the mask
        if torch.sum(action_probs) == 0: action_probs = action_mask

        # Sample an action from the action probabilities
        sampled_action, log_prob_action = sample_categorical(action_probs)
        # One hot encode the sampled action and add to the extra inputs
        extra_inputs.append(one_hot_encode_categorical(action_probs, sampled_action))

        # Get branch corresponding to chosen action
        sampled_values = [sampled_visualisation, sampled_action]
        value_probabilities = [log_prob_vis, log_prob_action]
        action_layer_dict = self.action_layers_list[sampled_action]
        for param_layer in action_layer_dict[0]:
            hidden_state, param_probs = param_layer(hidden_state, extra_inputs)

            sampled_param, log_prob_param = sample_categorical(param_probs)
            value_probabilities.append(log_prob_param)
            sampled_values.append(sampled_param)

            encoded_param = one_hot_encode_categorical(param_probs, sampled_param)
            extra_inputs.append(encoded_param)

        _, critic_value = action_layer_dict[1](hidden_state, extra_inputs)

        return sampled_values, value_probabilities, critic_value
    
    def get_action_mask(self, sampled_visualisation):
        return self.dashboard_environment.get_action_mask(sampled_visualisation)
    
    def simple_argmax_forward(self, state):
        extra_inputs = []

        ### Visualisation Layer
        hidden_state, visualisation_probs = self.visualisation_layer(state)

        ### Sampling visualisation ###

        # Sample a visualisation index from the visualisation probabilities
        sampled_visualisation, log_prob_vis = argmax_categorical_random(visualisation_probs)
        # One hot encode the sampled visualisation and add to the extra inputs
        extra_inputs.append(one_hot_encode_categorical(visualisation_probs, sampled_visualisation))

        ### Action layer
        hidden_state, action_probs = self.action_layer(state, extra_inputs)

        ### Sampling action ###

        # Masking actions
        action_mask = self.get_action_mask(sampled_visualisation)
        # If there are no possible actions -> return
        if torch.sum(action_mask) == 0: return None, None, None
        # Otherwise apply mask to probabilities
        action_probs *= action_mask
        # If there are no available options, select a random valid action from the mask
        if torch.sum(action_probs) == 0: action_probs = action_mask

        # Sample an action from the action probabilities
        sampled_action, log_prob_action = argmax_categorical_random(action_probs)
        # One hot encode the sampled action and add to the extra inputs
        extra_inputs.append(one_hot_encode_categorical(action_probs, sampled_action))

        # Get branch corresponding to chosen action
        sampled_values = [sampled_visualisation, sampled_action]
        value_probabilities = [log_prob_vis, log_prob_action]
        action_layer_dict = self.action_layers_list[sampled_action]
        for param_layer in action_layer_dict[0]:
            hidden_state, param_probs = param_layer(hidden_state, extra_inputs)

            sampled_param, log_prob_param = argmax_categorical_random(param_probs)
            value_probabilities.append(log_prob_param)
            sampled_values.append(sampled_param)

            encoded_param = one_hot_encode_categorical(param_probs, sampled_param)
            extra_inputs.append(encoded_param)

        _, critic_value = action_layer_dict[1](hidden_state, extra_inputs)

        return sampled_values, value_probabilities, critic_value

    def forward_collect(self, state, top = None):
        TESTING = True
        if TESTING:
            # Pytorch Tensor from Numpy array state
            tensor_state = torch.as_tensor(state, dtype = torch.float)

            # Sample action parameters using the current model(/policy) by feeding state to itself
            parameter_values, _, _ = self.simple_argmax_forward(tensor_state)

            # Return action parameters values
            return parameter_values

    # @torch.jit.script_method
    def output_parameter_values(self, state):
        # Pytorch Tensor from Numpy array state
        tensor_state = torch.as_tensor(state, dtype = torch.float)

        # Sample action parameters using the current model(/policy) by feeding state to itself
        parameter_values, parameter_probabilities, critic_value = self(tensor_state)
        if parameter_values is None: 
            return None
        
        # Save the parameter probabilities and critic value in the saved actions list
        saved_action = (parameter_probabilities, critic_value)
        self.saved_actions.append(saved_action)

        # Return action parameters values
        return parameter_values
    
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

        # Create lists for storing value and policy losses
        policy_losses = []
        value_losses = []
        # Calculate losses for each time step
        for (log_probs, critic_value), R in zip(self.saved_actions, returns):
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

        # Reset the reward and saved action buffers
        del self.rewards[:]
        del self.saved_actions[:]
