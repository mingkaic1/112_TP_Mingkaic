from maze import *
from map import *
from tank import *

class Round():
    def __init__(self, settings):
        self.settings = settings
        self.numPlayers = self.settings["NUM_PLAYERS"]
        self.isOver = False
        self.maze = Maze(10, 10)
        self.map = Map(self.maze, 1000, 1000)

        # Initialize .tanks and Tank objects
        self.tanks = []
        for i in range(self.numPlayers):
            self.tanks.append(Tank(100, 100))

        # Initialize .projectiles
        self.projectiles = []

        # Initialize .mapCellSize (a setting variable, for streamlining .updateProjectiles())
        self.mapCellSize = self.settings["MAPCELL_SIZE"]

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

    def updateProjectiles(self):
        for i in range(len(self.projectiles)):
            row = int(self.projectiles[i].x // self.mapCellSize)
            col = int(self.projectiles[i].y // self.mapCellSize)
            print(row, col)
            # Temp
            if not ((0 < row < 10) and (0 < col < 10)):
                continue

            currentMapCell = self.map.getMapCell(row, col)
            self.projectiles[i].setCurrentCell(currentMapCell)
            print("check")
            self.projectiles[i].move()

    def printDebugInfo(self):
        print("All MapCells and linked Walls:")
