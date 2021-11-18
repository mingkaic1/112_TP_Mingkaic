from maze import *
from map import *
from tank import *

class Round():
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.isOver = False
        self.maze = Maze(10, 10)
        self.map = Map(self.maze, 1000, 1000)

        # Initialize .tanks and Tank objects
        self.tanks = []
        for i in range(self.numPlayers):
            self.tanks.append(Tank(100, 100))

        # Initialize .projectiles
        self.projectiles = []

    def controlTank(self, tankIndex, binding, keyStatus):

        if keyStatus == "pressed":
            if binding == "forward":
                self.tanks[tankIndex].startMovingForward()
            if binding == "backward":
                self.tanks[tankIndex].startMovingBackward()
            if binding == "left":
                self.tanks[tankIndex].startSteeringLeft()
            if binding == "right":
                self.tanks[tankIndex].startSteeringRight()
            if binding == "fire":
                projectile = self.tanks[tankIndex].fire()
                if projectile != None:
                    self.projectiles.append(projectile)

        if keyStatus == "released":
            if binding == "forward":
                self.tanks[tankIndex].stopMovingForward()
            if binding == "backward":
                self.tanks[tankIndex].stopMovingBackward()
            if binding == "left":
                self.tanks[tankIndex].stopSteeringLeft()
            if binding == "right":
                self.tanks[tankIndex].stopSteeringRight()