import argparse

from simulator import Simulator
from quietRenderer import QuietRenderer
from basicRenderer import BasicRenderer
from fancyRenderer import FancyRenderer
from logger import Logger
from levelData import LevelData


def arg_setup():
    parser = argparse.ArgumentParser(
        prog="Evacuation Simulator",
        description="Watch how cooperative or not people are in evacuations",
    )
    parser.add_argument(
        "level_file",
        default="levels/ladder.lvl",
        nargs="?",
        help="Level file to use",
    )
    parser.add_argument(
        "output_dir",
        default="output",
        nargs="?",
        help="Directory where output files will be saved",
    )
    parser.add_argument("-f", "--fancy", action="store_true", help="Enable fancy renderer")
    parser.add_argument("-q", "--quiet", action="store_true", help="Disable rendering (precedence over -f)")
    return parser.parse_args()

def main(args):
    level_data = LevelData(args.level_file)
    simulator = Simulator(level_data)
    if args.quiet:
        renderer = QuietRenderer()
    elif args.fancy:
        renderer = FancyRenderer(simulator.width, simulator.height)
    else:
        renderer = BasicRenderer()
    logger = Logger(args.output_dir)
    
    renderer.render(simulator, 0)

    for i in range(1, level_data.num_iterations + 1):
        simulator.update()
        renderer.render(simulator, i)
        logger.logStep(simulator.coop_count, simulator.defect_count, len(simulator.evacuated))
        if simulator.over:
            break


    logger.save()
    logger.plot()


if __name__ == "__main__":
    args = arg_setup()
    main(args)
