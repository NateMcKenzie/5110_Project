from simulator import Simulator, CellState
import curses


class FancyRenderer:
    def __init__(self):
        self.window = curses.initscr()
        curses.curs_set(0) # 0=invisible

    def render(self, simulator: Simulator):
        self.window.clear()
        kind_count = 0
        mean_count = 0
        for row in range(simulator.height):
            for col in range(simulator.width):
                cell_state = simulator.getCell(col, row)
                char = " "
                match cell_state:
                    case CellState.KIND:
                        kind_count += 1
                        char = "+"
                    case CellState.MEAN:
                        mean_count += 1
                        char = "-"
                self.window.addch(row, col, char)
        total_cells = simulator.height * simulator.width
        self.window.addstr(row+1, 0, "0" * int(kind_count/total_cells * 100 * 4))
        self.window.addstr(row+2, 0, "0" * int(mean_count/total_cells * 100 * 4))
        self.window.addstr(row+3, 0, f"TOTAL KIND: {kind_count}")
        self.window.addstr(row+4, 0, f"TOTAL MEAN: {mean_count}")
        self.window.refresh()
        curses.napms(1000)
