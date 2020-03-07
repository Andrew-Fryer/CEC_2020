from drone import Drone

class Algorithm:
    def __init__(self, grid):
        self.grid = grid
        # all of these lists will be for instances of the classes
        self.correct = []  # which z=0 positions are in the correct place
        self.stacks = [] #dict.fromkeys(['x', 'y', 'z'], 0)
        self.emptySpaces = []  # empty space available.
        self.unknown = []  # list of 2d visualization with which ones are stacks we don't know below
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
            b, dB = self.drone.scan()
            if (b == None):
                temp = {'x': i, 'y': j, 'z': -1}
                self.emptySpaces.append(temp)
            else:
                temp = {'x': i, 'y': j, 'z': b[1]}
                if (b == dB and b[1] == 0 and b[0] not in self.colourStacks):
                    self.correct.append(temp)
                    self.stacks.append(temp)
                    self.colourStacks.append(b[0])
                else:
                    temp.z = -1
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
                                
    def empty_hopper(self):
        colours = self.drone.getHopperColours()
        for c in colours:
            colourDropped = False
            for s in self.stacks:
                if (self.grid.blockAt(s.x, s.y) == c):
                    self.drone.moveTo([s.x, s.y])
                    self.drone.scan()
                    self.drone.dropOff(c, -1)
                    self.drone.scan()
                    colourDropped = True
                    break
            if (colourDropped == False and len(self.emptySpaces) > 0):
                newStack = self.emptySpaces[0]
                self.emptySpaces.remove(newStack)
                self.stacks.append(newStack)
                self.colourStacks.append(c)
                self.drone.moveTo([newStack.x, newStack.y])
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
                if (i.z == n):  #check only those unknown spaces for specific z values
                    #move drone, pickup block, and scan
                    self.drone.moveTo([i.x, i.y]) 
                    notPickedUp = self.drone.pickUp()
                    if (notPickedUp == False):
                        if (self.grid.blockAt(i.x, i.y) == None):
                            self.emptySpaces.append(i)
                            self.stacks.append(i)
                            self.unknown.remove(i)
                    self.drone.scan()
                    
                    #if hopper is full, empty it
                    if (self.drone.isHopperFull()): #drop off blocks, NEED TO ACCOUNT FOR IF STACK IS FULL
                        empty_hopper()
    
    def build_final(self):
        for z in range(self.grid.getSize()):
            level_blocks = self.grid.getDesiredLevel(z)
            for b in level_blocks:
                if (b[2] in self.hopper):
                    self.drone.moveTo([b[0], b[1]])
                    self.drone.dropOff(b[2], z)
                else:
                    for s in self.stacks:
                        if (self.grid.blockAt(s.x, s.y) == b[2]):
                            self.drone.moveTo([s.x, s.y])
                            self.drone.pickUp()
                            self.drone.moveTo(b[0], b[1])
                            self.drone.dropOff(b[2], z)
                            break
                            
                    
        
