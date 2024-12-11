class BasicRenderer:
    def render(self, simulator, round_count):
        print(f"Update {round_count}")
        for y in range(simulator.height):
            line = ""
            for x in range(simulator.width):
                if (x, y) in simulator.agents:
                    agent = simulator.agents[(x, y)]
                    if agent.strategy == "cooperate":
                        line += "+"
                    elif agent.strategy == "defect":
                        line += "-"
                elif (x, y) in simulator.obstacles:
                    line += "o"
                elif (x, y) in simulator.exits:
                    line += "/"
                else:
                    line += "."
            print(line)
