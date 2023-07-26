import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

from AgentNetwork.Constants import EPSILON
from AgentNetwork.Parameters import GAMMA, LEARNING_RATE

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
    def update_network_gradients(self):
        # Initialise return value to 0 and create a list for the accumulated returns
        R = 0
        returns = []

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