from obstacles import *

class Map():

    WALL_HALF_WIDTH = 2

    # Initialize with an already-generated Map object
    # 'width' and 'height' is pixel size of playable map on screen, NOT whole window
    def __init__(self, maze, width, height):
        self.maze = maze
        self.width = width
        self.height = height

        self.numRows = self.maze.numRows
        self.numCols = self.maze.numCols

        self.wallHalfWidth = self.WALL_HALF_WIDTH

        # Initialize measurement attributes
        #   - Idea: Coordinates for MapCells and Walls are integers
        #   - (.effectiveWidth may be a few pixels smaller than .width)
        self.mapCellWidth = self.width // self.numCols
        self.mapCellHeight = self.height // self.numRows
        self.effectiveWidth = self.mapCellWidth * self.numCols
        self.effectiveHeight = self.mapCellHeight * self.numRows

        # Initialize .grid (2D list of MapCell objects)
        self.grid = []
        self.makeGrid()

        # Initialize .wallRectangles (list of 4-tuples, each representing coordinates of a wall)
        #   - To optimize drawing (tkinter can just draw all rectangles based on .wallRectangles, instead
        #       of going through each MapCell object)
        #   - 4 edges of map (i.e. outlines) are stored as single rectangles
        self.wallRectangles = []
        self.makeWallRectangles()

    # Build .grid (currently does not contain information about walls)
    def makeGrid(self):
        for row in range(self.numRows):
            self.grid.append([])
            for col in range(self.numCols):
                # Add in the MapCell object
                p1 = (col * self.mapCellWidth, row * self.mapCellHeight)
                p2 = ((col + 1) * self.mapCellWidth, (row + 1) * self.mapCellHeight)
                self.grid[row].append(MapCell(row, col, p1, p2))

                # Top wall
                if self.maze.grid[row][col].walls[0] == True:
                    # Current mapCell is in first row
                    if row == 0:
                        self.grid[row][col].setWall(0, self.wallHalfWidth)
                    # Otherwise, link to a previously generated Wall
                    else:
                        self.grid[row][col].linkWall(0, self.grid[row - 1][col].walls[2])

                # Left wall
                if self.maze.grid[row][col].walls[1] == True:
                    # Current mapCell is in first col
                    if col == 0:
                        self.grid[row][col].setWall(1, self.wallHalfWidth)
                    # Otherwise, link to a previously generated Wall
                    else:
                        self.grid[row][col].linkWall(1, self.grid[row][col - 1].walls[3])

                # Bottom wall
                if self.maze.grid[row][col].walls[2] == True:
                    # Since .grid is created left-right, top-down, there should not be any MapCell at the bottom
                    self.grid[row][col].setWall(2, self.wallHalfWidth)

                # Right wall
                if self.maze.grid[row][col].walls[3] == True:
                    # Since .grid is created left-right, top-down, there should not be any MapCell at the bottom
                    self.grid[row][col].setWall(3, self.wallHalfWidth)

    def makeWallRectangles(self):
        # Top wall as single rectangle
        self.wallRectangles.append((0 - self.wallHalfWidth,
                                    0 - self.wallHalfWidth,
                                    self.effectiveWidth + self.wallHalfWidth,
                                    self.wallHalfWidth))
        # Bottom wall as single rectangle
        self.wallRectangles.append((0 - self.wallHalfWidth,
                                    self.effectiveHeight - self.wallHalfWidth,
                                    self.effectiveWidth + self.wallHalfWidth,
                                    self.effectiveHeight + self.wallHalfWidth))
        # Left wall as single rectangle
        self.wallRectangles.append((0 - self.wallHalfWidth,
                                    0 - self.wallHalfWidth,
                                    self.wallHalfWidth,
                                    self.effectiveHeight + self.wallHalfWidth))
        # Right wall as single rectangle
        self.wallRectangles.append((self.effectiveWidth - self.wallHalfWidth,
                                    0 - self.wallHalfWidth,
                                    self.effectiveWidth + self.wallHalfWidth,
                                    self.effectiveHeight + self.wallHalfWidth))

        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                # If MapCell is not on the bottom row, and has a bottom wall
                if (row < self.numRows - 1) and (self.grid[row][col].walls[2] != None):
                    bottomWall = self.grid[row][col].walls[2]
                    self.wallRectangles.append((bottomWall.x1,
                                                bottomWall.y1,
                                                bottomWall.x2,
                                                bottomWall.y2))
                # If MapCell is not on the right-most row, and has a right wall
                if (col < self.numCols - 1) and (self.grid[row][col].walls[3] != None):
                    rightWall = self.grid[row][col].walls[3]
                    self.wallRectangles.append((rightWall.x1,
                                                rightWall.y1,
                                                rightWall.x2,
                                                rightWall.y2))

    def getMapCell(self, row, col):
        return self.grid[row][col]

class MapCell():

    def __init__(self, row, col, p1, p2):
        self.row = row
        self.col = col
        self.x1, self.y1 = p1
        self.x2, self.y2 = p2

        # Initialize .walls
        #   - Store Wall objects and None (if there is no Wall in that position)
        #   - Order: North West South East
        self.walls = [None, None, None, None]

    def setWall(self, direction, wallHalfWidth):
        # Top wall
        if direction == 0:
            p1 = (self.x1 - wallHalfWidth, self.y1 - wallHalfWidth)
            p2 = (self.x2 + wallHalfWidth, self.y1 + wallHalfWidth)
        # Left wall
        elif direction == 1:
            p1 = (self.x1 - wallHalfWidth, self.y1 - wallHalfWidth)
            p2 = (self.x1 + wallHalfWidth, self.y2 + wallHalfWidth)
        # Bottom wall
        elif direction == 2:
            p1 = (self.x1 - wallHalfWidth, self.y2 - wallHalfWidth)
            p2 = (self.x2 + wallHalfWidth, self.y2 + wallHalfWidth)
        # Right wall
        elif direction == 3:
            p1 = (self.x2 - wallHalfWidth, self.y1 - wallHalfWidth)
            p2 = (self.x2 + wallHalfWidth, self.y2 + wallHalfWidth)
        self.walls[direction] = Wall(p1, p2)

    def linkWall(self, direction, wall):
        self.walls[direction] = wall

    def __repr__(self):
        return f"MapCell({self.row}, {self.col}): {self.wallList}"

    def __hash__(self):
        return hash(self.getHashables())

    def getHashables(self):
        return self.row, self.col, "MapCell"