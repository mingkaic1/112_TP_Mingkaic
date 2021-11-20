from cmu_112_graphics import *
from maze import *
from map import *
from tank import *
from projectiles import *
from obstacles import *
from fpsmeter import *
from round import *
from game import *
from settings import *

TARGET_FPS = 100
WIDTH = settings["WINDOW_WIDTH"]
HEIGHT = settings["WINDOW_HEIGHT"]

# --------------------
# START APP
# --------------------

def appStarted(app):
    app.timerDelay = 1000 // TARGET_FPS
    app.mode = "gameMode"
    app.framesElapsed = 0

    # FPSmeter
    app.fpsMeter = FPSmeter()

    # Initialize Game object
    app.game = Game(settings)
    app.game.startRound()

# --------------------
# GAME MODE
# --------------------

def gameMode_timerFired(app):
    app.framesElapsed += 1

    # Update FPSmeter
    app.fpsMeter.addFrame()

    # Start new round if necessary
    if (app.game.round == None) or (app.game.round.isOver == True):
        app.game.startRound()

    # Update Tanks
    app.game.round.updateTanks()

    # Update Projectiles
    app.game.round.updateProjectiles()

def gameMode_keyPressed(app, event):

    # Check if event.key controls tank; if so, make the control
    app.game.checkKeyPressed(event.key)

    if (event.key == "r"):
        app.game.round.isOver = True

def gameMode_keyReleased(app, event):

    # Check if event.key controls tank; if so, make the control
    app.game.checkKeyReleased(event.key)

def gameMode_redrawAll(app, canvas):
    drawWalls(app, canvas)
    drawTanks(app, canvas)
    drawProjectiles(app, canvas)
    drawFPS(app, canvas)

# --------------------
# DRAWING HELPER FUNCTIONS
# --------------------

def drawWalls(app, canvas):
    for wall in app.game.round.map.translatedWallRectangles:
        canvas.create_rectangle(*wall, fill = "black")

def drawTanks(app, canvas):
    # Get list of lists, each containing 4 tuples representing corners of tank polygon
    tanksTranslatedCorners = app.game.round.getTanksTranslatedCorners()
    for i in range(len(tanksTranslatedCorners)):
        canvas.create_polygon(tanksTranslatedCorners[i])

def drawProjectiles(app, canvas):
    # Get list of tuples, each representing 4 canvas coordinates of circle
    projectilesTranslatedCoordinates = app.game.round.getProjectilesTranslatedCoordinates()
    for i in range(len(projectilesTranslatedCoordinates)):
        canvas.create_oval(projectilesTranslatedCoordinates[i], fill = "black")

def drawFPS(app, canvas):
    canvas.create_text(5, 5, text = f"{round(app.fpsMeter.getFPS())}", anchor = "nw")

runApp(width = WIDTH, height = HEIGHT)