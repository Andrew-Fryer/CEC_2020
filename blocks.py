import numpy as np


class Algorithm:
    def __init__(self):
        # all of these lists will be for instances of the classes
        self.correct = []  # which z=0 positions are in the correct place
        self.stacks = dict.fromkeys(['x', 'y', 'z'], 0)
        self.emptySpaces = []  # empty space available.
        self.unknown = []  # list of 2d visualization with which ones are stacks we don't know below
