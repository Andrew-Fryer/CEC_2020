import numpy as np
from drone import Drone


class Algorithm:
    def __init__(self, grid):
        # all of these lists will be for instances of the classes
        self.correct = []  # which z=0 positions are in the correct place
        self.stacks = dict.fromkeys(['x', 'y', 'z'], 0)
        self.emptySpaces = []  # empty space available.
        self.unknown = []  # list of 2d visualization with which ones are stacks we don't know below

        self.drone = Drone(grid, [0, 0])

    def build_stacks(self):
        pass

    def build_z_stack(self, z):
        for i in range(z, -1, -1):

        
