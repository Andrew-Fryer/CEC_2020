from drone import Drone

class Algorithm:
    def __init__(self, grid):
        self.grid = grid
        # all of these lists will be for instances of the classes
        self.correct = []  # which z=0 positions are in the correct place
        self.stacks = [] #dict.fromkeys(['x', 'y', 'z'], 0)
        self.fullStacks = []
        self.emptySpaces = []  # empty space available.
        self.unknown = []  # list of 2d visualization with which ones are stacks we don't know below
        self.toStack = []
        self.colourStacks = []

        self.drone = Drone(grid, [0, 0])
        
    def first_sweep(self):
        size = self.grid.getSize()
        i = 0
        j = 0
        di = 1
        dj = 0
        it = 0
        for n in range(size ** 2):
            self.drone.moveTo([i, j])
#            print([i, j], self.drone.pos)
            b = self.drone.scan()
            dB = self.grid.desiredBlockAt(i, j)
#            print(i, j, b)
            if (b[0] == ''):
                temp = {'x': i, 'y': j, 'z': -1}
                self.emptySpaces.append(temp)
            else:
                temp = {'x': i, 'y': j, 'z': b[1]}
                if (b == dB and b[1] == 0 and b[0] not in self.colourStacks):
                    self.correct.append(temp)
                    self.stacks.append(temp)
                    self.colourStacks.append(b[0])
                else:
                    self.unknown.append(temp)
                    
            #makes drone spiral
            i += di
            j += dj
            if (i >= size - it - 1 and di == 1):
                di = 0
                dj = 1
            if (j >= size - it - 1 and dj == 1):
                di = -1
                dj = 0
            if (i < it + 1 and di == -1):
                di = 0
                dj = -1
            if (j < it + 2 and dj == -1):
                di = 1
                dj = 0
                it += 1
                
    def closestStack(self):
        stacks = self.stacks
        drone = self.drone
        distance = []
        orderedStack = []
        for i in range(0, len(stacks)):
            distance.append(abs(drone.pos[0] - stacks[i]['x'] +
                                drone.pos[1] - stacks[i]['y']))
        distanceSorted = sorted(distance)
        for j in range(0, len(stacks)):
            orderedStack.append(stacks[distance.index(distanceSorted[j])])
        return orderedStack
                                
    def empty_hopper(self):
        colours = self.drone.getHopperColours()
        for c in colours:
            colourDropped = False
            for s in self.stacks:
                if (self.grid.blockAt(s['x'], s['y'])[0] == c):
                    self.drone.moveTo([s['x'], s['y']])
                    self.drone.scan()
                    full = self.drone.dropOff(c, -1)
                    if (full == 10):
                        self.fullStacks.append(s)
                        self.stacks.remove(s)
                        if (len(self.emptySpaces) > 0):
                            newStack = self.emptySpaces[0]
                        else:
                            newStack = self.correct[0]
                        temp = {'x': newStack['x'], 'y': newStack['y'], 'z': newStack['z']}
                        self.stacks.append(temp)
                        self.drone.moveTo([temp['x'], temp['y']])
                        self.drone.dropOff(c, -1)
                    self.drone.scan()
                    colourDropped = True
                    break
            if (colourDropped == False and len(self.emptySpaces) > 0):
                newStack = self.emptySpaces[0]
                self.emptySpaces.remove(newStack)
                self.stacks.append(newStack)
                self.colourStacks.append(c)
                self.drone.moveTo([newStack['x'], newStack['y']])
                self.drone.scan()
                self.drone.dropOff(c, -1)
                self.drone.scan()

    def build_stacks(self):
        self.first_sweep()
        for i in range(1, self.grid.getSize()):
            self.build_z_stack(i)

    def build_z_stack(self, z): #idea, sort lists by shortest distance from drone
        for n in range(z, -1, -1): #loop through all lower z cases
            for i in self.unknown: #check all unknown spaces 
                if (i['z'] == n):  #check only those unknown spaces for specific z values
                    #move drone, pickup block, and scan
                    self.drone.moveTo([i['x'], i['y']]) 
                    pickedUp = self.drone.pickUp()
                    if (pickedUp == True):
                        if (self.grid.blockAt(i['x'], i['y'])[0] == ''):
                            self.emptySpaces.append(i)
                            self.stacks.append(i)
                            self.unknown.remove(i)
                        elif (self.grid.blockAt(i['x'], i['y'])[1] == 1):
                            self.toStack.append(i)
                            self.unknown.remove(i)
                    self.drone.scan()
                    
                    #if hopper is full, empty it
                    if (self.drone.isHopperFull()): #drop off blocks, NEED TO ACCOUNT FOR IF STACK IS FULL
                        self.empty_hopper()
            for i in self.toStack:
                if (self.drone.isHopperFull()):
                    self.empty_hopper()
                self.drone.moveTo([i['x'], i['y']])
                pickedUp = self.drone.pickUp()
                if (pickedUp == True):
                    for s in self.stacks:        
                        if (self.grid.blockAt(s['x'], s['y'])[0] == self.grid.blockAt(i['x'], i['y'])[0]):
                            self.drone.moveTo([s['x'], s['y']])
                            self.drone.dropOff(self.grid.blockAt(i['x'], i['y'])[0], -1)
                            break
                    self.toStack.remove(i)
                    
    
    def build_final(self):
        for z in range(self.grid.getSize()):
            level_blocks = self.grid.getDesiredLevel(z)
            for b in level_blocks:
                if (self.drone.memory[b[0]][b[1]] == None):
                    if (b[2] in self.hopper):
                        self.drone.moveTo([b[0], b[1]])
                        self.drone.dropOff(b[2], z)
                    else:
                        for s in self.stacks:
                            if (self.grid.blockAt(s['x'], s['y'])[0] == b[2]):
                                self.drone.moveTo([s['x'], s['y']])
                                self.drone.pickUp()
                                self.drone.moveTo(b[0], b[1])
                                self.drone.dropOff(b[2], z)
                                break
                        for s in self.full_stacks:
                            if (self.grid.blockAt(s['x'], s['y'])[0] == b[2]):
                                self.drone.moveTo([s['x'], s['y']])
                                self.drone.pickUp()
                                self.drone.moveTo(b[0], b[1])
                                self.drone.dropOff(b[2], z)
                                break
                            
                    
        
