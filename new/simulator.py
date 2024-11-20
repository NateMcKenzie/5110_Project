import random

class Simulator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for y in range(height)] for x in range(width)]
        self.agents = set()
        self.empty = set([[(x, y) for y in range(self.height)] for x in range(self.width)])
        self.attempted_moves = {} # new position: list of agents attempting to move into the position
        
    def populate(self, num_agents):
        positions = random.sample(self.empty, num_agents)
        for position in positions:
            self.agents.add(position)
            empty.remove(position)
    
    def update(self):
        self.attempted_moves = {} # position: list[Agent]
        for agent in self.agents:
            new_position = # make move
            attempted_moves[new_position] += agent
        for position in attempted_moves:
            # Decide probabilities with game
            probs = game(self.agents)
            # Roll probabilities to find who moves into the position
            
            # Reevaluate the strategies of every agent who failed to move
            
    def game(self, agents):
        P = 2.5
        num_cooperate = 0
        num_defect = 0
        for agent in agents:
            if agent.strategy == "cooperate":
                num_cooperate += 1
            elif agent.strategy == "defect":
                num_defect += 1
        if num_defect == 0:
            probs = [1.0 / num_cooperate for agent in agents]
        elif num_defect == 1:
            probs = [0.0 for agent in agents if agent.strategy == "cooperate" else 1.0]
        else:
            probs = [1.0 / num_defect ** P]
            
    def render(self):
        for x in range(self.width):
            for y in range(self.height):
                line = ""
                if self.grid[x][y] in self.agents:
                    agent = self.grid[x][y]
                    if agent.strategy == "cooperate":
                        line += "+"
                    elif agent.strategy == "defect":
                        line += "-"
                else:
                    line += "#"
    
class Agent:
    def __init__(self, strategy):
        self.strategy = strategy