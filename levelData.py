class LevelData:
    def __init__(self, filename):
        with open(filename) as file:
            self.obstacles = []
            self.exits = []
            self.width, self.height = map(int, file.readline().split(" "))

            for y in range(self.height):
                line = file.readline()
                for x in range(self.width):
                    match line[x]:
                        case "=":
                            self.obstacles.append((x,y))
                        case "/":
                            self.exits.append((x,y))
