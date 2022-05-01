import time
import gridworld
import n_sarsa
import sarsa2
import os
import numpy as np
import copy
from tqdm import tqdm

# Specify dimensions

while True:    
    try:
        dim = int(input("Please provide your desired grid dimension (dim X dim):\n"))
        
        if dim >= 5:
            break
            
        print("Dimension needs to be larger than 4!\n")
    
    except:
        print("Please provide an integer value!\n")

# Create GW object

gw = gridworld.Gridworld(dim)

gw.build()

# Show GW

gw.visualize(show_gridworld=True,show_rewardworld=True,show_mergeworld=True)

input("Press enter to start SARSA")


# define actionspace
action_space=[0,1,2,3]
dict_moves={0:"left",1:"right",2:"up",3:"down"}

sarsa=sarsa2.Sarsa2(dim*dim,action_space,gw.get_target_idx(),alpha=0.8,gamma=0.9, n_of_episodes=10, n=1)

sarsa.train(gw)

"""sarsa=n_sarsa.sarsa(dim*dim,action_space,total_episodes=50000)

# initializing the reward
reward = 0


# Starting the SARSA learning

for episode in tqdm(range(sarsa.total_episodes)):
    

#         # check exploration status
#         unique, counts = np.unique(Q, return_counts=True)
#         tmp = dict(zip(unique, counts))
#         if tmp[0] < ((dim*dim)/4): # if a less then a quarter of Q values is unexplored end the algorithm
#             break
#         else:
#             print("Unexplored: ",(tmp[0]/Q.size)*100, "%")
    
    t = 0 # reset temperatur during episodes
    gw.reset()
       
    state1 = copy.deepcopy(gw.grid_world) # prevent bugs 
    
    idx_state1 = gw.get_player_idx() # state needs to be an index for the condition work 
    action1 = sarsa.choose_action(idx_state1) # get current action

    while t < sarsa.max_steps: 
        
        #sgw.visualize()
         
        # getting the next state
        state2, done, reward = gw.step(dict_moves[action1])
                
        # get index of player in next state
        idx_state2 = gw.get_player_idx()
        
        # choose the next action
        action2 = sarsa.choose_action(idx_state2) # state needs to be an index for the condition work
         
        # calculate the Q-value
        sarsa.update(state1, state2, reward, action1, action2)
         
        # update state and action
        state1 = state2
        action1 = action2
        
        # update temperature
        t += 1
         
        #If at the end of learning process
        if done:
            break

            
print("Learning finished!")        


# print learned policy for every state

moves_ls = []
dummy = np.array([0.,0.,0.,0.])

for i in sarsa.Q:
    if (i==dummy).all(): # if state only has value of 0s
        moves_ls.append("None")
        
    else:
        moves_ls.append(dict_moves[np.argmax(i)])
    
moves_ls = np.array(moves_ls)
moves_ls = moves_ls.reshape(dim,dim)"""


#print("Learned moves: \n")
#print(moves_ls)

gw.visualize(show_mergeworld=True, show_gridworld=True,show_rewardworld=True)


input("Press enter to see our learned moves in Action")
gw.reset()
total_reward=0
for timestep in range(20):
    # get index of player in current state
    idx_state = gw.get_player_idx()
    action=sarsa.choose_action(idx_state)
    s,finished,reward=gw.step(action)
    total_reward+=reward
    #clear screen
    if os.name == 'posix': #Linux, Mac
        os.system('clear')
    else: #Windows
        os.system('cls')
    print()
    print("T=", timestep)
    print("Total reward=",total_reward)
    print("chosen action:",action,"-->",dict_moves[action])
    gw.visualize(show_mergeworld=True, show_gridworld=True,show_rewardworld=False)

    if finished:
        print("is finished")
        break
    time.sleep(1)


gw.reset()
gw.visualize(show_mergeworld=True, show_gridworld=True,show_rewardworld=True)