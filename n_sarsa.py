import numpy as np
import random

class sarsa():
    # set initial parameters
    epsilon = 0.9
    total_episodes = 90000000
    max_steps = 1000
    alpha = 0.8
    gamma = 0.9


    number_of_states=0

    action_space=[]

    # list to save the SAR
    n_list=[]
 
    # initialize Q value table 
    Q = np.zeros((1,1))

    def __init__(self,number_of_states,action_space,epsilon = 0.9,   total_episodes = 90000000,    max_steps = 1000,    alpha = 0.8,    gamma = 0.9):
        self.Q = np.zeros((number_of_states,len(action_space))) # dim: number of states x actions
        self.epsilon=epsilon
        self.total_episodes=total_episodes
        self.max_steps=max_steps
        self.alpha=alpha
        self.gamma=gamma
        self.action_space=action_space


    def choose_action(self,state):
        if np.random.uniform(0, 1) < self.epsilon:
            
            # sample random action
            action = random.sample(self.action_space,1)[0] 
            return action
            
        else:
            
            # get best action (maximize Q value)
            action = np.argmax(self.Q[state, :]) # requires index of the player (state)
            
            return action

    def update(self,state1,state2,reward,action1,action2):
    
    #     print("current state (s): ",state1, "\n", "next state (s'): ",
    #           state2,"\n","reward (r): ",reward,"\n", "current action (a): ",
    #           dict_moves[action1],"\n", "next action (a'): ",dict_moves[action2],"\n")
        
        idx1 = np.where(state1 == "P")[0][0]
        #print("index 1: ",idx1)
        
        idx2 = np.where(state2 =="P")[0][0]
        #print("index 2: ",idx2)
        
        # get estimates
        Q_old = self.Q[idx1, action1]   
        Q_new = self.Q[idx2, action2]
        self.Q[idx1, action1] = Q_old + self.alpha * (reward + (self.gamma *  Q_new) - Q_old)
        
    #     print("Q_old: ", Q_old)
    #     print("Q_new: ", Q_new)
    #     print(("Reward: ", reward))
    #     print("Q_calc: ", (Q_old + alpha * (reward + (gamma *  Q_new) - Q_old)))

    
    def train(self):
        pass
