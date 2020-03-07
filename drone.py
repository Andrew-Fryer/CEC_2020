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
        self.desiredMemory = []
        #Initializing drone's memory of environment to zero
        for i in range(self.env.getSize()):
            toAddi = []
            toAddiD = []
            for j in range(self.env.getSize()):
                toAddj = []
                toAddjD = []
                for k in range(self.env.getSize()):
                    toAddj.append(None)
                    toAddjD.append(None)
                toAddi.append(toAddj)
                toAddiD.append(toAddjD)
            self.memory.append(toAddi)
            self.desiredMemory.append(toAddiD)

    #Moves the drone in a given direction, updates the time taken
    def move(self, direction): #0 is up, 1 is right, 2 is down, 3 is left
        self.time += 1
        if (direction == 0):
            self.pos[1] += 1
        elif (direction == 1):
            self.pos[0] += 1
        elif (direction == 2):
            self.pos[1] += -1
        elif (direction == 3):
            self.pos[0] += -1
        else:
            self.time += -1

    def moveTo(self, target):
        while (self.pos[0] != target[0] and self.pos[1] != target[1]):
            xDiff = target[0] - self.pos[0]
            if (xDiff > 0):
                self.move(1)
            elif (xDiff < 0):
                self.move(3)
            else:
                yDiff = target[1] - self.pos[1]
                if (yDiff > 0):
                    self.move(0)
                elif (yDiff < 0):
                    self.move(2)

    #Picks up a block in the environment at the current position, updates time
    def pickUp(self):
        toAdd = self.env.takeBlock(self.pos[0], self.pos[1]) #(colour, z)
        if (toAdd == None): #if there is an error exit
            return True
        if (len(self.hopper) < self.hopperSize): #if there is room in the hopper, pick up block
            self.hopper.append(toAdd[0]) #add to hopper

            #Update time
            newColour = toAdd[0]
            if (newColour == self.lastColour):
                self.time += 2
            else:
                self.time += 3

            self.lastColour = newColour
            self.memory[self.pos[0]][self.pos[1]][toAdd[1]] = None
            return False
        else:
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
            return True
        self.hopper.remove(toRemove) #Remove block from hopper

        newZ = z
        if (z == -1):
            newZ = self.grid.blockAt(self.pos[0], self.pos[1])[1] + 1
        if (newZ >= self.grid.getSize()):
            return True
        #Add block to grid and memory
        test = self.grid.addBlock(self.pos[0], self.pos[1], (toRemove, newZ))
        newZ = self.env.blockAt(self.pos[0], self.pos[1])[1] + 1
        if (newZ >= self.env.getSize()):
            return
        #Add block to env and memory
        test = self.env.addBlock(self.pos[0], self.pos[1], (toRemove, newZ))
        if (test != None):
            #Update time
            if (colour == self.lastColour):
                self.time += 2
            else:
                self.time += 3

            self.lastColour = colour
            self.memory[self.pos[0]][self.pos[1]][newZ] = toRemove[0]
            return False
        else:
            return True

    #Scans the block below the drone
    def scan(self):
        block = self.env.blockAt(self.pos[0], self.pos[1])
        self.memory[self.pos[0]][self.pos[1]][block[1]] = block[0]
        desiredBlock = self.env.desiredBlockAt(self.pos[0], self.pos[1])
        self.desiredMemory[self.pos[0]][self.pos[1]][desiredBlock[1]] = desiredBlock[0]
        return block, desiredBlock

    def isHopperFull(self):
        return len(self.hopper) >= self.hopperSize

    def getHopperColours(self):
        out = []
        for i in self.hopper:
            if (i not in out):
                out.append(i)
        return out
