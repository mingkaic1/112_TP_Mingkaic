from cmu_112_graphics import *
from maze import *
from map import *
from tank import *
from projectiles import *
from obstacles import *
from fpsmeter import *

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
    startGame(app)

def startGame(app):
    app.game = Game()
    app.game.startRound()

# --------------------
# GAME MODE
# --------------------

def gameMode_timerFired(app):
    app.framesElapsed += 1

    # FPSmeter
    app.fpsMeter.addFrame()
    print(f"{FPS: }app.fpsMeter.getFPS()")

    # Start new round
    if app.game.round.isOver == True:
        app.game.startRound()

def gameMode_keyPressed(app, event):

    # Player 1
    if (event.key == app.game.controls[1]["forward"]):
        app.game.round.tank[1].startMovingForward()
    if (event.key == app.game.controls[1]["backward"]):
        app.game.round.tank[1].startMovingBackward()
    if (event.key == app.game.controls[1]["left"]):
        app.game.round.tank[1].startSteeringLeft()
    if (event.key == app.game.controls[1]["right"]):
        app.game.round.tank[1].startMovingRight()
    if (event.key == app.game.controls[1]["fire"]):
        app.game.round.tank[1].fire()

    # Player 2
    if (event.key == app.game.controls[2]["forward"]):
        app.game.round.tanks[2].startMovingForward()
    if (event.key == app.game.controls[2]["backward"]):
        app.game.round.tanks[2].startMovingBackward()
    if (event.key == app.game.controls[2]["left"]):
        app.game.round.tanks[2].startSteeringLeft()
    if (event.key == app.game.controls[2]["right"]):
        app.game.round.tanks[2].startMovingRight()
    if (event.key == app.game.controls[2]["fire"]):
        app.game.round.tanks[2].fire()

def gameMode_keyReleased(app, event):

    # Player 1
    if (event.key == app.game.controls[1]["forward"]):
        round.tank1.stopMovingForward()
    if (event.key == app.game.controls[1]["backward"]):
        round.tank1.stopMovingBackward()
    if (event.key == app.game.controls[1]["left"]):
        round.tank1.stopSteeringLeft()
    if (event.key == app.game.controls[1]["right"]):
        round.tank1.stopMovingRight()
    if (event.key == app.game.controls[1]["fire"]):
        round.tank1.fire()

    # Player 2
    if (event.key == app.game.controls[2]["forward"]):
        round.tank2.stopMovingForward()
    if (event.key == app.game.controls[2]["backward"]):
        round.tank2.stopMovingBackward()
    if (event.key == app.game.controls[2]["left"]):
        round.tank2.stopSteeringLeft()
    if (event.key == app.game.controls[2]["right"]):
        round.tank2.stopMovingRight()
    if (event.key == app.game.controls[2]["fire"]):
        round.tank2.fire()

def gameMode_redrawAll(app, canvas):
    pass

runApp(width = WIDTH, height = HEIGHT)