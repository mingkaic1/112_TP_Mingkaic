import math
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
