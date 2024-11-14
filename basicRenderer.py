from simulator import Simulator, CellState


class BasicRenderer:
    def render(self, simulator: Simulator):
        character = ""
        for row in range(simulator.height):
            for col in range(simulator.width):
                match (simulator.getCell(col, row)):
                    case CellState.KIND:
                        print("+", end="")
                    case CellState.MEAN:
                        print("-", end="")
                    case _:
                        print(" ", end="")
            print()
