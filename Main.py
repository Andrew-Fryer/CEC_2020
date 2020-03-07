import Env

env = Env.Env("easy.txt")

print(env.blockAt(0,0))

print(env.stateEquals(env.dState))
print(env.stateEquals(env.state))
print(env.done())



## Joe's Experimental Zone - Do Not Touch

print(env.getSize())
env.plot_state(env.state_dataFrame)

## Joe's Experimental Zone - Do Not Touch

print("done")
 
