from simulator import Simulator
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
        for y in range(simulator.height):
            for x in range(simulator.width):
                char = " "
                if (x, y) in simulator.agents:
                    agent = simulator.agents[(x, y)]
                    if agent.strategy == "cooperate":
                        char = "+"
                    elif agent.strategy == "defect":
                        char = "-"
                window.addch(y, x, char)
        self.show_stats(window, y, simulator.coop_count, simulator.defect_count)
        curses.napms(900)

    def show_stats(self, window, row, coop_count, defect_count):
        total_alive = coop_count + defect_count
        coop_size = int((coop_count / total_alive) * self.BAR_WIDTH)
        defect_size = int((defect_count / total_alive) * self.BAR_WIDTH)
        coop_bar = ("=" * coop_size) + (" " * (self.BAR_WIDTH - coop_size))
        defect_bar = ("=" * defect_size) + (" " * (self.BAR_WIDTH - defect_size))

        window.addstr(row + 1, 0, "_" * (self.BAR_WIDTH + 7))
        window.addstr(row + 2, 0, "KIND [" + coop_bar + "]")
        window.addstr(row + 3, 0, "MEAN [" + defect_bar + "]")
        window.addstr(row + 4, 0, f"TOTAL KIND: {coop_count}")
        window.addstr(row + 5, 0, f"TOTAL MEAN: {defect_count}")
        window.refresh()
