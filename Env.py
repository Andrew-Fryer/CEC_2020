from asyncore import file_dispatcher

import pandas as pd

# add desired grid

class Env:
    def __init__(self, filename):
        with open(filename, "r") as f:
            # I'm assuming the file could be sparse

            lines = [l for l in f.read().splitlines() if l != ""]
            index = lines.index("scrambled_image")


            assert lines[0] == "unscrambled_image"
            assert lines[1][0:5] == "size="
            size = int(lines[1][5:])
            desiredState = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
            for l in lines[2:index]:
                # add to state
                eIndex = l.index("=")
                pos = l[:eIndex]
                posStr = pos.split(",")
                x = int(posStr[0])
                y = int(posStr[1])
                z = int(posStr[2])

                color = l[eIndex+1:].strip("\"")

                desiredState[x][y][z] = color

            assert lines[index] == "scrambled_image"
            assert lines[index+1][0:5] == "size="
            dSize = int(lines[index+1][5:])
            assert dSize == size
            state = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
            for l in lines[index+2:]:
                # add to state
                eIndex = l.index("=")
                pos = l[:eIndex]
                posStr = pos.split(",")
                x = int(posStr[0])
                y = int(posStr[1])
                z = int(posStr[2])

                color = l[eIndex + 1:].strip("\"")

                state[x][y][z] = color

            self.state = state
            self.dState = desiredState
            self.s = size

    def stateEquals(self, mem):
        return self.state == mem

    def done(self):
        return self.state == self.dState

    def blockAt(self, x, y):
        for z in reversed(range(self.s)):
            if self.state[x][y][z] != "":
                return self.state[x][y][z], z
        return None # default could be "", -1

    def getSize(self):
        return self.s

    def addBlock(self, x, y, tuple):
        # wip
        color = tuple[0]
        z = tuple[1]

        # check if the block will be floating
        bAt = self.blockAt(x,y)
        if bAt is None:
            existingZ = -1
        else:
            _, existingZ = bAt
        if z != existingZ + 1:
            if z <= existingZ:
                print("Can't place block beneath another block", x, y, z, existingZ)
                return None
            print("warning, you are placing a floating block")

            # check that the block will have at least 1 neighbor to support it
            leftN = False if x == 0 else self.state[x-1][y][z] != ""
            rightN = False if x == self.s - 1 else self.state[x+1][y][z] != ""
            upN = False if y == self.s - 1 else self.state[x][y+1][z] != ""
            downN = False if y == 0 else self.state[x][y-1][z] != ""

            if (not leftN) and (not rightN) and (not upN) and (not downN):
                print("No neightbors to support")
                return None

        # add block in
        self.state[x][y][z] = color
        return True # success






    def takeBlock(self, x, y):
        # return none if we can't take...
        #wip
        for z in reversed(range(self.s)):
            if self.state[x][y][z] != "":
                color = self.state[x][y][z]
                self.state[x][y][z] = ""
                return color, z
        return "", 0

