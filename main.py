from cmu_112_graphics import *
from maze import *
from map import *
from tank import *
from projectiles import *
from obstacles import *
from fpsmeter import *
from round import *
from game import *


WIDTH = 1000
HEIGHT = 1000
TARGET_FPS = 100

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
    app.game = Game()
    app.game.startRound()

    print(app.game.controls)

# --------------------
# GAME MODE
# --------------------

def gameMode_timerFired(app):
    app.framesElapsed += 1

    # FPSmeter
    app.fpsMeter.addFrame()
    # print(f"FPS: {app.fpsMeter.getFPS()}")

    # Start new round
    if (app.game.round == None) or (app.game.round.isOver == True):
        app.game.startRound()

    # Update Tanks
    for i in range(len(app.game.round.tanks)):
        app.game.round.tanks[i].update()

def checkTankKeyPressed(app, event, i):
    if (event.key == app.game.controls[i]["forward"]):
        app.game.round.tanks[i].startMovingForward()
    if (event.key == app.game.controls[i]["backward"]):
        app.game.round.tanks[i].startMovingBackward()
    if (event.key == app.game.controls[i]["left"]):
        app.game.round.tanks[i].startSteeringLeft()
    if (event.key == app.game.controls[i]["right"]):
        app.game.round.tanks[i].startSteeringRight()
    if (event.key == app.game.controls[i]["fire"]):
        app.game.round.tanks[i].fire()

def checkTankKeyReleased(app, event, i):
    if (event.key == app.game.controls[i]["forward"]):
        app.game.round.tanks[i].stopMovingForward()
    if (event.key == app.game.controls[i]["backward"]):
        app.game.round.tanks[i].stopMovingBackward()
    if (event.key == app.game.controls[i]["left"]):
        app.game.round.tanks[i].stopSteeringLeft()
    if (event.key == app.game.controls[i]["right"]):
        app.game.round.tanks[i].stopSteeringRight()

def gameMode_keyPressed(app, event):
    for i in range(len(app.game.round.tanks)):
        checkTankKeyPressed(app, event, i)

    if (event.key == "r"):
        app.game.round.isOver = True
    if (event.key == "p"):
        print(app.game.round.maze)

def gameMode_keyReleased(app, event):

    for i in range(len(app.game.round.tanks)):
        checkTankKeyReleased(app, event, i)

def gameMode_redrawAll(app, canvas):
    drawWalls(app, canvas)
    drawTanks(app, canvas)

    print(app.game.round.tanks[0].isMovingForward)

def drawWalls(app, canvas):
    for wall in app.game.round.map.wallRectangles:
        canvas.create_rectangle(*wall, fill = "black")

def drawTanks(app, canvas):
    for i in range(len(app.game.round.tanks)):
        corners = app.game.round.tanks[i].getCorners()
        canvas.create_polygon(corners)

runApp(width = WIDTH, height = HEIGHT)