from simulator import Simulator, CellState
import curses


class FancyRenderer:
    BAR_WIDTH = 50

    def __init__(self):
        curses.initscr()
        curses.curs_set(0)  # 0=invisible

    def render(self, simulator: Simulator):
        curses.wrapper(self.wrapped_render, simulator)

    def wrapped_render(self, window, simulator: Simulator):
        window.clear()
        for row in range(simulator.height):
            for col in range(simulator.width):
                cell_state = simulator.getCell(col, row)
                char = " "
                match cell_state:
                    case CellState.KIND:
                        char = "+"
                    case CellState.MEAN:
                        char = "-"
                window.addch(row, col, char)
        self.show_stats(window, row, simulator.kind_count, simulator.mean_count)
        curses.napms(900)

    def show_stats(self, window, row, kind_count, mean_count):
        total_alive = kind_count + mean_count
        kind_size = int((kind_count / total_alive) * self.BAR_WIDTH)
        mean_size = int((mean_count / total_alive) * self.BAR_WIDTH)
        kind_bar = ("=" * kind_size) + (" " * (self.BAR_WIDTH - kind_size))
        mean_bar = ("=" * mean_size) + (" " * (self.BAR_WIDTH - mean_size))

        window.addstr(row + 1, 0, "_" * (self.BAR_WIDTH + 7))
        window.addstr(row + 2, 0, "KIND [" + kind_bar + "]")
        window.addstr(row + 3, 0, "MEAN [" + mean_bar + "]")
        window.addstr(row + 4, 0, f"TOTAL KIND: {kind_count}")
        window.addstr(row + 5, 0, f"TOTAL MEAN: {mean_count}")
        window.refresh()
