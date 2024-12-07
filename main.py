from renderer import Renderer
from simulator import Simulator


def main():
    width = 20
    height = 20
    num_agents = 50
    num_iterations = 10
    
    simulator = Simulator(width, height)
    simulator.populate(num_agents)
    renderer = Renderer()
    
    print("Iteration 0")
    renderer.render(simulator)
    
    for it in range(num_iterations):
        print(f"Iteration {it + 1}")
        simulator.update()
        renderer.render(simulator)


if __name__ == '__main__':
    main()
