from obstacles import *

class Map():
    # 'width' and 'height' is pixel size of playable map on screen, NOT whole window
    def __init__(self, maze, width, height):
        self.grid = [] # 2D list of MapCell objects
        self.makeGrid(maze)
        self.makeWalls() # ...

    # Build self.grid using the given Maze object
    def makeGrid(self, maze):
        for row in range(len(maze.grid)):
            self.grid.append([])
            for col in range(len(maze.grid[row])):
                self.grid[-1].append(MapCell(row, col))
                self.grid[-1][-1].setWallList(maze.grid[row][col].walls)

class MapCell():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.wallList = [] # Temporary list to store walls as list of 4 True/Falses
        self.walls = []

    def __repr__(self):
        return f"MapCell({self.row}, {self.col}): {self.wallList}"

    def __hash__(self):
        return hash(self.getHashables())

    def getHashables(self):
        return self.row, self.col, "MapCell"

    def setWallList(self, wallList):
        self.wallList = wallList

    def makeWalls(self):
        pass # TO DO

