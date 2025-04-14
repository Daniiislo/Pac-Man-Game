from src.utils.algorithm_utils import Node, QueueFrontier, State, get_neighbors, extract_path, measure_performance

class BFS():
    def __init__(self, walls,game_state):
        self.walls = walls
        self.game_state = game_state  # Add reference to game_state
        self.expanded_nodes = 0
        
    def neighbors(self, state):
        # Use common neighbors function
        return get_neighbors(self.walls, state)
    
    @measure_performance
    def solve(self, state: State, goal_position):
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

            # Increment the number of expanded nodes
            self.expanded_nodes += 1

            # If node is the goal, then we have a solution
            if node.state.current_position == goal_position:
                return extract_path(node)
            
            # Mark node as explored
            explored.add(node.state.current_position)

            # Add neighbors to frontier
            for action, position in self.neighbors(node.state):
                state = State(current_position=position)
                if not frontier.contains_state(state) and state.current_position not in explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)