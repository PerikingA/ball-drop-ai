import torch
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import deque
from dqn_model import DQN
from game_env import GameEnv
import pygame

# Hyperparameters
GAMMA = 0.99  # Discount factor for future rewards
BATCH_SIZE = 64  # Number of samples drawn from memory
LEARNING_RATE = 0.001
MEMORY_SIZE = 10000
EPSILON_DECAY = 0.995  # Decay factor for exploration rate
MIN_EPSILON = 0.01
NUM_EPISODES = 100
CHECKPOINT_INTERVAL = 1  # Save checkpoint every episode
CHECKPOINT_PATH = 'checkpoint.pth'

# Initialize environment, model, optimizer, and replay memory
env = GameEnv()

# State size depends on the features used in get_state
input_dim = 103  # Updated state size
output_dim = 2   # Number of actions: left, right
dqn = DQN(input_dim, output_dim)
optimizer = optim.Adam(dqn.parameters(), lr=LEARNING_RATE)
replay_memory = deque(maxlen=MEMORY_SIZE)
epsilon = 1.0

# Initialize Pygame for visualization
pygame.init()
width, height = 1200, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('AI Training Visualization')
clock = pygame.time.Clock()

def choose_action(state):
    if np.random.rand() < epsilon:
        return random.randint(0, output_dim - 1)  # Explore: random action
    state = torch.FloatTensor(state).unsqueeze(0)
    q_values = dqn(state)
    return torch.argmax(q_values).item()  # Exploit: best action

def train():
    global epsilon
    if len(replay_memory) < BATCH_SIZE:
        return  # Don't train if there aren't enough samples
    batch = random.sample(replay_memory, BATCH_SIZE)
    states, actions, rewards, next_states, dones = zip(*batch)

    # memory info
    # Convert lists to numpy arrays
    states = np.array(states)
    actions = np.array(actions)
    rewards = np.array(rewards)
    next_states = np.array(next_states)
    dones = np.array(dones)
    # Convert numpy arrays to PyTorch tensors
    states = torch.FloatTensor(states)
    actions = torch.LongTensor(actions)
    rewards = torch.FloatTensor(rewards)
    next_states = torch.FloatTensor(next_states)
    dones = torch.FloatTensor(dones)

    # get q vals
    current_q_values = dqn(states).gather(1, actions.unsqueeze(1)).squeeze(1)
    next_q_values = dqn(next_states).max(1)[0]
    target_q_values = rewards + (1 - dones) * GAMMA * next_q_values

    # get loss & optimize
    loss = F.mse_loss(current_q_values, target_q_values.detach())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)  # Decay epsilon

def save_checkpoint(episode):
    torch.save({
        'episode': episode,
        'model_state_dict': dqn.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'epsilon': epsilon
    }, CHECKPOINT_PATH)
    
def render_training():
    screen.fill((0, 0, 0))  
    env.render(screen) 
    pygame.display.flip()
    
def main():
    for episode in range(NUM_EPISODES):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = choose_action(state)
            next_state, reward, done = env.step(action)
            replay_memory.append((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            train()
            # Visualize training
            render_training()
            clock.tick(60) 

        print(f"Episode {episode + 1}/{NUM_EPISODES}, Total Reward: {total_reward}")
        
        if (episode + 1) % CHECKPOINT_INTERVAL == 0:
            save_checkpoint(episode + 1)

    torch.save(dqn.state_dict(), 'trained_model.pth')

if __name__ == "__main__":
    main()
