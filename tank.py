from cmu_112_graphics import *
import math

from fpsmeter import *
from projectiles import *

class Tank():

    speed = 4
    dTheta = 10
    STARTING_AMMO = 5
    MAX_AMMO = 5

    def __init__(self, x = 0, y = 0):
        self.x, self.y = x, y
        self.size = 20
        self.length = self.size # Derived
        self.width = self.length * 0.75 # Derived

        self.theta = 0 # Facing angle in degrees from North

        self.isSteeringLeft = False
        self.isSteeringRight = False
        self.isMovingForward = False
        self.isMovingBackward = False

        self.ammo = self.STARTING_AMMO

    # Return list of coords of 4 corners, counterclockwise from front-right
    def getCorners(self):
        self.sin = math.sin(math.radians(self.theta))
        self.cos = math.cos(math.radians(self.theta))
        corner0 = (
            self.x - (self.length/2)*self.sin + (self.width/2)*self.cos,
            self.y - (self.length/2)*self.cos - (self.width/2)*self.sin
        )
        corner1 = (
            self.x - (self.length/2)*self.sin - (self.width/2)*self.cos,
            self.y - (self.length/2)*self.cos + (self.width/2)*self.sin
        )
        corner2 = (
            self.x + (self.length / 2) * self.sin - (self.width / 2) * self.cos,
            self.y + (self.length / 2) * self.cos + (self.width / 2) * self.sin
        )
        corner3 = (
            self.x + (self.length / 2) * self.sin + (self.width / 2) * self.cos,
            self.y + (self.length / 2) * self.cos - (self.width / 2) * self.sin
        )
        return corner0, corner1, corner2, corner3

    # Steering

    def steerLeft(self):
        self.theta += self.dTheta

    def steerRight(self):
        self.theta -= self.dTheta

    def startSteeringLeft(self):
        self.isSteeringLeft = True

    def startSteeringRight(self):
        self.isSteeringRight = True

    def stopSteeringLeft(self):
        self.isSteeringLeft = False

    def stopSteeringRight(self):
        self.isSteeringRight = False

    def steer(self):
        if (self.isSteeringLeft == True) and (self.isSteeringRight == False):
            self.steerLeft()
        elif (self.isSteeringRight == True) and (self.isSteeringLeft == False):
            self.steerRight()

    # Moving

    def move(self):
        if (self.isMovingForward == True) and (self.isMovingBackward == False):
            self.moveForward()
        elif (self.isMovingBackward == True) and (self.isMovingForward == False):
            self.moveBackward()

    def moveForward(self):
        self.sin = math.sin(math.radians(self.theta))
        self.cos = math.cos(math.radians(self.theta))
        self.x -= self.speed * self.sin
        self.y -= self.speed * self.cos

    def moveBackward(self):
        self.sin = math.sin(math.radians(self.theta))
        self.cos = math.cos(math.radians(self.theta))
        self.x += self.speed * self.sin
        self.y += self.speed * self.cos

    def startMovingForward(self):
        self.isMovingForward = True

    def startMovingBackward(self):
        self.isMovingBackward = True

    def stopMovingForward(self):
        self.isMovingForward = False

    def stopMovingBackward(self):
        self.isMovingBackward = False

    # Fire

    # Return a Bullet object
    def fire(self):
        if self.ammo <= 0:
            return None
        self.ammo -= 1
        return Bullet(self.x, self.y, self.theta)

    def replenishAmmo(self, amount = 1):
        self.ammo += amount
        if (self.ammo > self.MAX_AMMO):
            self.ammo = self.MAX_AMMO

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
        if (app.bullets[i].shouldDespawn == True):
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
        canvas.create_oval(bullet.x - bullet.R, bullet.y - bullet.R, bullet.x + bullet.R, bullet.y + bullet.R, fill = "black")

runApp(width=WIDTH, height=HEIGHT)