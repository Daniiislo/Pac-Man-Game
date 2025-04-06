import sys
import heapq

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
 

