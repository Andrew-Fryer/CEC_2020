from Env import Env
from blocks import Algorithm

def print_a():
    print("Correct:", a.correct)
    print("Stacks:", a.stacks)
    print("Empty Spaces:", a.emptySpaces)
    print("Unknown:", a.unknown)
    print("Colour Stacks:", a.colourStacks)
    print()
    print("------------------------------------------------------------------")
    print()

env = Env("easy.txt")
a = Algorithm(env)

print_a()
a.first_sweep()
print_a()
for i in range(1, a.grid.getSize()):
    a.build_z_stack(i)
#    print_a()
a.empty_hopper()
print_a()
a.build_final()