import random
import math
import itertools as it

class Simulator:
    def __init__(self, level_data):
        self.P = 25
        self.coop_rate = level_data.coop_rate
        self.width = level_data.width
        self.height = level_data.height
        self.agents = {}
        self.neighboring = dict() # position: neighboring accessible cells (8 cells; accounting for walls and obstacles; may be out of bounds (for escaping))
        self.empty = set([(x, y) for x in range(self.width) for y in range(self.height) if (x, y) not in level_data.obstacles])
        self.obstacles = set(level_data.obstacles)
        self.exits = set(level_data.exits)
        self.exit_distances = [[self.calc_exit_distance(x, y) for x in range(self.width)] for y in range(self.height)]
        self.evacuated = set() # All evacuated agents
        self.over = False


        for (x, y) in it.product(range(self.width), range(self.height)):
            self.compute_neighboring((x, y))

        self.populate(level_data.num_agents)

        # Stats and logging
        self.count_states()


    def calc_exit_distance(self, x, y):
        if (x, y) in self.obstacles:
            return float("inf")
        distances = [math.sqrt((exit_pos[0]-x)**2 + (exit_pos[1]-y)**2) for exit_pos in self.exits]
        return min(distances)
        
    def populate(self, num_agents):
        positions = random.sample(list(self.empty), num_agents)
        for position in positions:
            strategy = "cooperate" if random.random() < self.coop_rate else "defect" 
            self.add_agent(strategy, position)
    
    def add_agent(self, strategy, position):
        if position in self.empty:
            agent = Agent(strategy, position)
            self.agents[position] = agent
            self.empty.remove(position)
        elif not self.is_in_bounds(position):
            print(f"Cannot create agent at out-of-bounds position {position}")
        else:
            print(f"Cannot create agent at nonempty position {position}")

    def compute_neighboring(self, position):
        if not self.is_in_bounds(position):
            return
        x, y = position
        neighbors = [(new_x, new_y) for new_x in range(x - 1, x + 2) for new_y in range (y - 1, y + 2)]
        valid_neighbors = []

        for neighbor in neighbors:
            if neighbor not in self.obstacles and self.is_in_bounds(neighbor):
                valid_neighbors.append(neighbor)

        self.neighboring[position] = valid_neighbors

    def is_in_bounds(self, position):
        return 0 <= position[0] < self.width and 0 <= position[1] < self.height

    def update(self):
        attempted_moves = {} # position: list[Agent]
        for position, agent in self.agents.items(): # Each agent will try to move
            # Keep track of every agent's attempted move
            new_position = self.choose_move(agent)
            if new_position is None: # Check if agent has no available moves
                continue
            elif new_position in attempted_moves:
                attempted_moves[new_position].append(agent)
            else:
                attempted_moves[new_position] = [agent]
        for position, agents in attempted_moves.items():
            # Decide which agent moves
            agents = attempted_moves[position]
            moving_agent = self.game(agents)

            # Move successful agent (if one exists) and reevaluate the strategies of every agent who fail
            for agent in agents:
                if agent == moving_agent:
                    if position not in self.exits:
                        self.move(agent, position)
                       #print(f"{agent} moves")
                    else:
                        self.evacuate_agent(agent)
                       #print(f"{agent} evacuates")
                else:
                    self.reevaluate(agent)

        self.count_states()
        
    # Choose a neighboring cell to attempt to move to
    # TODO: Implement smarter pathing logic
    def choose_move(self, agent):
        available_moves = [cell for cell in self.neighboring[agent.position] if cell in self.empty]
        if len(available_moves) == 0:
            return None
        exit_moves = [cell for cell in available_moves if cell in self.exits]
        if len(exit_moves) > 0: # Move to exit if available
            return random.choice(exit_moves)
        ranking = sorted(available_moves, key=lambda move: self.exit_distances[move[1]][move[0]], reverse=True)
        weight = [(ranking.index(move) + 1)**1.2 for move in available_moves]
        choice = random.choices(available_moves, weights=weight)
        return choice[0]
        
    def move(self, agent, position):
        self.empty.add(agent.position)
        self.empty.remove(position)

        del self.agents[agent.position]
        self.agents[position] = agent
        agent.position = position

    def evacuate_agent(self, agent):
        self.evacuated.add(agent)
        self.empty.add(agent.position)
        del self.agents[agent.position]
        if len(self.agents) == 0:
            self.over = True
            
    # Returns the agent that moves into the square
    # Returns None if no agent moves
    def game(self, agents):
        if len(agents) == 1:
            return agents[0]

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
            probs = [1.0 / num_defect ** self.P for agent in agents]
            
        probs.append(1.0 - sum(probs)) # Probability that no one moves
        choices = agents + [None]
        return random.choices(choices, weights=probs)[0]
            
    def reevaluate(self, agent):
        # Calculate formula for reevaluating strategy
        random_num = random.random()
        if random_num > 0.2: # Only change with 20% probability TODO: use actual formula
            if agent.strategy == "cooperate":
                agent.strategy = "defect"
            elif agent.strategy == "defect":
                agent.strategy = "cooperate"

    def count_states(self):
        self.coop_count = 0
        self.defect_count = 0
        for agent in self.agents.values():
            if agent.strategy == "cooperate":
                self.coop_count += 1
            elif agent.strategy == "defect":
                self.defect_count += 1

class Agent:
    def __init__(self, strategy, position):
        self.strategy = strategy
        self.position = position
        
    def __repr__(self):
        return f"Agent {self.strategy} {self.position}"
