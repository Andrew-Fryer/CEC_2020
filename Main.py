import Env

env = Env.Env("easy.txt")

print(env.blockAt(0,0))

print(env.stateEquals(env.dState))
print(env.stateEquals(env.state))
print(env.done())


print(env.getSize())
env.plot_state()


print("done")
