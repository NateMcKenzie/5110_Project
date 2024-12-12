from simulator import Simulator

import curses
import time


class FancyRenderer:
    BAR_WIDTH = 50

    def __init__(self, width, height):
        curses.initscr()
        if curses.LINES < height + 6:
            curses.endwin()
            raise RuntimeError(f"Your terminal only has {curses.LINES} lines. Fancy rendering this file requires {height + 6}")
        curses.cbreak()
        curses.curs_set(0)  # 0=invisible
        self.last_render = int(time.time())

    def render(self, simulator: Simulator, round_count):
        curses.wrapper(self.wrapped_render, simulator, round_count)

    def wrapped_render(self, window, simulator: Simulator, round_count):
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
                elif (x, y) in simulator.obstacles:
                    char = "o"
                elif (x, y) in simulator.exits:
                    char = "/"
                window.addch(y, x, char)
        if simulator.over:
            window.addstr(simulator.height + 1, 0, f"ALL AGENTS EXITED IN {round_count} steps")
            window.refresh()
            curses.napms(4000)
            return

        self.show_stats(window, y, simulator.coop_count, simulator.defect_count, len(simulator.evacuated))

        now = int(time.time())
        curses.napms(800 - (self.last_render - now))
        self.last_render = now

    def show_stats(self, window, row, coop_count, defect_count, evac_count):
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
        window.addstr(row + 6, 0, f"EVACUATED: {evac_count}")
        window.refresh()
