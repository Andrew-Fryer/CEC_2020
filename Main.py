import Env
from drone import Drone 

env = Env.Env("easy.txt")

print(env.blockAt(0,0))

print(env.stateEquals(env.dState))
print(env.stateEquals(env.state))
print(env.done())


## Joe's Experimental Zone - Do Not Touch

print(env.getSize())
theDrone = Drone(env, None) 
env.plot_state(theDrone)

## Joe's Experimental Zone - Do Not Touch

print("done")

