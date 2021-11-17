from cmu_112_graphics import *
from fpsmeter import *

# --------------------
# GRAPHICS FRAMEWORK FUNCTIONS
# --------------------

WIDTH = 800
HEIGHT = 800
MARGIN = 50
FPS = 60 # Target

KEY_BINDINGS = {
    "P1_LEFT": "Left",
    "P1_RIGHT": "Right",
    "P1_UP": "Up",
    "P1_DOWN": "Down",
    "P1_FIRE": "Space",

    "P2_LEFT": "A",
    "P2_RIGHT": "D",
    "P2_UP": "W",
    "P2_DOWN": "S",
    "P2_FIRE": "Tab"
}

def appStarted(app):
    app.timerDelay = 1000//FPS
    app.tank1 = Tank(app.width // 2, app.height // 2)

    app.fpsmeter = FPSmeter()

    app.bullets = []

def timerFired(app):
    app.tank1.steer()
    app.tank1.move()
    moveBullets(app)

    app.fpsmeter.addFrame()
    print(app.fpsmeter.getFPS())

def moveBullets(app):
    i = 0
    while i < len(app.bullets):
        app.bullets[i].move()
        if (app.bullets[i].isDespawned == True):
            app.bullets.pop(i)
            app.tank1.replenishAmmo()
        else:
            # Bounce off sides of screen
            if (app.bullets[i].x <= 0) or (app.bullets[i].x >= app.width):
                app.bullets[i].bounce(isVertical = False)
            elif (app.bullets[i].y <= 0) or (app.bullets[i].y >= app.height):
                app.bullets[i].bounce(isVertical = True)
            i += 1

def keyPressed(app, event):
    # Steering
    if (event.key == KEY_BINDINGS["P1_LEFT"]):
        app.tank1.startSteeringLeft()
    if (event.key == KEY_BINDINGS["P1_RIGHT"]):
        app.tank1.startSteeringRight()
    # Moving
    if (event.key == "Up"):
        app.tank1.startMovingForward()
    if (event.key == "Down"):
        app.tank1.startMovingBackward()
    # Fire
    if (event.key == "Space"):
        output = app.tank1.fire()
        if (output != None):
            app.bullets.append(output)

def keyReleased(app, event):
    # Steering
    if (event.key == "Left"):
        app.tank1.stopSteeringLeft()
    if (event.key == "Right"):
        app.tank1.stopSteeringRight()
    # Moving
    if (event.key == "Up"):
        app.tank1.stopMovingForward()
    if (event.key == "Down"):
        app.tank1.stopMovingBackward()

def redrawAll(app, canvas):
    drawTank(app, canvas, app.tank1)
    drawBullets(app, canvas)

def drawTank(app, canvas, tank):
    corners = tank.getCorners()
    canvas.create_polygon(corners)

def drawBullets(app, canvas):
    for bullet in app.bullets:
        canvas.create_oval(bullet.x - bullet.RADIUS, bullet.y - bullet.RADIUS, bullet.x + bullet.RADIUS, bullet.y + bullet.RADIUS, fill ="black")

runApp(width=WIDTH, height=HEIGHT)