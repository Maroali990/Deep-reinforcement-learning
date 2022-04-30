import gridworld
import n_sarsa
import os

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


"""# Move
_,k,b = gw.move("down")
# Show GW
gw.visualize()
print("Reward: " + str(b))
print("Finished: " + str(k))

# define actionspace
action_space=[0,1,2,3]
dict_moves={0:"left",1:"right",2:"up",3:"down"}

sarsa=n_sarsa.sarsa(dim*dim,action_space)"""



"""for timestep in range(20):
    #clear screen
    if os.name == 'posix': #Linux, Mac
        os.system('clear')
    else: #Windows
        os.system('cls')
    print()
    input("Next action")
    action=sarsa.choose_action()
    gw.move(action)
    gw.visualize()"""