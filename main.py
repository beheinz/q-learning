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

    scale = 100

    w = int(scale*(size) + (scale/4)*(size-1))
    print("w", w)
    h = int(scale*(size) + (scale/4)*(size-1))
    print("h", h)

    data = np.zeros((h, w, 3), dtype=np.uint8)

    for state in qagent.route:

        coords = state_to_coords(state, size)

        # find correct pixel placement for x
        if coords[1] % 2 == 0:
            x = int(coords[1]/2*(scale)) + int(coords[1]/2*(scale/4))
        else:
            x = int((coords[1]/2)+0.5)*(scale) + int((coords[1]/2)-0.5)*(scale/4)

        # find correct pixel placement for y
        if coords[0] % 2 == 0:
            y = int(coords[0]/2*(scale)) + int(coords[0]/2*(scale/4))
        else:
            y = int((coords[0]/2)+0.5)*(scale) + int((coords[0]/2)-0.5)*(scale/4)

        print(x, x+scale, y, y+scale)

        data[x:x+scale, y:y+scale] = [0, 0 ,255]

    for pair in state_pairs:

        coords = state_pair_to_coords(pair, size)

        # find the correct pixel placement for x
        if coords[1] % 2 == 0:
            x = int(coords[1]/2*(scale)) + int(coords[1]/2*(scale/4))
        else:
            x = int((coords[1]/2)+0.5)*(scale) + int((coords[1]/2)-0.5)*(scale/4)

        # find correct pixel placement for y
        if coords[0] % 2 == 0:
            y = int(coords[0]/2*(scale)) + int(coords[0]/2*(scale/4))
        else:
            y = int((coords[0]/2)+0.5)*(scale) + int((coords[0]/2)-0.5)*(scale/4)

        print(int(x), int(x+scale/4), int(y), int(y+scale/4))

        # if a horizontal line
        if abs(pair[0] - pair[1]) == 1:
            length_x = scale
            length_y = scale / 4

        # verticle line
        else:
            length_x = scale / 4
            length_y = scale

        # set to red
        data[int(x):int(x+length_x), int(y):int(y+length_y)] = [255, 255 ,255]

    img = Image.fromarray(data, 'RGB')
    img.save('my.png')

def generate_line(pair, length, size):

    line_pairs = []

    # verticle
    if abs(pair[0] - pair[1]) == 1:
        for i in range(length):
            new_pair = [pair[0] + i*size, pair[1] + i*size]
            line_pairs.append(new_pair)
    else:
        for i in range(length):
            new_pair = [pair[0] + i, pair[1] + i]
            line_pairs.append(new_pair)

    return line_pairs


def main():

    # setup variables
    size = 32 # min size is 3
    gamma = 0.75 # discount factor
    alpha = 0.9 # learning rate

    # barrier lines that make up state state_pairs
    # state pairs are two states besides each other than have a barrier between them
    #line_a = [[7,8],[23,24],[39,40],[55,56],[71,72],[87,88],[103,104],[119,120],[135,136],[151,152],[151,167],[150,166]]
    #line_b = [[38,54],[36,52],[37,53],[39,55]]
    #line_c = [[106,122],[105,121],[104,120],[107,123],[108,124]]
    #line_d = [[63,79],[62,78],[61,77],[60,76],[59,75],[58,74]]

    #state_pairs = line_a + line_b + line_c + line_d


    line_a = generate_line([4,5], 18, size)
    line_b = generate_line([431,432], 19, size)
    line_c = generate_line([395,427], 15, size)
    line_d = generate_line([694,726], 10, size)


    state_pairs = line_a + line_b + line_c + line_d

    print("Grid barrier lines created:", len(state_pairs))


    # blank table of q values
    Q = np.array(np.zeros([size*size,size*size]))

    states = setup_states(size)
    actions = setup_actions(size)

    rewards = Rewards(size)
    rewards.setup_rewards(size)
    rewards.setup_state_pairs(state_pairs)

    qagent = QAgent(alpha, gamma, states, actions, rewards.rewards, Q, size)

    print("Training model")
    qagent.training(0, 1023, 100000)

    print("Creating image")
    create_image(size, qagent, state_pairs)

if __name__ == "__main__":
    main()
