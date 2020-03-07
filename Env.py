from asyncore import file_dispatcher

import pandas as pd

# add desired grid

class Env:
    def __init__(self, filename):
        with open(filename, "r") as f:
            # I'm assuming the file could be sparse

            lines = [l for l in f.read().splitlines() if l != ""]
            assert lines[0] == "unscrambled_image"
            assert lines[1][0:5] == "size="
            size = int(lines[1][5:])

            index = lines.index("scrambled_image")

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

            state = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
            for l in lines[2:index]:
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
        # wip
        for x in range(self.s):
            for y in range(self.s):
                for z in range(self.s):
                    if self.dState[x][y][z] != mem[x][y][z]:
                        return False
        return True

    def done(self):
        # wip
        for x in range(self.s):
            for y in range(self.s):
                for z in range(self.s):
                    if self.state[x][y][z] != self.dState[x][y][z]:
                        return False
        return True

    def blockAt(self, x, y):
        for z in reversed(range(self.s)):
            if self.state[x][y][z] != "":
                return self.state[x][y][z], z
        return None

    def getSize(self):
        return self.s

    def addBlock(self, x, y, tuple):
        # wip
        color = tuple[0]
        z = tuple[1]


    def takeBlock(self, x, y):
        # return none if we can't take...
        #wip
        for z in reversed(range(self.s)):
            if self.state[x][y][z] != "":
                color = self.state[x][y][z]
                self.state[x][y][z] = ""
                return color, z
        return "", 0

