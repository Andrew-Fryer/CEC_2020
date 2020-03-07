import Env

env = Env.Env("easy.txt")

print(env.blockAt(0,0))

print(env.stateEquals(env.dState))
print(env.stateEquals(env.state))
print(env.done())

print(env.getSize())
print()

print(env.addBlock(0, 0, ("red", 0))) # under existing block
print(env.addBlock(0, 0, ("red", 4))) # floating
print(env.addBlock(0, 0, ("red", 3))) # nice :)
print(env.addBlock(1, 1, ("red", 0))) # no blocks here yet, but nice :)
print(env.addBlock(1, 1, ("red", 2))) # floating, but works
print(env.addBlock(0, 20, ("red", 3))) # out of bounds
print()

print(env.takeBlock(1, 1)) # take that floating red block
print(env.takeBlock(1, 1)) # take that first red block
print(env.takeBlock(1, 1)) # no block to take
# TODO: take one that is surrounded

print("done")

