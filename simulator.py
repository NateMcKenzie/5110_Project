from copy import deepcopy
from enum import Enum
import math


class CellState(Enum):
    DEAD = 0
    KIND = 1
    MEAN = 2


class Simulator:
    def __init__(self, width: int, height: int, exit: (int,int)):
        self.width = width
        self.height = height
        self.__exit = exit
        
        self.__board = []
        for x in range(width):
            self.__board.append([])
            for y in range(height):
                distance = math.sqrt((exit[0] - x)**2 + (exit[1] - y)**2)
                self.__board[-1].append([CellState.DEAD, distance])

    def update(self):
        pass
        # Go through each cell
            # If there is a person there (KIND or MEAN)
                # Assign probabilities to cells around them according to distance to exit
                # TODO: Should probably pre-calculate and store these distances in the board itself
                # Randomly pick one to go to
                # Somehow indicate that this cell has +1 KIND/MEAN trying to enter it
        # Go through cells again
            # Determine who is trying to come into cell
                # If no one: change nothing.
                # If one person: They come in.
                # If multiple KIND people: They have equal chance of moving in.
                # If 1 MEAN and some KIND: MEAN goes in.
                # If multiple MEAN: They have probability of moving in.
            # Mark cell coming from as DEAD, mark cell moving to according to winner.
            # Those who don't win have to re-evaluate if they should be MEAN or KIND

    def setCell(self, x: int, y: int, state: CellState):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.__board[y][x][0] = state

    def getCell(self, x: int, y: int):
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.__board[y][x]
        return CellState.DEAD
