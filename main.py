import argparse

from basicRenderer import BasicRenderer
from fancyRenderer import FancyRenderer
from simulator import Simulator, CellState
from logger import Logger


def arg_setup():
    parser = argparse.ArgumentParser(
        prog="Evacuation Simulator",
        description="Watch how kind or mean people are in evacuations",
    )
    parser.add_argument(
        "output_dir",
        default="output",
        nargs="?",
        help="Directory path where output files will be saved",
    )
    parser.add_argument("-f", "--fancy", action="store_true", help="Enable fancy renderer")
    return parser.parse_args()


def main(args):
    simulator = Simulator(20, 20, (0, 0))
    renderer = FancyRenderer() if args.fancy else BasicRenderer()
    logger = Logger(args.output_dir)

    simulator.setCell(1, 2, CellState.KIND)
    simulator.setCell(1, 3, CellState.KIND)
    simulator.setCell(3, 4, CellState.KIND)
    simulator.setCell(5, 5, CellState.KIND)
    simulator.setCell(2, 7, CellState.KIND)
    simulator.setCell(3, 4, CellState.KIND)
    simulator.setCell(3, 6, CellState.KIND)
    simulator.setCell(2, 2, CellState.KIND)
    simulator.setCell(2, 3, CellState.KIND)
    simulator.setCell(3, 3, CellState.KIND)

    # Blinker: Should blink (in conway)
    simulator.setCell(6, 4, CellState.KIND)
    simulator.setCell(6, 5, CellState.KIND)
    simulator.setCell(6, 6, CellState.KIND)
    simulator.count_states()
    renderer.render(simulator)

    for i in range(20):
        simulator.update()
        renderer.render(simulator)
        logger.logStep(simulator.kind_count, simulator.mean_count)

    logger.save()
    logger.plot()


if __name__ == "__main__":
    args = arg_setup()
    main(args)
