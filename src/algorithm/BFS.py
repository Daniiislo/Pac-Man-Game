from General import Node, QueueFrontier, State

class BFS():
    def __init__(self, walls):
        self.walls = walls
        
    def neighbors(self, state):
        row , col = state.current_position

        # All possible action
        candidates = [
            ("U", (row - 1, col)),
            ("D", (row + 1, col)),
            ("L", (row, col - 1)),
            ("R", (row, col + 1))
        ]

        # Ensure actions are valid
        result = []

        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue

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
                raise Exception("no solution")
            
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