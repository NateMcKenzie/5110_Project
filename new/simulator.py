import random

class Simulator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for y in range(height)] for x in range(width)]
        self.agents = set()
        self.empty = set([(x, y) for x in range(self.width) for y in range(self.height)])
        self.attempted_moves = {} # new position: list of agents attempting to move into the position
        
    def populate(self, num_agents):
        positions = random.sample(list(self.empty), num_agents)
        for position in positions:
            agent = Agent("cooperate", position)
            self.agents.add(agent)
            self.empty.remove(position)
            self.grid[position[0]][position[1]] = agent
    
    def update(self):
        attempted_moves = {} # position: list[Agent]
        for agent in self.agents:
            new_position = self.choose_move(agent)
            if new_position in attempted_moves:
                attempted_moves[new_position].append(agent)
            else:
                attempted_moves[new_position] = [agent]
        print(attempted_moves)
        for position in attempted_moves:
            # Decide probabilities with game
            agents = attempted_moves[position]
            probs = self.game(agents)
            
            # Roll probabilities to find who moves into the position
            choices = agents + [None]
            choice = random.choices(choices, weights=probs)
            print(choice)
            
            # Move successful agent (if one exists) and reevaluate the strategies of every agent who fail
            for agent in agents:
                if agent == choice:
                    print("MOVE")
                    self.move(agent, position)
                else:
                    self.reevaluate(agent)
        
    # Choose a neighboring cell to attempt to move to
    # TODO: Implement smarter pathing logic
    def choose_move(self, agent):
        neighbors = []
        for dx in range(-1, 2):
            x = agent.position[0] + dx
            for dy in range(-1, 2):
                y = agent.position[1] + dy
                if (x, y) in self.empty and 0 <= x < self.width and 0 <= y < self.height and not (dx == dy == 0):
                    neighbors.append((x, y))
        return random.choice(neighbors)
        
    def move(self, agent):
        self.empty.add(agent.position)
        self.grid[agent.position[0]][agent.position[1]] = None
        
        agent.position = position
        self.empty.remove(agent.position)
        self.grid[position[0]][position[1]] = agent
            
    # Return a list of probabilities of moving for each agent.
    # The last probability is the probability of no one moving.
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
            probs = [0.0 if agent.strategy == "cooperate" else 1.0 for agent in agents]
        else:
            probs = [1.0 / num_defect ** P]
        probs.append(1.0 - sum(probs)) # Probability that no one moves
        return probs
            
    def reevaluate(self, agent):
        # Calculate formula for reevaluating strategy
        random_num = random.random()
        if random_num < 0.2: # Only change with 20% probability TODO: use actual formula
            return
        if agent.strategy == "cooperate":
            agent.strategy == "defect"
        else:
            agent.strategy = "cooperate"
            
    def render(self):
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if self.grid[x][y] in self.agents:
                    agent = self.grid[x][y]
                    if agent.strategy == "cooperate":
                        line += "+"
                    elif agent.strategy == "defect":
                        line += "-"
                else:
                    line += "."
            print(line)
    
class Agent:
    def __init__(self, strategy, position):
        self.strategy = strategy
        self.position = position
        
    def __repr__(self):
        return f"Agent {self.strategy} {self.position}"