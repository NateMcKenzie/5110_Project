from simulator import Simulator, CellState
import curses


class FancyRenderer:
    def __init__(self):
        self.window = curses.initscr()

    def render(self, simulator: Simulator):
        debug = open("debug", "w")
        self.window.clear()
        for row in range(simulator.height):
            for col in range(simulator.width):
                char = simulator.getCell(col, row)
                print(char, file=debug)
                self.window.addch(row, col, " " if char[0] is CellState.DEAD else "o")
        debug.close()
        self.window.refresh()
