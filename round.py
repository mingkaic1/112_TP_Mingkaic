from maze import *
from map import *
from tank import *

class Round():
    def __init__(self, settings):
        self.settings = settings
        self.numPlayers = self.settings["NUM_PLAYERS"]
        self.isOver = False
        self.maze = Maze(self.settings["NUM_ROWS"], self.settings["NUM_COLS"])
        self.map = Map(self.maze, self.settings)

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
            row = int(self.projectiles[i].y // self.mapCellSize)
            col = int(self.projectiles[i].x // self.mapCellSize)
            print(row, col)


            currentMapCell = self.map.getMapCell(row, col)
            self.projectiles[i].setCurrentCell(currentMapCell)
            print("check")
            self.projectiles[i].move()

    def updateTanks(self):
        for i in range(len(self.tanks)):
            self.tanks[i].update()

    def getProjectilesTranslatedCoordinates(self):
        result = []
        for i in range(len(self.projectiles)):
            result.append((self.projectiles[i].x - self.projectiles[i].r + self.settings["MARGIN"],
                           self.projectiles[i].y - self.projectiles[i].r + self.settings["MARGIN"],
                           self.projectiles[i].x + self.projectiles[i].r + self.settings["MARGIN"],
                           self.projectiles[i].y + self.projectiles[i].r + self.settings["MARGIN"]))
        return result

    def getTanksTranslatedCorners(self):
        result = []
        for i in range(len(self.tanks)):
            corners = self.tanks[i].getCorners()
            translatedCorners = []
            for corner in corners:
                translatedCorners.append((corner[0] + self.settings["MARGIN"],
                                          corner[1] + self.settings["MARGIN"]))
            result.append(translatedCorners)
        return result


    def printDebugInfo(self):
        print("All MapCells and linked Walls:")
