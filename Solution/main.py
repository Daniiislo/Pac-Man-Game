from Mize import Mize
from BFS import BFS
from General import State

mize = Mize("maze.txt")
mize.print()

state = State(mize.start)
bfs = BFS(mize.walls)
solution = None
solution = bfs.solve(state, mize.goal)
print(solution)