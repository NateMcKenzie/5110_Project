class BasicRenderer:
    def render(self, simulator):
        for y in range(simulator.height):
            line = ""
            for x in range(simulator.width):
                if simulator.grid[x][y] in simulator.agents:
                    agent = simulator.grid[x][y]
                    if agent.strategy == "cooperate":
                        line += "+"
                    elif agent.strategy == "defect":
                        line += "-"
                else:
                    line += "."
            print(line)
