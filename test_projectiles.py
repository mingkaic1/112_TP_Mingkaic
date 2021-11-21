from cmu_112_graphics import *
from tank import *
from projectiles import *
from obstacles import *
from map import *
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

    app.bullets = []

    app.dummyMapCell = MapCell(0, 0)
    app.dummyMapCell.walls.append(Wall((300, 100), (500, 200)))
    app.dummyMapCell.walls.append(Wall((200, 150), (250, 500)))

    app.fpsmeter = FPSmeter()

def timerFired(app):
    app.tank1.steer()
    app.tank1.move()
    moveBullets(app)

    # app.fpsmeter.addFrame()
    # print(app.fpsmeter.getFPS())

def moveBullets(app):
    i = 0
    while i < len(app.bullets):
        app.bullets[i].move()
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
            output.currentMapCell = app.dummyMapCell
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
    drawWall(app, canvas)

    app.fpsmeter.addFrame()

def drawTank(app, canvas, tank):
    corners = tank.getCorners()
    canvas.create_polygon(corners)

def drawBullets(app, canvas):
    for bullet in app.bullets:
        canvas.create_oval(bullet.x - bullet.r, bullet.y - bullet.r, bullet.x + bullet.r, bullet.y + bullet.r, fill ="black")

def drawWall(app, canvas):
    for wall in app.dummyMapCell.walls:
        canvas.create_rectangle(wall.x1, wall.y1, wall.x2, wall.y2, fill = "black")

runApp(width=WIDTH, height=HEIGHT)