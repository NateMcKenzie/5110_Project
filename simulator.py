from copy import deepcopy
from enum import Enum
import math

from logger import Logger


class CellState(Enum):
    DEAD = 0
    KIND = 1
    MEAN = 2


class Simulator:
    def __init__(self, width: int, height: int, exit: (int, int)):
        self.width = width
        self.height = height
        self.__exit = exit

        self.__board = [[CellState.DEAD for x in range(width)] for y in range(height)]
        self.__distances = []
        for x in range(width):
            self.__distances.append([])
            for y in range(height):
                distance = math.sqrt((exit[0] - x) ** 2 + (exit[1] - y) ** 2)
                self.__distances[-1].append(distance)

        # Stats and logging
        self.kind_count = 0
        self.mean_count = 0
        self.logger = Logger("log.txt")

    def update(self):
        # Put in Conway's Game of Life for now to see how it works
        swap_board = deepcopy(self.__board)

        for row in range(self.height):
            for col in range(self.width):
                neighbors = 0
                for col_neighbor in range(-1, 2):
                    for row_neighbor in range(-1, 2):
                        if not (row_neighbor == 0 and col_neighbor == 0):
                            neighbor_cell = self.getCell(
                                col + col_neighbor, row + row_neighbor
                            )
                            if neighbor_cell != CellState.DEAD:
                                neighbors += 1

                if self.getCell(col, row) != CellState.DEAD and neighbors < 2:
                    swap_board[row][col] = CellState.DEAD
                elif self.getCell(col, row) != CellState.DEAD and neighbors > 3:
                    swap_board[row][col] = CellState.DEAD
                elif self.getCell(col, row) == CellState.DEAD and neighbors == 3:
                    swap_board[row][col] = CellState.MEAN

        self.__board = swap_board
        self.count_states()
        self.logger.logStep(self.kind_count, self.mean_count)

    def setCell(self, x: int, y: int, state: CellState):
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.__board[y][x] = state

    def getCell(self, x: int, y: int):
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.__board[y][x]
        return CellState.DEAD

    def getDistance(self, x: int, y: int):
        if (0 <= x < self.width) and (0 <= y < self.height):
            return self.__distances[y][x]
        return float("inf")

    # Can do this as we go, but it gets a little clunky with the swap board and everything.
    # This is Python so who cares about one more count.
    def count_states(self):
        self.kind_count = 0
        self.mean_count = 0
        for row in self.__board:
            for cell in row:
                if cell == CellState.MEAN:
                    self.mean_count += 1
                elif cell == CellState.KIND:
                    self.kind_count += 1


