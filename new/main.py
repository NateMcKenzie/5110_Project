from simulator import Simulator 

def main():
    width = 20
    height = 20
    num_agents = 50
    num_iterations = 10
    
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