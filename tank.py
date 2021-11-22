import math
from projectiles import *

class Tank():

    SIZE = 20
    speed = 6
    D_THETA = 5

    def __init__(self, settings, id, x = 0, y = 0, theta = 0):
        self.settings = settings
        self.x, self.y = x, y
        self.length = self.settings["TANK_SIZE"]
        self.width = self.length * self.settings["TANK_PROPORTION"]
        self.speed = self.settings["TANK_SPEED"]
        self.theta = theta # Facing angle in degrees from North
        self.id = id

        # Init steering & movement booleans
        self.isSteeringLeft = False
        self.isSteeringRight = False
        self.isMovingForward = False
        self.isMovingBackward = False

        # Init ammo counter
        self.ammo = self.settings["TANK_STARTING_AMMO"]
        self.maxAmmo = self.settings["TANK_MAX_AMMO"]

        # Initialize .currentMapCells (list of 9 MapCell objects centered around Tank)
        self.currentMapCells = []

        # Initialize .corners
        self.corners = []
        self.updateCorners()

    def getCorners(self):
        return self.corners

    # Return list of coords of 4 corners, counterclockwise from front-right
    def updateCorners(self):
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
        self.corners = [corner0, corner1, corner2, corner3]

    def setCurrentMapCells(self, mapCells):
        self.currentMapCells = mapCells

    # Update
    def update(self):
        self.move()
        self.steer()
        # Update .corners
        self.updateCorners()
        for i in range(len(self.currentMapCells)):
            for j in range(len(self.currentMapCells[i].walls)):
                wall = self.currentMapCells[i].walls[j]
                if wall != None:
                    self.checkCollision(wall)

    def checkCollision(self, wall):
        xMin, xMax, yMin, yMax = self.getMinMaxXY()

        # NOTE:
        # Current collision detection does NOT use Separating Axis Theorem (SAT).
        # The Tank has to be entirely out of a Wall's span for there to be no
        # collision (i.e. the Tank has to move a few pixels "around" the Wall's
        # corner to be able to stop colliding)
        #
        # TO DO:
        # Implement SAT (Vector classes, function for projection vector, etc.)
        #
        # ALSO, right now this is very jank (tends to collide with 2 walls at the corner at the same time)

        # Check for collision on BOTTOM surface of Wall
        #   - If up-most point of Tank polygon is above bottom surface wall,
        #     while down-most point is below
        if ((yMin < wall.y2) and
            (yMax > wall.y2) and not
            ((xMax < wall.x1 + 2) or (xMin > wall.x2 - 2))):
            self.y += (wall.y2 - yMin + 1)
            self.updateCorners()
            xMin, xMax, yMin, yMax = self.getMinMaxXY()

        # Check for collision on TOP surface of Wall
        if ((yMax > wall.y1) and
            (yMin < wall.y1) and not
            ((xMax < wall.x1 + 2) or (xMin > wall.x2 - 2))):
            self.y -= (yMax - wall.y1 + 1)
            self.updateCorners()
            xMin, xMax, yMin, yMax = self.getMinMaxXY()

        # Check for collision on RIGHT surface of Wall
        if ((xMin < wall.x2) and
            (xMax > wall.x2) and not
            ((yMax < wall.y1 + 2) or (yMin > wall.y2 - 2))):
            self.x += (wall.x2 - xMin + 1)
            self.updateCorners()
            xMin, xMax, yMin, yMax = self.getMinMaxXY()

        # Check for collision on BOTTOM surface of Wall
        if ((xMax > wall.x1) and
            (xMin < wall.x1) and not
            ((yMax < wall.y1 + 2) or (yMin > wall.y2 - 2))):
            self.x -= (xMax - wall.x1 + 1)
            self.updateCorners()
            xMin, xMax, yMin, yMax = self.getMinMaxXY()

    # HELPER FUNCTION
    #   - Until SAT collision detection implemented
    def getMinMaxXY(self):
        xValues = []
        yValues = []
        for i in range(len(self.corners)):
            xValues.append(self.corners[i][0])
            yValues.append(self.corners[i][1])
        xMin = min(xValues)  # Left-most x value
        xMax = max(xValues)  # Right-most x value
        yMin = min(yValues)  # Up-most y value
        yMax = max(yValues)  # Down-most y value
        return xMin, xMax, yMin, yMax

    # Steering

    def steerLeft(self):
        self.theta += self.D_THETA

    def steerRight(self):
        self.theta -= self.D_THETA

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
        # return Bullet(self.x, self.y, self.theta)
        return Bullet(self.x - (self.length/2)*math.sin(math.radians(self.theta)),
                      self.y - (self.length/2)*math.cos(math.radians(self.theta)),
                      self.theta,
                      self.settings["PROJECTILE_LIFETIME_FRAMES"])

    def replenishAmmo(self, amount = 1):
        self.ammo += amount
        if (self.ammo > self.maxAmmo):
            self.ammo = self.maxAmmo
