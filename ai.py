import numpy as np
import matplotlib.pyplot as plt

class QAgent():
    
    # Initialize alpha, gamma, states, actions, rewards, and Q-values
    def __init__(self, alpha, gamma, states, actions, rewards, Q):
        
        self.gamma = gamma  
        self.alpha = alpha 
        
        self.states = states
        self.actions = actions
        self.rewards = rewards
        
        self.Q = Q
        
        self.q_change = []

    # Training the robot in the environment
    def training(self, start_state, end_state, iterations):
        
        # copy the rewards table
        rewards_new = np.copy(self.rewards)
        
        # set reward for staying in end state as maximum
        rewards_new[end_state, end_state] = 999
        
        # explore environment
        for i in range(iterations):
            
            # set current state to random state
            current_state = np.random.randint(0,9)

            # blank playable actions list
            playable_actions = []
            
            # for each action
            for j in range(9):

                # if actions is possible ie has a reward greater than 0
                if rewards_new[current_state,j] > 0:

                    # add to playable actions
                    playable_actions.append(j)
    
            # choose a random state for next state from playable actions
            next_state = np.random.choice(playable_actions)
            TD = rewards_new[current_state,next_state] + \
                    self.gamma * self.Q[next_state, np.argmax(self.Q[next_state,])] - self.Q[current_state,next_state]
            
            self.Q[current_state,next_state] += self.alpha * TD

            print(current_state, next_state, self.alpha*TD, self.Q[current_state, next_state])

            self.q_change.append(self.alpha * TD)

        # initilise optimal route with strting location
        route = [start_state]

        
        next_state = start_state
        
        # Get the route 
        self.get_optimal_route(start_state, end_state, next_state, route, self.Q, iterations)
        
    # Get the optimal route from q values
    def get_optimal_route(self, start_state, end_state, next_state, route, Q, iterations):
        
        while(next_state != end_state):
            
            print("Starting state:", start_state+1)
            
            next_state = np.argmax(Q[start_state,])

            print("Q Table:", Q[start_state,])

            print("Next state:", next_state+1)
                
            route.append(next_state)
            start_state = next_state

            print()
        
         
        print(route)

        self.create_td_graph(iterations, 50)
    

    def create_td_graph(self, iterations, nBins):

        bin_size = iterations / nBins

        bin_size = int(bin_size)
        totals = []
        x = []

        for i in range(nBins):

            x.append(i*bin_size)
            totals.append(sum(self.q_change[i*bin_size:(i*bin_size+bin_size)])/bin_size)

           
        print(sum(totals))
        print(totals)

        print(sum(self.q_change) / int(bin_size))
        
        plt.plot(x, totals)
        plt.show()





## MAIN 

# Define the states and actions
actions = [0,1,2,3,4,5,6,7,8]
states = [0,1,2,3,4,5,6,7,8]

# Define the rewards
rewards = np.array([[0,1,0,0,0,0,0,0,0],
              [1,0,1,0,1,0,0,0,0],
              [0,1,0,0,0,1,0,0,0],
              [0,0,0,0,0,0,1,0,0],
              [0,1,0,0,0,0,0,1,0],
              [0,0,1,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,1,0],
              [0,0,0,0,1,0,1,0,1],
              [0,0,0,0,0,0,0,1,0]])

# Initialize parameters
gamma = 0.75 # Discount factor
alpha = 0.9 # Learning rate

# Initializing Q-Values
Q = np.array(np.zeros([9,9]))

qagent = QAgent(alpha, gamma, states, actions, rewards, Q)
qagent.training(8, 0, 1000)
