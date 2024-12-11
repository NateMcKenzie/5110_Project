import argparse

from simulator import Simulator
from basicRenderer import BasicRenderer
from fancyRenderer import FancyRenderer
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
    width = 20
    height = 20
    num_agents = 5
    num_iterations = 2
    
    simulator = Simulator(width, height)
    simulator.populate(num_agents)
    simulator.count_states()
    renderer = FancyRenderer() if args.fancy else BasicRenderer()
    logger = Logger(args.output_dir)
    
    renderer.render(simulator)

    for i in range(1, num_iterations + 1):
        simulator.update()
        print(f"Update {i}")
        renderer.render(simulator)
        logger.logStep(simulator.coop_count, simulator.defect_count)

    logger.save()
    logger.plot()


if __name__ == "__main__":
    args = arg_setup()
    main(args)
