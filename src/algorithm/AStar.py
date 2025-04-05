from src.utils.algorithm_utils import Node, State
from src.config import STEP_SIZE    
import time
import tracemalloc
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
        self.count = 0
    
    def empty(self):
        return len(self.elements) == 0
    
    def add(self, item, priority):
        # Count được sử dụng để đảm bảo thứ tự ổn định khi hai phần tử có priority bằng nhau
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

class AStar():
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

    def heuristic(self, a, b):
        # Sử dụng khoảng cách Manhattan làm hàm heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def solve(self, state: State, goal_position):
        # Initialize the number of expanded nodes
        expanded_nodes = 0

        # Start time tracking
        start_time = time.time()

        # Start memory tracking 
        tracemalloc.start()

        # Initial solution to None
        solution = None

        # Initialize frontier with priority queue
        start = Node(state=state, parent=None, action=None, cost=0)
        frontier = PriorityQueue()
        
        # Thêm node khởi đầu với priority = heuristic(start, goal)
        start_pos = state.current_position
        frontier.add(start, self.heuristic(start_pos, goal_position))
        
        # Lưu trữ chi phí đã biết đến mỗi node
        cost_so_far = {start_pos: 0}
        
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
            current_pos = node.state.current_position

            # Increment the number of expanded nodes
            expanded_nodes += 1

            # If node is the goal, then we have a solution
            if current_pos == goal_position:
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
            explored.add(current_pos)

            # Add neighbors to frontier
            for action, position in self.neighbors(node.state):
                # Tính toán chi phí thực để đi đến vị trí mới (g(n))
                new_cost = cost_so_far[current_pos] + 1  # Mỗi bước đi có chi phí 1
                
                # Nếu đây là lần đầu tiên đến position hoặc tìm thấy đường đi tốt hơn
                if position not in cost_so_far or new_cost < cost_so_far[position]:
                    cost_so_far[position] = new_cost
                    
                    # Tính toán priority = g(n) + h(n)
                    priority = new_cost + self.heuristic(position, goal_position)
                    
                    state = State(current_position=position)
                    if position not in explored:
                        child = Node(state=state, parent=node, action=action, cost=new_cost)
                        frontier.add(child, priority) 