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

# Game will try to keep within +-20% of this FPS
TARGET_FPS = 100

WIDTH = settings["WINDOW_WIDTH"]
HEIGHT = settings["WINDOW_HEIGHT"]

# --------------------
# START APP
# --------------------

def appStarted(app):
    app.timerDelay = 1000 // (TARGET_FPS * 2) # This seems to work well as a starting value (at least with TARGET_FPS = 60 on MY computer)
    app.mode = "gameMode"
    app.framesElapsed = 0

    # FPSmeter
    app.fpsMeter = FPSmeter()

    app.framesSinceLastFPSAdjust = 0

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

    # Update GameAIs
    app.game.round.updateGameAIs()

    # Update Tanks
    app.game.round.updateTanks()

    # Update Projectiles
    app.game.round.updateProjectiles()

    # Check if any tank is hit (and if the round is over)
    app.game.checkHits()

    # Try to maintain a constant FPS by adjusting app.timerDelay
    currentFPS = app.fpsMeter.getFPS()
    # Need to boost FPS (decrease app.timerDelay)
    if currentFPS < TARGET_FPS * 0.8:
        app.timerDelay = int((app.timerDelay * 0.9) // 1) # Round down
    # Need to lower FPS (increase app.timerDelay)
    elif currentFPS > TARGET_FPS * 1.2:
        app.timerDelay = int((app.timerDelay * 1.1 + 1) // 1) # Round up
    print(app.timerDelay)

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
    drawScores(app, canvas)

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
        if tanksTranslatedCorners[i] != None:
            canvas.create_polygon(tanksTranslatedCorners[i], fill = app.game.settings["PLAYER_COLORS"][i])

def drawProjectiles(app, canvas):
    # Get list of tuples, each representing 4 canvas coordinates of circle
    projectilesTranslatedCoordinates = app.game.round.getProjectilesTranslatedCoordinates()
    for i in range(len(projectilesTranslatedCoordinates)):
        canvas.create_oval(projectilesTranslatedCoordinates[i], fill = "black")

def drawFPS(app, canvas):
    canvas.create_text(5, 5, text = f"{round(app.fpsMeter.getFPS())}", anchor = "nw")

def drawScores(app, canvas):
    xGap = app.game.settings["WINDOW_WIDTH"] // (app.game.settings["NUM_PLAYERS"] + app.game.settings["NUM_AI"] + 1)
    x0 = (app.game.settings["WINDOW_WIDTH"] - (app.game.settings["NUM_PLAYERS"] + app.game.settings["NUM_AI"] - 1) * xGap) // 2
    y = ((app.game.settings["MARGIN"] + app.game.settings["NUM_ROWS"] * app.game.settings["MAPCELL_SIZE"]) + app.game.settings["WINDOW_HEIGHT"]) // 2
    for i in range(app.game.settings["NUM_PLAYERS"] + app.game.settings["NUM_AI"]):
        canvas.create_text(x0 + i * xGap, y, font = "Arial 80 bold", fill = app.game.settings["PLAYER_COLORS"][i], text = f"{app.game.scores[i]}")
runApp(width = WIDTH, height = HEIGHT)