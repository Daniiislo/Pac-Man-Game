from src.utils.algorithm_utils import Node, QueueFrontier, State
from src.config import STEP_SIZE  
import time
import tracemalloc   

class BFS():
    def __init__(self, walls):
        self.walls = walls
        
    def neighbors(self, state):
        # ensure int
        x, y = state.current_position

        # All possible action
        candidates = [
            ("u", (x, y - STEP_SIZE)),
            ("d", (x, y + STEP_SIZE)),
            ("l", (x - STEP_SIZE, y)),
            ("r", (x + STEP_SIZE, y))
        ]

        # Ensure actions are valid
        result = []

        # Get max boundaries of the grid
        max_x = len(self.walls[0]) - 1
        max_y = len(self.walls) - 1

        for action, (x, y) in candidates:
            isValid = True
            if 0 <= x <= max_x and 0 <= y <= max_y:
                for i in range(STEP_SIZE):
                    if not isValid:
                        break
                    for j in range(STEP_SIZE):
                        # Check if position is out of bounds
                        if y + i > max_y or x + j > max_x or y + i < 0 or x + j < 0:
                            isValid = False
                            break
                        
                        # Check if there's a wall
                        if self.walls[y + i][x + j]:
                            isValid = False
                            break
            else:
                isValid = False
                
            if isValid:
                result.append((action, (x, y)))

        return result

    
    def solve(self, state: State, goal_position):
        # Initialize the number of expanded nodes
        expanded_nodes=0

        # Start time tracking
        start_time= time.time()
        
        # Start memory tracking 
        tracemalloc.start()

        # Initial solution to None
        solution = None

        # Initialize frontier to just the starting position
        start = Node(state=state, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)
        
        # Initialize an empty explored set
        explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                end_time = time.time()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                return []
            
            # Choose a node from the frontier
            node = frontier.remove()

            # Increment the number of expanded nodes
            expanded_nodes += 1

            # If node is the goal, then we have a solution
            if node.state.current_position == goal_position:
                actions = []

                # Follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                solution = actions

                # Stop time tracking
                end_time = time.time()

                # Stop memory tracking
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                print(f"Search Time: {end_time - start_time:.4f} seconds")
                print(f"Memory Usage: {current / 1024:.2f} KB (current), {peak / 1024:.2f} KB (peak)")
                print(f"Expanded Nodes: {expanded_nodes}")

                return solution
            
            # Mark node as explored
            explored.add(node.state.current_position)

            # Add neighbors to frontier
            for action, position in self.neighbors(node.state):
                state = State(current_position=position)
                if not frontier.contains_state(state) and state.current_position not in explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)