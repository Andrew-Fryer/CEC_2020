import math

class Drone:    
    def __init__(self, grid):
        self.grid = grid
        
        self.pos = [0, 0]
        self.time = 0
        
        self.hopper = []
        self.hopperSize = (int)(math.floor(pow(self.grid.getSize(), 0.5)/2))
        self.lastColour = ""
        
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
    
    def pickUp(self):
        toAdd = self.grid.takeBlock(self.pos[0], self.pos[1]) #(colour, z)
        if (toAdd == None):
            return
        if (len(self.hopper) < self.hopperSize):
            self.hopper.append(toAdd)
            newColour = toAdd[0]
            if (newColour == self.lastColour):
                self.time += 2
            else:
                self.time += 3
    
    def dropOff(self, colour, z):
        toRemove = None
        for i in self.hopper:
            if (i[0] == colour and i[1] == z):
                toRemove = i
                break
        
        self.hopper.remove(toRemove)
        self.grid.addBlock(self.pos[0], self.pos[1], toRemove)
                
            