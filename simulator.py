class Simulator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[CellState.DEAD] * width] * height


class CellState(Enum):
    DEAD = 0
    KIND = 1
    MEAN = 2
