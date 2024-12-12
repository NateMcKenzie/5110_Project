class LevelData:
    def __init__(self, filename):
        with open(filename) as file:
            self.obstacles = []
            self.exits = []
            file.readline() # Ignore header
            self.width, self.height = map(int, file.readline().split(" "))
            self.num_agents, self.num_iterations = map(int, file.readline().split(" "))
            self.coop_rate = float(file.readline())

            for y in range(self.height):
                line = file.readline()
                for x in range(self.width):
                    match line[x]:
                        case "o":
                            self.obstacles.append((x,y))
                        case "/":
                            self.exits.append((x,y))
