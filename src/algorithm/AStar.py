from src.utils.algorithm_utils import Node, State, PriorityQueue, get_neighbors, extract_path, measure_performance

class AStar():
    def __init__(self, walls,game_state):
        self.walls = walls
        self.game_state = game_state  # Add reference to game_state
        self.expanded_nodes = 0

    def neighbors(self, state):
        # Use common neighbors function
        return get_neighbors(self.walls, state)

    def heuristic(self, a, b):
        """
        Calculate Manhattan distance heuristic
        
        Args:
            a: First position (x1, y1)
            b: Second position (x2, y2)
            
        Returns:
            Manhattan distance |x1-x2| + |y1-y2|
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    @measure_performance
    def solve(self, state: State, goal_position):
        # Initialize frontier with priority queue
        start = Node(state=state, parent=None, action=None, cost=0)
        frontier = PriorityQueue()
        
        # Add start node with priority = heuristic(start, goal)
        start_pos = state.current_position
        frontier.add(start, self.heuristic(start_pos, goal_position))
        
        # Store the known cost to each node
        cost_so_far = {start_pos: 0}
        
        # Initialize an empty explored set
        explored = set()

        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                return []
            
            # Choose a node from the frontier
            node = frontier.remove()
            current_pos = node.state.current_position

            # Increment the number of expanded nodes
            self.expanded_nodes += 1

            # If node is the goal, then we have a solution
            if current_pos == goal_position:
                return extract_path(node)
            
            # Mark node as explored
            explored.add(current_pos)

            # Add neighbors to frontier
            for action, position in self.neighbors(node.state):
                # Calculate the actual cost to reach the new position (g(n))
                new_cost = cost_so_far[current_pos] + 1  # Each step has a cost of 1
                
                # If this is the first time to position or find a better path
                if position not in cost_so_far or new_cost < cost_so_far[position]:
                    cost_so_far[position] = new_cost
                    
                    # Calculate priority = g(n) + h(n)
                    priority = new_cost + self.heuristic(position, goal_position)
                    
                    state = State(current_position=position)
                    if position not in explored:
                        child = Node(state=state, parent=node, action=action, cost=new_cost)
                        frontier.add(child, priority) 