import math

#Drone class
#Needs the env object passed into on initialization for environment reference
class Drone:
    def __init__(self, env, pos):
        self.env = env

        if (pos != None):
            self.pos = [pos[0], pos[1]]
        else:
            self.pos = [0, 0]

        self.time = 0

        self.hopper = []
        self.hopperSize = (int)(math.floor(pow(pow(self.env.getSize(), 3), 0.5)/2))
        self.lastColour = ""

        self.memory = []
        #Initializing drone's memory of environment to zero
        for i in range(self.env.getSize()):
            toAddi = []
            for j in range(self.env.getSize()):
                toAddj = []
                for k in range(self.env.getSize()):
                    toAddj.append(None)
                toAddi.append(toAddj)
            self.memory.append(toAddi)

    #Moves the drone in a given direction, updates the time taken
    def move(self, direction): #0 is up, 1 is right, 2 is down, 3 is left
        if (direction == 0):
            if self.pos[1] >= self.env.s - 1:
                return None
            self.pos[1] += 1
        elif (direction == 1):
            if self.pos[0] >= self.env.s - 1:
                return None
            self.pos[0] += 1
        elif (direction == 2):
            if self.pos[1] <= 0:
                return None
            self.pos[1] += -1
        elif (direction == 3):
            if self.pos[0] <= 0:
                return None
            self.pos[0] += -1
        else:
            print("invalid direction")
        self.time += 1
        self.scan()
        return True
    def moveTo(self, target):
        xDiff = target[0] - self.pos[0]
        yDiff = target[1] - self.pos[1]
        for i in range(abs(xDiff)):
            if (xDiff < 0):
                self.move(3)
            else:
                self.move(1)
        for i in range(abs(yDiff)):
            if (yDiff < 0):
                self.move(2)
            else:
                self.move(0)

    #Picks up a block in the environment at the current position, updates time
    def pickUp(self):
        if (len(self.hopper) < self.hopperSize): #if there is room in the hopper, pick up block
            toAdd = self.env.takeBlock(self.pos[0], self.pos[1])  # (colour, z)
            if (toAdd == None):  # if there is an error exit
                return None

            newColour = toAdd[0]
            self.hopper.append(newColour) #add to hopper

            #Update time
            if (newColour == self.lastColour):
                self.time += 2
            else:
                self.time += 3

            self.lastColour = newColour
            self.scan()
            return True

    #Drops off a block in the environment at the current position at a given z value
    def dropOff(self, colour, z):
        toRemove = None
        inHopper = False
        for i in self.hopper: #block needs to be in hopper to drop off
            if (i == colour):
                toRemove = i
                inHopper = True
                break
        if (inHopper == False): #If the block is not in the hopper
            return None

        newZ = z
        if (z == -1):
            newZ = self.env.blockAt(self.pos[0], self.pos[1])[1] + 1
        #Add block to grid and memory

        test = self.env.addBlock(self.pos[0], self.pos[1], (toRemove, newZ))

        if (test == None):
            print("add block failed")
            return None

        #Update time
        if (colour == self.lastColour):
            self.time += 2
        else:
            self.time += 3

        self.lastColour = colour
        self.memory[self.pos[0]][self.pos[1]][newZ] = toRemove
        self.scan()
        self.hopper.remove(toRemove) #Remove block from hopper
        return True

    #Scans the block below the drone
    def scan(self):
        block = self.env.blockAt(self.pos[0], self.pos[1])
        if block is None:
            block = ["", -1]
        for z in range(self.env.getSize() - 1, block[1], -1):
            self.memory[self.pos[0]][self.pos[1]][z] = None
        if block is not None:
            self.memory[self.pos[0]][self.pos[1]][block[1]] = block[0]
        return block

    def isHopperFull(self):
        return len(self.hopper) >= self.hopperSize

    def getHopperColours(self):
        out = []
        for i in self.hopper:
            if (i not in out):
                out.append(i)
        return out
