from src.utils.algorithm_utils import Node, StackFrontier, State, get_neighbors, extract_path, measure_performance 

class DFS():
    def __init__(self, walls):
        self.walls = walls
        self.expanded_nodes = 0

    def neighbors(self, state):
        # Use common neighbors function
        return get_neighbors(self.walls, state)
    
    @measure_performance
    def solve(self, state: State, goal_position):
        # Initialize frontier to just the starting position
        start = Node(state=state, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        explored = set()

        # Keep looping until solution found
        while not frontier.empty():
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

            # Get neighbors
            neighbors = self.neighbors(node.state)
            
            for action, pos in neighbors:
                next_state = State(current_position=pos)
                if not frontier.contains_state(next_state) and pos not in explored:
                    frontier.add(Node(state=next_state, parent=node, action=action))