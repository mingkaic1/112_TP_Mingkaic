from cmu_112_graphics import *
from maze import *

# --------------------
# TEST ALGORITHMS
# --------------------

# myMaze = Maze()
# myMaze.testAlgorithms([4, 10, 20, 50, 100], 10)

# --------------------
# GRAPHICS FRAMEWORK FUNCTIONS
# --------------------

WIDTH = 800
HEIGHT = 800
MARGIN = 50

def appStarted(app):
    app.margin = MARGIN
    newMaze(app)

def newMaze(app):
    app.maze = Maze(20, 20)
    app.numRows = app.maze.numRows
    app.numCols = app.maze.numCols

def keyPressed(app, event):
    if (event.key == "r"):
        newMaze(app)

def redrawAll(app, canvas):
    drawMaze(app, canvas)

def drawMaze(app, canvas):
    for row in range(app.numRows):
        for col in range(app.numCols):
            cellCoords = getCellCoords(app, row, col)  # 4-tuple
            drawCell(app, canvas, app.maze.grid[row][col].walls, cellCoords)

def drawCell(app, canvas, walls, cellCoords): # walls is a 4-list; cellCoords is a 4-tuple
    x0, y0, x1, y1 = cellCoords
    if (walls[0] == True):
        canvas.create_line(x0, y0, x1, y0)
    if (walls[1] == True):
        canvas.create_line(x0, y0, x0, y1)
    if (walls[2] == True):
        canvas.create_line(x0, y1, x1, y1)
    if (walls[3] == True):
        canvas.create_line(x1, y0, x1, y1)

def getCellCoords(app, row, col):
    x0 = round(app.margin + (app.width - 2*app.margin)*(col/app.numCols))
    x1 = round(app.margin + (app.width - 2*app.margin)*((col + 1)/app.numCols))
    y0 = round(app.margin + (app.height - 2*app.margin)*(row/app.numRows))
    y1 = round(app.margin + (app.height - 2*app.margin)*((row + 1)/ app.numRows))
    return x0, y0, x1, y1

runApp(width = WIDTH, height = HEIGHT)