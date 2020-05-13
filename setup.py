import numpy as np

class Rewards():

    def __init__(self, size):

        self.size = size
        self.rewards = np.zeros([self.size*self.size, self.size*self.size])

        self.top_left = 0
        self.top_right = self.size-1
        self.bottom_left = (self.size*self.size) - (self.size)
        self.bottom_right = (self.size*self.size) - 1

    def set_up(self, state, size):
        # up
        self.rewards[state, state-size] = 1
        self.rewards[state-size, state] = 1

    def set_down(self, state, size):
        # down
        self.rewards[state, state+size] = 1
        self.rewards[state+size, state] = 1

    def set_left(self, state, size):
        # left
        self.rewards[state, state-1] = 1
        self.rewards[state-1 , state] = 1

    def set_right(self, state, size):
        # right
        self.rewards[state, state+1] = 1
        self.rewards[state+1 , state] = 1

    def setup_rewards(self, size):

        #print("setup rewards")

        print("Corner states:",self.top_left, self.top_right, self.bottom_left, self.bottom_right)

        self.create_rewards()

    def create_rewards(self):

        #print("create rewards")

        for state in range(self.size*self.size):

            # top left corner
            if state == self.top_left:
                #print("corner", state)
                self.set_right(state, self.size)
                self.set_down(state, self.size)

            # top right corner
            elif state == self.top_right:
                #print("corner", state)
                self.set_left(state, self.size)
                self.set_down(state, self.size)

            # bottom left corner
            elif state == self.bottom_left:
                #print("corner", state)
                self.set_right(state, self.size)
                self.set_up(state, self.size)

            # bottom right corner
            elif state == self.bottom_right:
                #print("corner", state)
                self.set_left(state, self.size)
                self.set_up(state, self.size)

            # top row
            elif self.top_left <= state <= self.top_right:
                #print("row1", state)
                self.set_left(state, self.size)
                self.set_down(state, self.size)
                self.set_right(state, self.size)

            # bottom row
            elif self.bottom_left <= state <= self.bottom_right:
                #print("row2", state)
                self.set_left(state, self.size)
                self.set_up(state, self.size)
                self.set_right(state, self.size)

            # left column
            elif state % self.size == 0:
                #print("column1", state)
                self.set_up(state, self.size)
                self.set_right(state, self.size)
                self.set_down(state, self.size)

            # right column
            elif (state+1)%self.size == 0:
                #print("column2", state)
                self.set_up(state, self.size)
                self.set_left(state, self.size)
                self.set_down(state, self.size)

            else:
                #print("normal", state)
                self.set_right(state, self.size)
                self.set_up(state, self.size)
                self.set_left(state, self.size)
                self.set_down(state, self.size)

    def setup_state_pairs(self, state_pairs):

        for pair in state_pairs:
            self.rewards[pair[0], pair[1]] = 0
            self.rewards[pair[1], pair[0]] = 0

    def get_rewards(self):

        return self.rewards
