import random, time, statistics
from suppressprint import *

class Cell():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = [True, True, True, True] # Counterclockwise: NWSE

    def __repr__(self):
        return f"Cell({self.row}, {self.col}): {self.walls}"

    def __hash__(self):
        return hash(self.getHashables())

    def getHashables(self):
        return self.row, self.col

    def knockWall(self, wall):
        self.walls[wall] = False

    def connect(self, other):
        if (isinstance(other, Cell) == False):
            return False
        # Other is north of Self
        if (self.row == other.row + 1) and (self.col == other.col):
            self.knockWall(0)
            other.knockWall(2)
        # Other is west of Self
        elif (self.row == other.row) and (self.col == other.col + 1):
            self.knockWall(1)
            other.knockWall(3)
        # Other is south of Self
        elif (self.row == other.row - 1) and (self.col == other.col):
            self.knockWall(2)
            other.knockWall(0)
        # Other is east of Self
        elif (self.row == other.row) and (self.col == other.col - 1):
            self.knockWall(3)
            other.knockWall(1)

class Maze():

    # Premade 4-by-4 grid for testing
    DEFAULT0 = [
        [[True, True, False, False], [True, False, True, False], [True, False, True, True], [True, True, False, True]],
        [[False, True, True, False], [True, False, True, False], [True, False, False, True], [False, True, False, True]],
        [[True, True, False, False], [True, False, False, False], [False, False, True, False], [False, False, True, True]],
        [[False, True, True, True], [False, True, True, False], [True, False, True, False], [True, False, True, True]]
    ]

    ALGORITHMS = {
        0: "Recursive Backtracker",
        1: "Aldous Broder",
        2: "Wilson",
        3: "Hunt and Kill"
    }

    def __init__(self, numRows = 4, numCols = 4):
        self.numRows = numRows
        self.numCols = numCols
        # Make .grid (2D list of Cell objects)
        self.makeGrid(numRows, numCols)
        # Generate maze
        self.generateMaze()

    def __repr__(self):
        result = ""
        for row in range(self.numRows):
            for col in range(self.numCols):
                result += f"{self.grid[row][col]}\n"
        return result

    # HELPER FUNCTION
    def makeGrid(self, numRows, numCols):
        self.grid = []
        for row in range(numRows):
            self.grid.append([])
            for col in range(numCols):
                self.grid[-1].append(Cell(row, col))

    # Change the size of the maze
    #   Updates numRows & numCols variables, and calls makeGrid()
    def setSize(self, numRows, numCols):
        self.numRows = numRows
        self.numCols = numCols
        self.makeGrid(numRows, numCols)

    def getCell(self, row, col):
        return self.grid[row][col]

    def generateDefault(self, defaultNum = 0):
        if (defaultNum == 0):
            self.initDefault(self.DEFAULT0)

    # HELPER FUNCTION (Do not call outside class)
    def initDefault(self, defaultGrid):
        self.grid = []
        self.numRows = len(defaultGrid)
        self.numCols = len(defaultGrid[0])
        for row in range(self.numRows):
            self.grid.append([])
            for col in range(self.numCols):
                self.grid[-1].append(Cell(row, col))
                self.grid[-1][-1].walls = defaultGrid[row][col]

    def generateMaze(self, algorithmNum = "random"):
        if (algorithmNum == "random"):
            algorithmNum = random.randint(min(self.ALGORITHMS.keys()),
                                          max(self.ALGORITHMS.keys()))
        if (algorithmNum == 0):
            self.generateMazeRecursiveBacktracker()
        elif (algorithmNum == 1):
            self.generateMazeAldousBroder()
        elif (algorithmNum == 2):
            self.generateMazeWilson()
        elif (algorithmNum == 3):
            self.generateMazeHuntAndKill()

    def testAlgorithms(self,
                       sizeList = [4, 10, 20],
                       iterations = 10,
                       algorithmNumList = "default"):
        if (algorithmNumList == "default"):
            algorithmNumList = self.ALGORITHMS.keys()
        # Initialize variable
        result = {}
        # Loop through each algorithm
        for algorithmNum in algorithmNumList:
            result[algorithmNum] = {
                "name": self.ALGORITHMS[algorithmNum],
                "results": {}
            }
            print(f"Testing [{algorithmNum}. {self.ALGORITHMS[algorithmNum]}] ...")
            # Loop through each size
            for size in sizeList:
                result[algorithmNum]["results"][size] = {
                    "average": 0,
                    "timings": []
                }
                self.setSize(size, size)
                print(f"\tTesting [{algorithmNum}. {self.ALGORITHMS[algorithmNum]}] at size {size}*{size} ...")
                # Loop through each iteration
                for iteration in range(iterations):
                    timeStart = time.perf_counter()
                    print(f"\t\tIteration {iteration + 1}/{iterations} ([{algorithmNum}. {self.ALGORITHMS[algorithmNum]}] at size {size}*{size}) ...")
                    with SuppressPrint():
                        self.generateMaze(algorithmNum)
                    timeEnd = time.perf_counter()
                    timeElapsed = timeEnd - timeStart
                    result[algorithmNum]["results"][size]["timings"].append(timeElapsed)
                # Calculate average timing
                timeAverage = statistics.mean(result[algorithmNum]["results"][size]["timings"])
                result[algorithmNum]["results"][size]["average"] = timeAverage
        # Display result
        print("\n--------------------")
        print("RESULTS")
        print("--------------------")
        for algorithmNum in result:
            print(f"{algorithmNum}. {result[algorithmNum]['name']}")
            for size in result[algorithmNum]["results"]:
                print(f"\t{size}*{size}  Average: {result[algorithmNum]['results'][size]['average']} s")
        return result

    def getNeighbors(self, currentCell):
        neighbors = []
        directions = self.getNeighborDirections(currentCell)
        for dirRow, dirCol in directions:
            neighbor = self.getCell(currentCell.row + dirRow,
                                    currentCell.col + dirCol)
            neighbors.append(neighbor)
        return neighbors

    def getUnvisitedNeighbors(self, currentCell, visitedCells):
        unvisitedNeighbors = []
        neighbors = self.getNeighbors(currentCell)
        for neighbor in neighbors:
            if (neighbor not in visitedCells):
                unvisitedNeighbors.append(neighbor)
        return unvisitedNeighbors

    def getVisitedNeighbors(self, currentCell, visitedCells):
        visitedNeighbors = []
        neighbors = self.getNeighbors(currentCell)
        for neighbor in neighbors:
            if (neighbor in visitedCells):
                visitedNeighbors.append(neighbor)
        return visitedNeighbors

    def checkInitCell(self, initRow, initCol):
        if (initRow == "random"):
            initRow = random.randint(0, self.numRows - 1)
        if (initCol == "random"):
            initCol = random.randint(0, self.numCols - 1)
        return initRow, initCol

    def getRandomCell(self):
        row = random.randint(0, self.numRows - 1)
        col = random.randint(0, self.numCols - 1)
        return self.getCell(row, col)

    def getNeighborDirections(self, currentCell):
        neighborDirections = []
        for dirRow, dirCol in [(0, -1), (-1, 0), (0, +1), (+1, 0)]:
            nextRow = currentCell.row + dirRow
            nextCol = currentCell.col + dirCol
            if ((nextRow in range(self.numRows)) and
                (nextCol in range(self.numCols))):
                neighborDirections.append((dirRow, dirCol))
        return neighborDirections

    # Recursive Backtracker (Depth-First Search) algorithm
    # Tends to have longer paths; very efficient
    def generateMazeRecursiveBacktracker(self, initRow = "random", initCol = "random"):
        # If no starting Cell is given, choose a random starting Cell
        initRow, initCol = self.checkInitCell(initRow, initCol)
        # Initialize variables
        totalCells = self.numRows * self.numCols
        cellStack = []
        visitedCells = set()
        cellStack.append(self.getCell(initRow, initCol))
        visitedCells.add(cellStack[-1])
        # Loop until all Cells are visited
        while len(visitedCells) < totalCells:
            currentCell = cellStack[-1]
            unvisitedNeighbors = self.getUnvisitedNeighbors(currentCell, visitedCells)
            # If current Cell is at a dead end (no unvisited neighbors), backtrack
            if (len(unvisitedNeighbors) == 0):
                cellStack.pop()
                continue
            # Choose a random neighbor Cell and move to it
            nextCell = random.choice(unvisitedNeighbors)
            currentCell.connect(nextCell)
            cellStack.append(nextCell)
            visitedCells.add(nextCell)
        print("Maze generated with Recursive Backtracker algorithm.")

    # Hunt and Kill algorithm
    # Tends to have meandering paths and fewer dead ends
    # For some reason, very inefficient suddenly at large (100) sizes
    def generateMazeHuntAndKill(self, initRow = "random", initCol = "random"):
        # If no starting Cell is given, choose a random starting Cell
        initRow, initCol = self.checkInitCell(initRow, initCol)
        # Initialize variables
        totalCells = self.numRows * self.numCols
        visitedCells = set()
        currentCell = self.getCell(initRow, initCol)
        visitedCells.add(currentCell)
        # Loop for each walk
        while len(visitedCells) < totalCells:
            unvisitedNeighbors = self.getUnvisitedNeighbors(currentCell, visitedCells)
            # Walk until a dead end is reached
            while (len(unvisitedNeighbors) > 0):
                nextCell = random.choice(unvisitedNeighbors)
                currentCell.connect(nextCell)
                visitedCells.add(nextCell)
                currentCell = nextCell
                unvisitedNeighbors = self.getUnvisitedNeighbors(currentCell, visitedCells)
            # Hunt from top-left corner for an adjacent unvisited cell
            adjacentCellFound = False
            for row in range(self.numRows):
                for col in range(self.numCols):
                    huntCell = self.getCell(row, col)
                    visitedNeighbors = self.getVisitedNeighbors(huntCell, visitedCells)
                    # If adjacent unvisited cell found, break nested loop
                    if (huntCell not in visitedCells) and (len(visitedNeighbors) > 0):
                        randomNeighbor = random.choice(visitedNeighbors)
                        huntCell.connect(randomNeighbor)
                        currentCell = huntCell
                        visitedCells.add(currentCell)
                        adjacentCellFound = True
                        break
                if (adjacentCellFound == True):
                    break
        print("Maze generated with Hunt-And-Kill algorithm")

    # Aldous Broder algorithm
    # Creates a uniform spanning tree (i.e. no bias), but extremely inefficient
    def generateMazeAldousBroder(self, initRow = "random", initCol = "random"):
        # If no starting Cell is given, choose a random starting Cell
        initRow, initCol = self.checkInitCell(initRow, initCol)
        # Initialize variables
        totalCells = self.numRows * self.numCols
        visitedCells = set()
        currentCell = self.getCell(initRow, initCol)
        visitedCells.add(currentCell)
        # Loop until all Cells are visited
        while len(visitedCells) < totalCells:
            neighbors = self.getNeighbors(currentCell) #
            # Choose a random neighbor Cell and move to it
            nextCell = random.choice(neighbors)
            if nextCell not in visitedCells:
                currentCell.connect(nextCell)
            visitedCells.add(nextCell)
            currentCell = nextCell
        print("Maze generated with Aldous Broder algorithm.")

    # Wilson's algorithm
    # Creates a uniform spanning tree (i.e. no bias)
    # Generally more efficient than Aldous Broder, except for first ~33%
    def generateMazeWilson(self, initRow = "random", initCol = "random"):
        # If no starting Cell is given, choose a random starting Cell
        initRow, initCol = self.checkInitCell(initRow, initCol)
        # Initialize variables
        totalCells = self.numRows * self.numCols
        visitedCells = set() # Cells already IN the maze (from previous walks)
        initCell = self.getCell(initRow, initCol)
        visitedCells.add(initCell)
        walkInitCell = initCell
        # Loop for each walk
        while len(visitedCells) < totalCells:
            # Store the current walk sequence as a dictionary, with each item:
            #   {Cell: (exit direction as a tuple)}
            currentWalk = {}
            # Choose a random unvisited cell to begin the walk
            while walkInitCell in visitedCells:
                walkInitCell = self.getRandomCell()
            currentWalk[walkInitCell] = None
            # Walk until a visited cell is reached
            currentCell = walkInitCell
            while currentCell not in visitedCells:
                neighborDirections = self.getNeighborDirections(currentCell)
                dirRow, dirCol = random.choice(neighborDirections)
                currentWalk[currentCell] = (dirRow, dirCol)
                currentCell = self.getCell(currentCell.row + dirRow,
                                           currentCell.col + dirCol)
            # Go through the walk again, following the found directions
            currentCell = walkInitCell
            while currentCell not in visitedCells:
                dirRow, dirCol = currentWalk[currentCell]
                nextCell = self.getCell(currentCell.row + dirRow,
                                        currentCell.col + dirCol)
                currentCell.connect(nextCell)
                visitedCells.add(currentCell)
                currentCell = nextCell
        print("Maze generated with Wilson's algorithm")

    # HELPER FUNCTION (Maze generation algorithm)
    def generateMazeRandomizedPrim(self):
        pass

