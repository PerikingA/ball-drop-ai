import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random 

class DQN(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=64):
        super(DQN, self).__init__()
        # Initialize the neural network layers
        self.state_size = state_size
        self.action_size = action_size
        self.hidden_size = hidden_size

        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, action_size)
        
        self.memory = deque(maxlen=10000)
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)
        self.batch_size = 64
        self.gamma = 0.99  # determines importance of future rewards
        self.epsilon = 1.0  # prob. of choosing a random action
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

    def forward(self, x):
        # Forward pass through the network
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

    def remember(self, state, action, reward, next_state, done):
        # Store xp in memory
        self.memory.append((state, action, reward, next_state, done))

    def learn(self):
        
        if len(self.memory) < self.batch_size:
            return
        
        # Sample a batch from memory
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        # convert memory info into PyTorch tensors to process
        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.float32)

        # get q vals
        current_q_values = self(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        next_q_values = self(next_states).max(1)[0]
        target_q_values = rewards + (self.gamma * next_q_values * (1 - dones))

        # get loss and optimize
        loss = nn.MSELoss()(current_q_values, target_q_values)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # update epsilon  
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
