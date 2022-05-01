import time
import numpy as np
import copy
import random

class Sarsa2():
    N=1
    Q=np.zeros((1,1))
    gamma=0.9
    epsilon=0.9
    alpha=0.8
    n_of_episodes=10
    action_space=[0,1,2,3]
    max_steps=10

    def __init__(self,number_of_states,action_space,terminal_state,alpha=0.8,gamma=0.9,epsilon=0.9, n_of_episodes=10, n=1, max_steps=100):
        self.N=n

        # initialize Q value table 
        self.Q = np.zeros((number_of_states,len(action_space)))
        self.Q[terminal_state] = 0

        self.gamma=gamma
        self.alpha=alpha
        self.epsilon=epsilon
        self.n_of_episodes=n_of_episodes
        self.action_space=action_space
        self.max_steps=max_steps

    def choose_action(self,state):
        if np.random.uniform(0, 1) < self.epsilon:

            # sample random action
            action = random.sample(self.action_space,1)[0] 
            return action
            
        else:
            
            # get best action (maximize Q value)
            action = np.argmax(self.Q[state, :]) # requires index of the player (state)
            
            return action


    def train(self,gw):
        gw=copy.deepcopy(gw)
        for n_of_episode in range(self.n_of_episodes):
            
            #Initialize S
            gw.reset()
            
            state_1=gw.get_player_idx()
            #Choose action using Q
            action_1=self.choose_action(state_1)

            finished=False

            states=[state_1]
            actions=[action_1]
            t=0
            while t<self.max_steps:
                
                rewards=[]
                for n in range(self.N):
                    #Take action
                    s,finished,r=gw.step(actions[-1])
                    states.append(s)
                    rewards.append(r*self.gamma**n)

                    #Choose action using Q
                    ca=self.choose_action(states[-1])
                    actions.append(ca)

                    print(n_of_episode)
                    print(ca)
                    gw.visualize(show_mergeworld=True, show_gridworld=True,show_rewardworld=False)
                    time.sleep(0.2)


                    if finished:
                        break

                returns=sum(rewards)
            
                self.Q[states[0],actions[0]]=self.Q[states[0],actions[0]]+self.alpha*(returns+-self.Q[states[0],actions[0]])
                t+=1
                if finished:
                    break






