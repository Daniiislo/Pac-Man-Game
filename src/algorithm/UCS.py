from src.utils.algorithm_utils import Node, State, PriorityQueue, get_neighbors, extract_path, measure_performance

class UniformCostSearch():
    def __init__(self, walls):
        self.walls = walls
        self.expanded_nodes = 0

    def neighbors(self, state):
        # Use common neighbors function
        return get_neighbors(self.walls, state, include_cost=True)
    
    @measure_performance
    def solve(self, state: State, goal_position):
        # Initialize frontier with priority queue
        start = Node(state=state, parent=None, action=None, cost=0)
        frontier = PriorityQueue()
        
        # Add starting node with priority 0 (initial cost)
        frontier.add(start, 0)
        
        # Store known costs to each position
        cost_so_far = {state.current_position: 0}
        
        # Initialize an empty explored set
        explored = set()

        # Keep looping until solution found
        while True:
            # If nothing left in frontier, then no path
            if frontier.empty():
                return []
            
            # Choose a node from the frontier (lowest cost)
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
            for action, position, step_cost in self.neighbors(node.state):
                # Calculate actual cost to reach new position (g(n))
                new_cost = cost_so_far[current_pos] + step_cost  # Use specific cost for this move
                
                # If this is first visit or we found a cheaper path
                if position not in cost_so_far or new_cost < cost_so_far[position]:
                    cost_so_far[position] = new_cost
                    
                    # Use cost as priority (no heuristic)
                    priority = new_cost
                    
                    state = State(current_position=position)
                    if position not in explored:
                        child = Node(state=state, parent=node, action=action, cost=new_cost)
                        frontier.add(child, priority)