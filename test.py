from src.algorithm.DFS import DFS
from src.algorithm.BFS import BFS
from src.algorithm.AStar import AStar
from src.algorithm.UCS import UniformCostSearch
from src.utils.algorithm_utils import State

# read maze from file matrix.txt
walls = []

with open('matrix.txt', 'r') as f:
    for line in f:
        row = []
        #split by tabs
        for i in line.split('\t'):
            if i == "False":
                row.append(False)
            elif i == "True":
                row.append(True)
        walls.append(row)



print (walls)
dfs = UniformCostSearch(walls)

start = State((33,39))

end = (17,23)

print(dfs.solve(start, end))