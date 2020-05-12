import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from setup import Rewards
from ai import QAgent

def setup_states(size):

    nStates = size * size
    states = []

    for state in range(nStates):
        states.append(state)

    return states

def setup_actions(size):

    nActions = size * size

    actions = []

    for action in range(nActions):
        actions.append(action)

    return actions

def create_image(size, qagent, state_pairs):

    # coords where top left is 0,0
    def state_to_coords(state, size):
        x = state % size
        y = int(state / size)

        return [2*x, 2*y]

    def state_pair_to_coords(state_pair, size):
        coords_a = state_to_coords(state_pair[0], size)
        coords_b = state_to_coords(state_pair[1], size)

        #print(coords_a, coords_b)

        a = int((coords_a[0] + coords_b[0]) / 2)
        b = int((coords_a[1] + coords_b[1]) / 2)

        return [a, b]

    w, h = 100*(size*2)-1, 100*(size*2)-1
    data = np.zeros((h, w, 3), dtype=np.uint8)

    for state in qagent.route:
        coords = state_to_coords(state, size)
        data[coords[1]*100:coords[1]*100+100, coords[0]*100:coords[0]*100+100] = [0, 0 ,255]

    for pair in state_pairs:
        coords = state_pair_to_coords(pair, size)
        data[coords[1]*100:coords[1]*100+100, coords[0]*100:coords[0]*100+100] = [255, 255 ,255]

    #data[0:1600, 0:1600] = [255, 0, 0] # red patch in upper left
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    #img.show()

def main():

    # setup variables
    size = 16 # min size is 3
    gamma = 0.75 # discount factor
    alpha = 0.9 # learning rate
    state_pairs = [[7,8],[23,24],[39,40],[55,56],[71,72],[87,88],[103,104]]
    Q = np.array(np.zeros([size*size,size*size]))

    states = setup_states(size)
    actions = setup_actions(size)

    rewards = Rewards(size)
    rewards.setup_rewards(size)
    rewards.setup_state_pairs(state_pairs)

    qagent = QAgent(alpha, gamma, states, actions, rewards.rewards, Q, size)
    qagent.training(3, 15, 25000)

    create_image(size, qagent, state_pairs)

if __name__ == "__main__":
    main()
