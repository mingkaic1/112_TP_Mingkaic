from map import *
from maze import *

maze1 = Maze(4, 4)
maze1.generateMaze()
map1 = Map(maze1, 400, 400)
for row in range(len(map1.grid)):
    for col in range(len(map1.grid[row])):
        print(map1.grid[row][col])