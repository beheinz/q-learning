import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class QAgent():

    # initialize alpha, gamma, states, actions, rewards, and Q-values
    def __init__(self, alpha, gamma, states, actions, rewards, Q, size):

        self.gamma = gamma
        self.alpha = alpha

        self.states = states
        self.actions = actions
        self.rewards = rewards

        self.Q = Q
        self.size = size

        self.q_change = []

    # Training the robot in the environment
    def training(self, start_state, end_state, iterations):

        # copy the rewards table
        rewards_new = np.copy(self.rewards)

        # set reward for staying in end state as maximum
        rewards_new[end_state, end_state] = 999

        # explore environment
        for i in range(iterations):

            if i % 1000 == 0:
                print("Running iteration", i, "...")

            # set current state to random state
            current_state = np.random.randint(0,(self.size*self.size))

            # blank playable actions list
            playable_actions = []

            # for each action
            for j in range(self.size*self.size):

                # if actions is possible ie has a reward greater than 0
                if rewards_new[current_state,j] > 0:

                    # add to playable actions
                    playable_actions.append(j)

            # choose a random state for next state from playable actions
            next_state = np.random.choice(playable_actions)
            TD = rewards_new[current_state,next_state] + \
                    self.gamma * self.Q[next_state, np.argmax(self.Q[next_state,])] - self.Q[current_state,next_state]

            self.Q[current_state,next_state] += self.alpha * TD

            #print(current_state, next_state, self.alpha*TD, self.Q[current_state, next_state])

            self.q_change.append(self.alpha * TD)

        # initilise optimal route with strting location
        route = [start_state]


        next_state = start_state

        # get the route
        self.get_optimal_route(start_state, end_state, next_state, route, self.Q, iterations)

    # get the optimal route from q values
    def get_optimal_route(self, start_state, end_state, next_state, route, Q, iterations):

        while(next_state != end_state):

            next_state = np.argmax(Q[start_state,])

            route.append(next_state)
            start_state = next_state

            # if route gets stuck
            if len(route) > 999:
                break

        print("Route:", route)

        self.route = route

        self.create_td_graph(iterations, 50)

    def create_td_graph(self, iterations, nBins):

        bin_size = iterations / nBins

        bin_size = int(bin_size)
        totals = []
        x = []

        for i in range(nBins):

            x.append(i*bin_size)
            totals.append(sum(self.q_change[i*bin_size:(i*bin_size+bin_size)])/bin_size)

        plt.plot(x, totals)

        plt.xlabel('Iteration', fontsize=10)
        plt.ylabel('Average temporal difference', fontsize=10)

        plt.savefig('foo.png')

        plt.show()
