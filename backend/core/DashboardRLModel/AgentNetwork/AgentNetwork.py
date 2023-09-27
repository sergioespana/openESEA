import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

from .Constants import EPSILON

from .Parameters import GAMMA, LEARNING_RATE

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

def collect_categorical(value_probabilities, top = None):
    dist = Categorical(value_probabilities)
    values_and_log_probs = [{ "value": value, "log_prob": dist.log_prob(value) } for value in range(len(value_probabilities))]
    sorted_values_and_log_probs = values_and_log_probs.sort(key = lambda x: x.get('log_prob'), reverse = True)
    if top is not None:
        return sorted_values_and_log_probs[0:top]
    return sorted_values_and_log_probs

def get_categorical(value_probabilities):
    return sample_categorical(value_probabilities)
    
def one_hot_encode_categorical(value_probabilities, sampled_value):
    num_values = value_probabilities.size(dim = 0)
    one_hot_encoded_value = F.one_hot(sampled_value, num_classes = num_values)
    return one_hot_encoded_value

class AgentNetwork(nn.Module):
    def __init__(self, num_inputs: int, num_hidden: int, num_actions: int, num_visualisations: int, list_of_param_lists):
        # Initialise base nn.Module class
        super(AgentNetwork, self).__init__()

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

        # Inputs into embedding through LSTM
        self.lstm_layer = nn.LSTM(num_inputs, num_hidden, bidirectional = True)
        # Double the hidden state size, because of the bi-LSTM
        num_hidden *= 2

        # Embedding to hidden state
        self.action_hidden_layer = nn.Linear(num_hidden, num_hidden)

        # Hidden state to action prediction
        self.action_prediction_layer = nn.Linear(num_hidden, num_actions)
        num_extra_inputs += num_actions

        # Sampled action + hidden state to next hidden state
        self.visualisation_hidden_layer = nn.Linear(num_hidden + num_extra_inputs, num_hidden)
    
        # Hidden state to visualisation prediction
        self.visualisation_prediction_layer = nn.Linear(num_hidden, num_visualisations)
        num_extra_inputs += num_visualisations

        # Prepare module lists and num_extra_inputs
        self.action_parameter_layers_list = nn.ModuleList()
        self.action_critic_layer_list = nn.ModuleList()
        num_extra_inputs_before_params = num_extra_inputs

        # Layers for list of params of every action
        for list_of_params in list_of_param_lists:
            num_extra_inputs = num_extra_inputs_before_params

            action_parameter_layers = nn.ModuleList()

            # Layer for every param
            for param_index, param in enumerate(list_of_params):
                param_size = param['values']
                param_type = param['type']

                # Hidden & Prediction layer
                hidden_layer = nn.Linear(num_hidden + num_extra_inputs, num_hidden)
                prediction_layer = nn.Linear(num_hidden, param_size)

                # If more params, append params to extra inputs
                if param_index < len(list_of_params) - 1:
                    num_extra_inputs += param_size

                # Add current parameter to this action list
                action_parameter_layers.append(nn.ModuleDict({'prediction': prediction_layer, 'hidden': hidden_layer }))
            
            # Critic layer
            action_critic_layer = nn.Linear(num_hidden, 1)

            # Append critic layer and parameter layers
            self.action_critic_layer_list.append(action_critic_layer)
            self.action_parameter_layers_list.append(action_parameter_layers)

    # @torch.jit.script_method
    def forward(self, state, dashboard_environment):
        extra_inputs = []

        ### LSTM Embedding ###
        embedding = self.process_lstm_embedding(state)

        ### Action Layer ###
        hidden_state, action_probs = self.process_action_layer(embedding)

        ### Action sampling ###
        # Sample an action from the action probabilities
        sampled_action, log_prob_action = sample_categorical(action_probs)
        # One hot encode the sampled action and add to the extra inputs
        one_hot_action = one_hot_encode_categorical(action_probs, sampled_action)
        extra_inputs.append(one_hot_action)
        concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        ### Visualisation Layer
        hidden_state, visualisation_probs = self.process_visualisation_layer(concatenated_hidden_state)

        ### Masking
        visualisation_mask = dashboard_environment.get_visualisation_mask(sampled_action)
        visualisation_probs = visualisation_probs * visualisation_mask
        if torch.sum(visualisation_probs) == 0:
            return None, None, None

        ### Sampling visualisations ###
        # Sample a visualisation index from the visualisation probabilities
        sampled_visualisation, log_prob_vis = sample_categorical(visualisation_probs)
        # One hot encode the sampled visualisation and add to the extra inputs
        one_hot_visualisation = one_hot_encode_categorical(visualisation_probs, sampled_visualisation)
        extra_inputs.append(one_hot_visualisation)
        concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        # Get branch corresponding to chosen action
        param_list = self.list_of_param_lists[sampled_action]

        sampled_values = [sampled_action, sampled_visualisation]
        value_probabilities = [log_prob_action, log_prob_vis]
        action_param_layers = self.action_parameter_layers_list[sampled_action]
        for param_index, action_param_layer in enumerate(action_param_layers):
            hidden_layer = action_param_layer['hidden']
            prediction_layer = action_param_layer['prediction']

            hidden_state = F.relu(hidden_layer(concatenated_hidden_state))
            param_probs = F.softmax(prediction_layer(hidden_state), dim = -1)

            sampled_param, log_prob_param = sample_categorical(param_probs)
            value_probabilities.append(log_prob_param)
            sampled_values.append(sampled_param)

            if param_index < len(param_list) - 1:
                encoded_param = one_hot_encode_categorical(param_probs, sampled_param)
                extra_inputs.append(encoded_param)
                concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        critic_layer = self.action_critic_layer_list[sampled_action]
        critic_value = critic_layer(hidden_state)

        return sampled_values, value_probabilities, critic_value
    
    def process_lstm_embedding(self, state):
        # Unsqueeze for input in lstm
        unsqueezed_state = state.unsqueeze(0).unsqueeze(0)
        # Feed input into LSTM for embedding
        unsqueezed_embedding, (h_n, c_n) = self.lstm_layer(unsqueezed_state)
        # Squeeze back into 'normal' shape
        embedding = unsqueezed_embedding.squeeze()
        return embedding
    
    def process_action_layer(self, state):
        # Feed embedding and process activation layer, input hidden state and get action probabilities with softmax
        hidden_state = F.relu(self.action_hidden_layer(state))
        action_probs = F.softmax(self.action_prediction_layer(hidden_state), dim = -1)
        return hidden_state, action_probs
    
    def process_visualisation_layer(self, state):
        # Feed hidden state and process activation layer, input hidden state and get visualisation probabilities with softmax
        hidden_state = F.relu(self.visualisation_hidden_layer(state))
        visualisation_probs = F.softmax(self.visualisation_prediction_layer(hidden_state), dim = -1)
        return hidden_state, visualisation_probs
    
    def simple_argmax_forward(self, state):
        extra_inputs = []

        ### LSTM Embedding ###
        embedding = self.process_lstm_embedding(state)

        ### Action Layer ###
        hidden_state, action_probs = self.process_action_layer(embedding)

        ### Action sampling ###
        # Sample an action from the action probabilities
        sampled_action, log_prob_action = argmax_categorical(action_probs)
        # One hot encode the sampled action and add to the extra inputs
        one_hot_action = one_hot_encode_categorical(action_probs, sampled_action)
        extra_inputs.append(one_hot_action)
        concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        ### Visualisation Layer
        hidden_state, visualisation_probs = self.process_visualisation_layer(concatenated_hidden_state)

        ### Masking
        ###

        ### Sampling visualisations ###
        # Sample a visualisation index from the visualisation probabilities
        sampled_visualisation, log_prob_vis = argmax_categorical(visualisation_probs)
        # One hot encode the sampled visualisation and add to the extra inputs
        one_hot_visualisation = one_hot_encode_categorical(visualisation_probs, sampled_visualisation)
        extra_inputs.append(one_hot_visualisation)
        concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        # Get branch corresponding to chosen action
        param_list = self.list_of_param_lists[sampled_action]

        sampled_values = [sampled_action, sampled_visualisation]
        value_probabilities = [log_prob_action, log_prob_vis]
        action_param_layers = self.action_parameter_layers_list[sampled_action]
        for param_index, action_param_layer in enumerate(action_param_layers):
            hidden_layer = action_param_layer['hidden']
            prediction_layer = action_param_layer['prediction']

            hidden_state = F.relu(hidden_layer(concatenated_hidden_state))
            param_probs = F.softmax(prediction_layer(hidden_state), dim = -1)

            sampled_param, log_prob_param = argmax_categorical(param_probs)
            value_probabilities.append(log_prob_param)
            sampled_values.append(sampled_param)

            if param_index < len(param_list) - 1:
                encoded_param = one_hot_encode_categorical(param_probs, sampled_param)
                extra_inputs.append(encoded_param)
                concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        critic_layer = self.action_critic_layer_list[sampled_action]
        critic_value = critic_layer(hidden_state)

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
        
        # ### LSTM ###
        # # Unsqueeze for input in lstm
        # unsqueezed_state = state.unsqueeze(0).unsqueeze(0)
        # # Feed input into LSTM for embedding
        # unsqueezed_embedding, (h_n, c_n) = self.lstm_layer(unsqueezed_state)
        # # Squeeze back into 'normal' shape
        # embedding = unsqueezed_embedding.squeeze()

        # ### Forward pass action ###
        # # Feed embedding and process activation layer, input hidden state and get action probabilities with softmax as well as critic value 
        # hidden_state = F.relu(self.action_hidden_layer(embedding))
        # action_probs = F.softmax(self.action_prediction_layer(hidden_state), dim = -1)

        # ### Action sampling ###
        # # Sample an action from action probabilities, one hot encode the sampled action and add to hidden state
        # actions_and_log_probs = collect_categorical(action_probs, top) # sorted by log_prob
        # for action_and_log_prob in actions_and_log_probs:
        #     one_hot_action = one_hot_encode_categorical(action_probs, action_and_log_prob['value'])
        #     extra_inputs = [one_hot_action]
        #     concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        #     ### Forward pass visualisations ###
        #     # Feed hidden state and process activation layer, input hidden state and get visualisation probabilities with softmax
        #     hidden_state = F.relu(self.visualisation_hidden_layer(concatenated_hidden_state))
        #     visualisation_probs = F.softmax(self.visualisation_prediction_layer(hidden_state), dim = -1)

        #     ### Sampling visualisations ###
        #     # Sample a visualisation index from visualisation probabilities
        #     visualisations_and_log_probs = collect_categorical(visualisation_probs) # sorted by log_prob
        #     one_hot_visualisations = [one_hot_encode_categorical(visualisation_probs, visualisation_and_log_prob['value']) for visualisation_and_log_prob in visualisations_and_log_probs]
        #     one_hot_visualisations = one_hot_visualisations if top is None else one_hot_visualisations[0:top]
        #     extra_inputs.append(one_hot_visualisation)
        #     concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        #     # Get branch corresponding to chosen action
        #     param_list = self.list_of_param_lists[sampled_action]

        #     sampled_values = [sampled_action, sampled_visualisation]
        #     value_probabilities = [log_prob_action, log_prob_vis]
        #     for param_index, param in enumerate(param_list):
        #         hidden_layer     = getattr(self, f'action_{sampled_action.item()}_param_{param_index}_hidden')
        #         prediction_layer = getattr(self, f'action_{sampled_action.item()}_param_{param_index}_prediction')

        #         hidden_state = F.relu(hidden_layer(concatenated_hidden_state))
        #         param_probs = F.softmax(prediction_layer(hidden_state), dim = -1)

        #         sampled_param, log_prob_param = sample_categorical(param_probs)
        #         value_probabilities.append(log_prob_param)
        #         sampled_values.append(sampled_param)

        #         if param_index < len(param_list) - 1:
        #             encoded_param = one_hot_encode_categorical(param_probs, sampled_param)
        #             extra_inputs.append(encoded_param)
        #             concatenated_hidden_state = torch.cat([hidden_state] + extra_inputs, dim = 0)

        #     critic_layer = getattr(self, f'action_{sampled_action.item()}_critic')
        #     critic_value = critic_layer(hidden_state)

        #     return sampled_values, value_probabilities, critic_value

    # @torch.jit.script_method
    def output_parameter_values(self, state, dashboard_environment):
        # Pytorch Tensor from Numpy array state
        tensor_state = torch.as_tensor(state, dtype = torch.float)

        # Sample action parameters using the current model(/policy) by feeding state to itself
        parameter_values, parameter_probabilities, critic_value = self(tensor_state, dashboard_environment)
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
        # Calculate the gradients by backpropagating loss
        loss.backward()
        # Apply the calculated gradients to the network
        self.optimizer.step()

        # Reset the reward and saved action buffers
        del self.rewards[:]
        del self.saved_actions[:]
