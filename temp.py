import numpy as np

stacks = []
stacks.append({'x': 5, 'y': 5})
stacks.append({'x': 6, 'y': 6})
drone = {'x': 3, 'y': 0}


def closestStack(stacks, drone):
    distance = []
    orderedStack = []
    for i in range(0, len(stacks)):
        distance.append(abs(drone['x'] - stacks[i]['x'] +
                            drone['y'] - stacks[i]['y']))
    distanceSorted = sorted(distance)
    for j in range(0, len(stacks)):
        orderedStack.append(stacks[distance.index(distanceSorted[j])])
    return orderedStack


print(closestStack(stacks, drone))
