from basicRenderer import BasicRenderer
from fancyRenderer import FancyRenderer
from simulator import Simulator, CellState


def main():
    simulator = Simulator(10, 10, (0,0))
    renderer = FancyRenderer()

    # Block: Should stay alive (in conway)
    simulator.setCell(1, 2, CellState.KIND)
    simulator.setCell(1, 3, CellState.KIND)
    simulator.setCell(2, 2, CellState.KIND)
    simulator.setCell(2, 3, CellState.KIND)
    simulator.setCell(3, 3, CellState.KIND)

    # Blinker: Should blink (in conway)
    simulator.setCell(6, 4, CellState.KIND)
    simulator.setCell(6, 5, CellState.KIND)
    simulator.setCell(6, 6, CellState.KIND)
    renderer.render(simulator)

    for i in range(50):
        simulator.update()
        renderer.render(simulator)


if __name__ == '__main__':
    main()
