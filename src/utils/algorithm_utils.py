import sys
import heapq
from src.config import STEP_SIZE

class State():
    def __init__(self, current_position):
        self.current_position = current_position
        #self.goal_position = goal_position

    def __eq__(self, other):
        return self.current_position == other.current_position


class Node():
    def __init__(self, state, parent, action, cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(state == node.state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node= self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
        
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node= self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.count = 0
    
    def empty(self):
        return len(self.elements) == 0
    
    def add(self, item, priority):
        # Count is used to ensure stable order when two elements have the same priority
        heapq.heappush(self.elements, (priority, self.count, item))
        self.count += 1
    
    def contains_state(self, state):
        return any(state == node.state for _, _, node in self.elements)
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            _, _, node = heapq.heappop(self.elements)
            return node

def get_neighbors(walls, state, include_cost=False):
    """
    Common function to find valid neighboring positions
    
    Args:
        walls: Collision matrix
        state: Current state
        include_cost: If True, return (action, position, cost), if False, return (action, position)
    
    Returns:
        List of valid moves
    """
    # Get current position
    x, y = state.current_position

    # Define all possible actions
    if include_cost:
        candidates = [
            ("u", (x, y - STEP_SIZE), 2),  # Up costs 2
            ("d", (x, y + STEP_SIZE), 2),  # Down costs 2
            ("l", (x - STEP_SIZE, y), 1),  # Left costs 1
            ("r", (x + STEP_SIZE, y), 1)   # Right costs 1
        ]
    else:
        candidates = [
            ("u", (x, y - STEP_SIZE)),
            ("d", (x, y + STEP_SIZE)),
            ("l", (x - STEP_SIZE, y)),
            ("r", (x + STEP_SIZE, y))
        ]

    # Initialize result list
    result = []
    
    # Get grid boundaries
    max_x = len(walls[0]) - 1
    max_y = len(walls) - 1

    # Check each candidate move
    for candidate in candidates:
        action = candidate[0]
        position = candidate[1]
        x, y = position
        
        isValid = True
        # First check if the position is within bounds
        if 0 <= x <= max_x and 0 <= y <= max_y:
            # Check every cell in the step size
            for i in range(STEP_SIZE):
                if not isValid:
                    break
                for j in range(STEP_SIZE):
                    # Check if position is out of bounds
                    if y + i > max_y or x + j > max_x or y + i < 0 or x + j < 0:
                        isValid = False
                        break
                    
                    # Check if there's a wall
                    if walls[y + i][x + j]:
                        isValid = False
                        break
        else:
            isValid = False
            
        # Add valid moves to result
        if isValid:
            if include_cost:
                result.append((action, position, candidate[2]))
            else:
                result.append((action, position))

    return result

def extract_path(node):
    """
    Extract path from the final node to the root
    
    Args:
        node: Final node
        
    Returns:
        List of actions to go from start to goal
    """
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    actions.reverse()
    return actions

def measure_performance(func):
    """
    Decorator to measure algorithm performance
    
    Args:
        func: Function to measure
        
    Returns:
        Wrapper function
    """
    def wrapper(self, state, goal_position):
        import time
        import tracemalloc
        
        # Start time and memory tracking
        start_time = time.time()
        tracemalloc.start()
        
        # Reset expanded nodes counter if exists
        if hasattr(self, 'expanded_nodes'):
            self.expanded_nodes = 0
        
        # Call the original function
        result = func(self, state, goal_position)
        
        # End time and memory tracking
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Print performance metrics
        print(f"Search Time: {end_time - start_time:.4f} seconds")
        print(f"Memory Usage: {current / 1024:.2f} KB (current), {peak / 1024:.2f} KB (peak)")
        if hasattr(self, 'expanded_nodes'):
            print(f"Expanded Nodes: {self.expanded_nodes}")
        
        return result
    
    return wrapper
 

