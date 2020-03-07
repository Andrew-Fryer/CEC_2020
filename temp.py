import numpy as np


def closestStack(stacks, drone):
    distance = []
    for i in len(stacks):
        distance[i] = abs(drone.x - stacks[i].x + drone.y - stacks[i].y)
    stackIndex = distance.index(min(distance))
    return stackIndex
