from src.algorithm.General import Node, QueueFrontier, State
from src.config import STEP_SIZE    

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
            if 0 <= x <= max_x and 0 <= y <= max_y:
                if action=="u":
                    if not self.walls[y][x] and not self.walls[y+1][x]:
                        result.append((action, (x, y)))
                elif action=="d":
                    if not self.walls[y][x] and not self.walls[y-1][x]:
                        result.append((action, (x, y)))
                elif action=="l":
                    if not self.walls[y][x] and not self.walls[y][x+1]:
                        result.append((action, (x, y)))
                elif action=="r":
                    if not self.walls[y][x] and not self.walls[y][x-1]:
                        result.append((action, (x, y)))
        return result

    
    def solve(self, state: State, goal_position):

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
                return []
            
            # Choose a node from the frontier
            node = frontier.remove()

            # If node is the goal, then we have a solution
            if node.state.current_position == goal_position:
                actions = []

                # Follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    node = node.parent
                actions.reverse()
                solution = actions
                return solution
            
            # Mark node as explored
            explored.add(node.state.current_position)

            # Add neighbors to frontier
            for action, position in self.neighbors(node.state):
                state = State(current_position=position)
                if not frontier.contains_state(state) and state.current_position not in explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)