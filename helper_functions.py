def set_up(state, size):
    # up
    rewards[state, state-size] = 1
    rewards[state-size, state] = 1

def set_down(state, size):
    # down
    rewards[state, state+size] = 1
    rewards[state+size, state] = 1

def set_left(state, size):
    # left
    rewards[state, state-1] = 1
    rewards[state-1 , state] = 1

def set_right(state, size):
    # right
    rewards[state, state+1] = 1
    rewards[state+1 , state] = 1

for state in range(size*size):

    # top left corner
    if state == top_left:
        #print("corner", state)
        set_right(state, size)
        set_down(state, size)

    # top right corner
    elif state == top_right:
        #print("corner", state)
        set_left(state, size)
        set_down(state, size)

    # bottom left corner
    elif state == bottom_left:
        #print("corner", state)
        set_right(state, size)
        set_up(state, size)

    # bottom right corner
    elif state == bottom_right:
        #print("corner", state)
        set_left(state, size)
        set_up(state, size)

    # top row
    elif top_left <= state <= top_right:
        #print("row1", state)
        set_left(state, size)
        set_down(state, size)
        set_right(state, size)

    # bottom row
    elif bottom_left <= state <= bottom_right:
        #print("row2", state)
        set_left(state, size)
        set_up(state, size)
        set_right(state, size)

    # left column
    elif state % size == 0:
        #print("column1", state)
        set_up(state, size)
        set_right(state, size)
        set_down(state, size)

    # right column
    elif (state+1)%size == 0:
        #print("column2", state)
        set_up(state, size)
        set_left(state, size)
        set_down(state, size)

    else:
        #print("normal", state)
        set_right(state, size)
        set_up(state, size)
        set_left(state, size)
        set_down(state, size)
