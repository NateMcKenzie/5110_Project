from simulator import Simulator, CellState


class FancyRenderer:
    def render(self, simulator: Simulator):
        move_cursor(0,0)
        print("abc")

    def move_cursor(x: int, y: int):
        print(f"\033[<{y}>;<{x}>f")
