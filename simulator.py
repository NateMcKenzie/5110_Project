import random
import itertools as it

class Simulator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.P = 25
        
        self.agents = {}
        self.empty = set() # All cells that are accessible but currently unoccupied
        self.neighboring = dict() # position: neighboring accessible cells (8 cells; accounting for walls and obstacles; may be out of bounds (for escaping))
        self.obstacles = set()
        self.exits = set() # position, direction
        self.walls = set() # (position, direction)
        self.evacuated = set() # All evacuated agents
        
        for (x, y) in it.product(range(width), range(height)):
            self.empty.add((x, y))
            self.compute_neighboring((x, y))
            
        # Add walls around the perimeter
        for x in range(width):
            self.add_wall((x, 0), "up")
            self.add_wall((x, height - 1), "down")
        for y in range(height):
            self.add_wall((0, y), "left")
            self.add_wall((width - 1, y), "right")

        # Stats and logging
        self.coop_count = 0
        self.defect_count = 0
        
    def populate(self, num_agents):
        positions = random.sample(list(self.empty), num_agents)
        for position in positions:
            strategy = "cooperate" if random.random() < 0.5 else "defect" # TODO: change this
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
            
    def add_obstacle(self, position):
        if position in self.empty:
            empty.remove(position)
            obstacles.add(position)
        elif not self.is_in_bounds(position):
            print(f"Cannot create agent at out-of-bounds position {position}")
        else:
            print(f"Cannot add obstacle at nonempty position {position}")
            
    def add_wall(self, position, direction):
        if not self.is_in_bounds(position):
            print("Cannot create wall at out-of-bounds position {position}")
            return
            
        # Check direction and compute position of other side of wall
        x, y = position
        if direction == "up":
            other_position = (x, y - 1)
            other_direction = "down"
        elif direction == "left":
            other_position = (x - 1, y)
            other_direction = "right"
        elif direction == "right":
            other_position = (x + 1, y)
            other_direction = "left"
        elif direction == "down":
            other_position = (x, y + 1)
            other_direction = "up"
        else:
            print(f"Cannot create wall in invalid direction {direction}")
            return
            
        # Add wall at direction
        self.walls.add((position, direction))
        self.compute_neighboring(position)
        
        # If other side is in bounds, add wall on opposite side
        if self.is_in_bounds(other_position):
            self.walls.add((other_position, other_direction))
            self.compute_neighboring(other_position)
        
    def remove_wall(self, position, direction):
        if not self.is_in_bounds(position):
            print("Cannot remove wall at out-of-bounds position {position}")
            return
            
        # Check direction and compute position of other side of wall
        x, y = position
        if direction == "up":
            other_position = (x, y - 1)
            other_direction = "down"
        elif direction == "left":
            other_position = (x - 1, y)
            other_direction = "right"
        elif direction == "right":
            other_position = (x + 1, y)
            other_direction = "left"
        elif direction == "down":
            other_position = (x, y + 1)
            other_direction = "up"
        else:
            print(f"Cannot create wall in invalid direction {direction}")
            return
            
        # Remove wall at direction
        self.walls.remove((position, direction))
        self.compute_neighboring(position)
        
        # If other side is in bounds, remove wall on opposite side
        if self.is_in_bounds(other_position):
            self.walls.remove((other_position, other_direction))
            self.compute_neighboring(other_position)
        
    # Compute all accessible cells within the Moore neighborhood
    def compute_neighboring(self, position):
        if not self.is_in_bounds(position):
            return
        x, y = position
        neighbors = []
        
        if (position, "left") not in self.walls:
            neighbors.append((x - 1, y))
            if (position, "up") not in self.walls:
                neighbors.append((x - 1, y - 1))
            if (position, "down") not in self.walls:
                neighbors.append((x - 1, y + 1))
        if (position, "right") not in self.walls:
            neighbors.append((x + 1, y))
            if (position, "up") not in self.walls:
                neighbors.append((x + 1, y - 1))
            if (position, "down") not in self.walls:
                neighbors.append((x + 1, y + 1))
        if (position, "up") not in self.walls:
            neighbors.append((x, y - 1))
        if (position, "down") not in self.walls:
            neighbors.append((x, y + 1))
            
        self.neighboring[position] = neighbors
        
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
                    if self.is_in_bounds(position):
                        self.move(agent, position)
                        print(f"{agent} moves")
                    else:
                        self.evacuate_agent(agent)
                        print(f"{agent} evacuates")
                else:
                    self.reevaluate(agent)

        self.count_states()
        
    # Choose a neighboring cell to attempt to move to
    # TODO: Implement smarter pathing logic
    def choose_move(self, agent):
        available_moves = [cell for cell in self.neighboring[agent.position] if cell in self.empty]
        exit_moves = [cell for cell in available_moves if cell in self.exits]
        if len(exit_moves) > 0: # Move to exit if available
            return random.choice(exit_moves)
        elif len(available_moves) == 0:
            return None
        return random.choice(available_moves)
        
    def move(self, agent, position):
        self.empty.add(agent.position)
        self.empty.remove(position)
        del self.agents[agent.position]
        self.agents[position] = agent
        agent.position = position
        
    def evacuate_agent(self, agent):
        self.evacuated.add(agent)
        self.agents.remove(agent)
            
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
