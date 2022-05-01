import numpy as np
import copy
import random
import os

# Create Gridworld object

class Gridworld:
    symbols={
        "Player":"P",
        "Wall":"\u2588",
        "Space":" ",
        "Teleport":"\u00A4"
    }

    def __init__(self,dim):
        
        self.dim = dim
        self.grid_world = []
        self.reward_world = []
        
        self.grid_world_original = []
        self.reward_world_original = []
        
        self.free_fields = []
        self.goal = []
        self.tele_idx = []
        
        self.finished = False
            
    def build(self):
        
        ######### Build GW #########

        for x in range(self.dim+1):
            self.grid_world = [self.symbols["Space"]] * (x * x)

        # Create obstacles

        self.grid_world = np.array(self.grid_world)

        num_obs = int((self.dim*self.dim)/8) # specify number of obstacles

        obstacle_indices = np.random.choice(np.arange(1,self.grid_world.size), replace=False, size=num_obs) # start at one to not place obstacles at player pos

        self.grid_world[obstacle_indices] = self.symbols["Wall"]
        
        ######### Build RW and Teleport #########

        # Assign rewards to states

        self.reward_world =copy.deepcopy(self.grid_world.flatten()) # create seperate array for reward

        self.free_fields = [x for x in np.arange(self.reward_world.size) if x not in obstacle_indices if x != 0] # generate list of free fields

        np.random.shuffle(self.free_fields) # shuffle free fields

        self.goal = self.free_fields[-1] # choose index for postive reward (terminal state)
        
        self.tele_idx = [self.free_fields[-2],self.free_fields[-3]]# choose 2 indices for teleports
        
        rew_neg_amount = 5 # specify number of negative rewards

        rew_neg_indices = np.random.choice(self.free_fields[1:-3], replace=False, size=rew_neg_amount) # randomly choose incides for negative rewards

        self.reward_world[rew_neg_indices] = "-" # place negative rewards

        self.reward_world[self.goal] = "+" # place positive reward (terminal state)
        
        self.reward_world[self.tele_idx] = self.symbols["Teleport"] # place teleports  

        ######### Set starting point #########

        self.grid_world[0] = self.symbols["Player"] # top left

        # Save Backup

        self.reward_world_original = copy.deepcopy(self.reward_world) 
        
        self.grid_world_original = copy.deepcopy(self.grid_world)
        

        #Check solvability
        if self.check_if_solvable()==False:
            self.build()
        
        
        return self.get_player_idx(), self.reward_world

    def check_if_solvable(self):
        #TODO
        return True

    def reset(self):
        
        self.reward_world = copy.deepcopy(self.reward_world_original)
        self.grid_world = copy.deepcopy(self.grid_world_original)
        self.finished = False
        #self.grid_world[0] = self.symbols["Player"]
        return self.get_player_idx(), self.reward_world

    def step(self, action):
        dict_moves={0:"left",1:"right",2:"up",3:"down"}
        action=dict_moves[action]
        idx = np.where(self.grid_world == self.symbols["Player"])[0]
        idx = idx[0]
        
        self.reward = 0
        
        if action == "left":
            
            # if path is Oob
            
            if idx == 0 or (idx%self.dim) == 0:
        
                return self.get_player_idx(), self.finished, self.reward
            
            else:
                
                if self.grid_world[idx-1]  == self.symbols["Wall"]:
                    
                    return self.get_player_idx(), self.finished, self.reward
                
                # check for teleports and teleport with 60% probability
                
                elif idx-1 == self.tele_idx[0] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[1]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                    
                elif idx-1 == self.tele_idx[1] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[0]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                   
                # if path isnt blocked
                
                else:
                    
                    # check for rewards
                    
                    if self.reward_world[idx-1] == "+":
                        
                        self.reward = +500
                        self.finished = True
                        
                    elif self.reward_world[idx-1] == "-":
                        
                        self.reward = -1
                        
                    # move player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[idx-1] = self.symbols["Player"]
                
                return self.get_player_idx(), self.finished, self.reward
            
        elif action == "right":
            
            # if path is Oob
            
            if idx == (self.dim-1) or idx == (len(self.grid_world)-1):
                
                return self.get_player_idx(), self.finished, self.reward
            
            else:
                
                if self.grid_world[idx+1] == self.symbols["Wall"]:
                    
                    return self.get_player_idx(), self.finished, self.reward
                
                # check for teleports and teleport with 60% probability
                
                elif idx+1 == self.tele_idx[0] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[1]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                    
                elif idx+1 == self.tele_idx[1] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[0]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                
                # if path isnt blocked
                
                else:
                    
                    # check for rewards
                    
                    if self.reward_world[idx+1] == "+":
                        
                        self.reward = +500
                        self.finished = True
                        
                    elif self.reward_world[idx+1] == "-":
                        
                        self.reward = -1
                        
                    # move player
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[idx+1] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
            
        elif action == "up":
            
             # if path is Oob
            
            if idx in range(0,(self.dim-1)):
                
                return self.get_player_idx(), self.finished, self.reward
            
            else:
                
                if self.grid_world[idx-self.dim] == self.symbols["Wall"]:
                    
                    return self.get_player_idx(), self.finished, self.reward
                
                # check for teleports and teleport with 60% probability
                
                elif idx-self.dim == self.tele_idx[0] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[1]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                    
                elif idx-self.dim == self.tele_idx[1] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[0]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                
                # if path isnt blocked
                
                else:
                    
                    # check for rewards
                    
                    if self.reward_world[idx-self.dim] == "+":
                        
                        self.reward = +500
                        self.finished = True
                        
                    elif self.reward_world[idx-self.dim] == "-":
                        
                        self.reward = -1
                        
                    # move player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[idx-self.dim] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
            
        elif action == "down":
            
             # if path is Oob
            
            if idx in range(len(self.grid_world)-self.dim,len(self.grid_world)):
                
                return self.get_player_idx(), self.finished, self.reward
            
            else:
                
                if self.grid_world[idx+self.dim] == self.symbols["Wall"]:
                    
                    return self.get_player_idx(), self.finished, self.reward
                
                # check for teleports and teleport with 60% probability
                
                elif idx+self.dim == self.tele_idx[0] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[1]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                    
                elif idx+self.dim == self.tele_idx[1] and random.randint(0,100) > 40:
                    
                    # teleport player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[self.tele_idx[0]] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
                
                # if path isnt blocked
                
                else:
                    
                    # check for rewards
                    
                    if self.reward_world[idx+self.dim] == "+":
                        
                        self.reward = +500
                        self.finished = True
                        
                    elif self.reward_world[idx+self.dim] == "-":
                        
                        self.reward = -1
                        
                    # move player
                    
                    self.grid_world[idx] = self.symbols["Space"]
                    
                    self.grid_world[idx+self.dim] = self.symbols["Player"]
                    
                    return self.get_player_idx(), self.finished, self.reward
            
        else:
            print("Please choose an action [left,right,up,down]!")        

    def create_visual_border(self, viz):
        return((self.dim*2)+1)*self.symbols["Wall"]+"\n"+self.symbols["Wall"]+str(viz).replace(' [', '').replace('[', '').replace(']', '').replace('\'', '').replace('\n', self.symbols["Wall"]+'\n'+self.symbols["Wall"])+self.symbols["Wall"]+"\n"+((self.dim*2)+1)*self.symbols["Wall"]+"\n"
    
    def visualize(self, show_gridworld=False,show_rewardworld=False,show_mergeworld=False):
        if show_gridworld:
            # Show GW
            
            print("Gridworld:")
            viz=self.grid_world.reshape(((self.dim, self.dim)))
            print(self.create_visual_border(viz))
            print("\n")

        if show_rewardworld:
            # Show RW

            print("Rewardworld:")
            viz=self.reward_world.reshape(((self.dim, self.dim)))
            print(self.create_visual_border(viz))
            print("\n")
        
        if show_mergeworld:
            print("Merge-World")
            merge_copy=copy.deepcopy(self.reward_world)
            merge_copy[self.get_player_idx()]=self.symbols["Player"]
            
            viz=merge_copy.reshape(((self.dim, self.dim)))
            print(self.create_visual_border(viz))
            print("\n")
        pass
    
    def get_player_idx(self):
        return np.where(self.grid_world == self.symbols["Player"])[0][0]

    def get_target_idx(self):
        return np.where(self.reward_world == "+")[0][0]
