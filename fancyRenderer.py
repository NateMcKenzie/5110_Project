from simulator import Simulator, CellState
import curses


class FancyRenderer:
    def __init__(self):
        self.window = curses.initscr()
        curses.curs_set(0) # 0=invisible

    def render(self, simulator: Simulator):
        self.window.clear()
        for row in range(simulator.height):
            for col in range(simulator.width):
                char = simulator.getCell(col, row)
                self.window.addch(row, col, " " if char is CellState.DEAD else "o")
        self.window.refresh()
        curses.napms(300)
