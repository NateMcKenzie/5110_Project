from simulator import Simulator, CellState
import curses

class FancyRenderer:
    BAR_WIDTH = 50
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
        self.show_stats(row, kind_count, mean_count)
        curses.napms(1000)

    def show_stats(self, row, kind_count, mean_count):
        total_alive = kind_count + mean_count
        kind_size = int((kind_count / total_alive) * self.BAR_WIDTH)
        mean_size = int((mean_count / total_alive) * self.BAR_WIDTH)
        kind_bar = ("=" * kind_size) + (" " * (self.BAR_WIDTH - kind_size))
        mean_bar = ("=" * mean_size) + (" " * (self.BAR_WIDTH - mean_size))

        self.window.addstr(row+1, 0, "_" * (self.BAR_WIDTH + 7))
        self.window.addstr(row+2, 0, "KIND [" + kind_bar + "]")
        self.window.addstr(row+3, 0, "MEAN [" + mean_bar + "]")
        self.window.addstr(row+4, 0, f"TOTAL KIND: {kind_count}")
        self.window.addstr(row+5, 0, f"TOTAL MEAN: {mean_count}")
        self.window.refresh()
