import pygame
import torch
from dqn_model import DQN
from game_env import GameEnv

# Hyperparameters
STATE_SIZE = 103  # 1 (player) + 100 (50 balls * 2) + 1 (ball speed) + 1 (timer) = 103
ACTION_SIZE = 2
HIDDEN_SIZE = 64
TRAINED_MODEL_PATH = 'trained_model.pth'
CHECKPOINT_PATH = 'checkpoint.pth' 
USE_CHECKPOINT = True

# Initialize environment and model
env = GameEnv()
model = DQN(state_size=STATE_SIZE, action_size=ACTION_SIZE, hidden_size=HIDDEN_SIZE)

# Load model
try:
    if USE_CHECKPOINT:
        # Load checkpoint
        checkpoint = torch.load(CHECKPOINT_PATH)
        model.load_state_dict(checkpoint['model_state_dict'])
    else:
        # Load trained model
        model.load_state_dict(torch.load(TRAINED_MODEL_PATH))
except FileNotFoundError:
    print("Error: model file was not found.")
    exit(1)
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)
    
model.eval()

# Initialize Pygame
pygame.init()
width, height = 1200, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ball Drop AI')
clock = pygame.time.Clock()

def choose_action(state):
    with torch.no_grad():
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        q_values = model(state)
        return torch.argmax(q_values).item()

def play_game():
    state = env.reset()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        action = choose_action(state)
        next_state, reward, done = env.step(action)
        env.render(screen)
        state = next_state
        pygame.display.flip()
        clock.tick(60)  

if __name__ == "__main__":
    play_game()
    pygame.quit()
