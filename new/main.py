from simulator import Simulator 

def main():
    width = 8
    height = 8
    num_agents = 4
    num_iterations = 5
    
    simulator = Simulator(width, height)
    simulator.populate(num_agents)
    
    print("Iteration 0")
    simulator.render()
    
    for it in range(num_iterations):
        print(f"Iteration {it + 1}")
        simulator.update()
        simulator.render()

if __name__ == "__main__":
    main()