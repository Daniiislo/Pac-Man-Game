from src.algorithm.DFS import DFS
from src.algorithm.General import State

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
dfs = DFS(walls)

start = State((1, 1))

end = (15, 1)

print(dfs.solve(start, end))