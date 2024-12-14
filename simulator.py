import random
import math
import itertools as it

class Simulator:
    def __init__(self, level_data):
        self.P = 2.5   # Penalty for defecting
        self.Kf = 10.0 # Pedestrians' familiarity with the exit 
        self.D = 1     # Inertia
        self.K = 0.1   # Irrationality
        
        self.coop_rate = level_data.coop_rate
        self.width = level_data.width
        self.height = level_data.height
        self.agents = dict()
        self.neighboring = dict() # position: neighboring accessible cells (8 cells; accounting for walls and obstacles; may be out of bounds (for escaping))
        self.empty = set([(x, y) for x in range(self.width) for y in range(self.height) if (x, y) not in level_data.obstacles])
        self.obstacles = set(level_data.obstacles)
        self.exits = set(level_data.exits)
        self.static_field_values = dict()
        self.evacuated = set() # All evacuated agents
        self.over = False

        for position in it.product(range(self.width), range(self.height)):
            self.compute_neighboring(position)
            if position not in self.obstacles:
                self.compute_static_field_value(position)

        self.populate(level_data.num_agents)

        # Stats and logging
        self.count_states()

    def calc_exit_distance(self, position):
        if position in self.obstacles:
            return float("inf")
        distances = [math.sqrt((exit_pos[0]-position[0])**2 + (exit_pos[1]-position[1])**2) for exit_pos in self.exits]
        return min(distances)
        
    def compute_static_field_value(self, position):
        distance = self.calc_exit_distance(position)
        # Set the static field value of exits to infinity
        self.static_field_values[position] = 1 / distance if distance != 0 else float("inf") 
        
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
            
            # Keep track of the strategies used in this particular game for reevaluation.
            strategies = [agent.strategy for agent in agents]
            num_cooperate = strategies.count("cooperate")
            num_defect = strategies.count("defect")
            
            # Move successful agent (if one exists) and reevaluate the strategies of every agent who fail
            for agent in agents:
                if agent == moving_agent:
                    if position not in self.exits:
                        self.move(agent, position)
                    else:
                        self.evacuate_agent(agent)
                else:
                    self.reevaluate(agent, num_cooperate, num_defect)

        self.count_states()
        
    # Choose a neighboring cell to attempt to move to
    def choose_move(self, agent):
        available_moves = [cell for cell in self.neighboring[agent.position] if cell in self.empty]
        available_exits = [move for move in available_moves if move in self.exits]
        if len(available_exits) > 0:
            return random.choice(available_exits) # Move to a random adjacent exit if one is available
        weights = [math.exp(self.Kf * self.static_field_values[move]) for move in available_moves]
        return random.choices(available_moves, weights=weights)[0]
        
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
            
    # Computes the index of the strategy that is the winner in a prisoner's dilemma game
    # Strategies are passed in as a tuple of strings
    # Returns the index of the agent that moves
    # Returns -1 if no agents move
    # Also returns probability distribution
    def game(self, agents):
        strategies = [agent.strategy for agent in agents]
        num_cooperate = strategies.count("cooperate")
        num_defect = strategies.count("defect")
        
        cooperate_prob = self.utility("cooperate", num_cooperate, num_defect)
        defect_prob = self.utility("defect", num_cooperate, num_defect)
        probs = [cooperate_prob if agent.strategy == "cooperate" else defect_prob for agent in agents]
        probs.append(1.0 - sum(probs)) # Probability that no agent is chosen
        
        choices = agents + [None]
        return random.choices(choices, weights=probs)[0]
        
    # Compute the utility (probability of moving) of a strategy in a game 
    # with a given number of cooperating and defecting players (including the given strategy)
    def utility(self, strategy, num_cooperate, num_defect):
        if num_defect == 0:
            return 1 / num_cooperate
        elif strategy == "cooperate":
            return 0.0
        elif num_defect == 1:
            return 1.0
        else:
            return 1.0 / num_defect ** self.P
            
    # Agents will reevaluate their strategies based on their expected utility from their last game,
    # with and without changing their strategy
    # The strategies from the last game are passed in
    def reevaluate(self, agent, num_cooperate, num_defect):
        # Calculate formula for reevaluating strategy
        M_x = self.utility(agent.strategy, num_cooperate, num_defect)
        
        if agent.strategy == "cooperate":
            other_strategy = "defect"
            num_cooperate -= 1
            num_defect += 1
        else:
            other_strategy = "cooperate"
            num_cooperate += 1
            num_defect -= 1
        M_y = self.utility(other_strategy, num_cooperate, num_defect)
            
        W = 1.0 / (1.0 + math.exp((M_x - M_y) / self.K))
        random_num = random.random()
        if random_num <= W: # Change with W probability
            agent.change_strategy() # Change strategy back

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
        
    def change_strategy(self):
        if self.strategy == "cooperate":
            self.strategy = "defect"
        else:
            self.strategy = "cooperate"
