from cmu_112_graphics import *
from settings import *
from game import *
from round import *
from map import *
from maze import *
from tank import *
from projectiles import *
from obstacles import *
from fpsmeter import *
import drawingHelpers # Includes top-level (non-encapsulated) drawing helper functions

# Game will try to keep within +-20% of this FPS
TARGET_FPS = 60

WIDTH = settings["WINDOW_WIDTH"]
HEIGHT = settings["WINDOW_HEIGHT"]

# --------------------
# START APP
# --------------------

def appStarted(app):

    app.timerDelay = 1000 // (TARGET_FPS * 2) # This seems to work well as a starting value (at least with TARGET_FPS = 60 on MY computer)
    app.mode = "gameMode"

    # For timing actions (executing actions at specific intervals, etc.)
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

    # Update GameAIs
    app.game.round.updateGameAIs()

    # Update Tanks
    app.game.round.updateTanks()

    # Update Projectiles
    app.game.round.updateProjectiles()

    # Check if any tank is hit (and if the round is over)
    app.game.checkHits()

def gameMode_keyPressed(app, event):

    # Check if event.key controls any player Tank; if so, make the control
    app.game.checkKeyPressed(event.key)

    if (event.key == "r"):
        app.game.round.isOver = True

def gameMode_keyReleased(app, event):

    # Check if event.key controls any player Tank; if so, make the control
    app.game.checkKeyReleased(event.key)

def gameMode_redrawAll(app, canvas):

    drawingHelpers.drawWalls(app, canvas)
    drawingHelpers.drawTanks(app, canvas)
    drawingHelpers.drawProjectiles(app, canvas)
    drawingHelpers.drawFPS(app, canvas)
    drawingHelpers.drawScores(app, canvas)

runApp(width = WIDTH, height = HEIGHT)