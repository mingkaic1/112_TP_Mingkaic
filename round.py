import random

from maze import *
from map import *
from tank import *
from graph import *

class Round():
    def __init__(self, settings):
        self.settings = settings
        self.numPlayers = self.settings["NUM_PLAYERS"]
        self.isOver = False
        self.maze = Maze(self.settings["NUM_ROWS"], self.settings["NUM_COLS"])
        self.map = Map(self.maze, self.settings)
        self.graph = Graph(self.maze)

        print(self.graph.graphDict)

        # Randomize tank starting locations and directions, and initialize .tank objects
        self.initTanks()

        # Initialize .projectiles
        self.projectiles = []

        # Initialize .mapCellSize (a setting variable, for streamlining .updateProjectiles())
        self.mapCellSize = self.settings["MAPCELL_SIZE"]


        print("path finding start")
        print(self.graph.findPathDijkstra((0, 0), (5, 5)))
        print("path finding done")

    def initTanks(self):
        # Keep on generating new combinations of starting positions, until a valid one is found
        while True:
            tankStartingPositions = []  # List of 3-tuples, each representing (row, col, theta)
            isValid = True
            for i in range(self.numPlayers):
                startingRow = random.randint(0, self.settings["NUM_ROWS"] - 1)
                startingCol = random.randint(0, self.settings["NUM_COLS"] - 1)
                tankStartingPositions.append((startingRow, startingCol))
                startingAngle = random.randint(0, 359)
                # Check if the starting position is far enough away from other tanks' starting positions
                for j in range(i):
                    if (self.getManhattanSeparation(tankStartingPositions[i],
                                                    tankStartingPositions[j]) <
                        self.settings["MIN_STARTING_MANHATTAN_SEPARATION_RATIO"] *
                        min([self.settings["NUM_ROWS"], self.settings["NUM_COLS"]])):
                        isValid = False
            if (isValid == True):
                break
        # Make random list of starting angles
        tankStartingAngles = [random.randint(0, 359) for i in range(self.numPlayers)]
        # Initialize .tank objects
        self.tanks = []
        for id in range(self.numPlayers):
            startingX = (tankStartingPositions[id][1] + 0.5) * self.settings["MAPCELL_SIZE"]
            startingY = (tankStartingPositions[id][0] + 0.5) * self.settings["MAPCELL_SIZE"]
            startingTheta = tankStartingAngles[id]
            self.tanks.append(Tank(self.settings,
                                   id,
                                   startingX,
                                   startingY,
                                   startingTheta))

    # HELPER FUNCTION
    def getManhattanSeparation(self, position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position1[1])

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
            currentMapCell = self.map.getMapCell(row, col)
            self.projectiles[i].setCurrentCell(currentMapCell)
            self.projectiles[i].move()

    def updateTanks(self):
        for i in range(len(self.tanks)):
            row = int(self.tanks[i].y // self.mapCellSize)
            col = int(self.tanks[i].x // self.mapCellSize)
            currentMapCells = []
            for dRow in [-1, 0, 1]:
                for dCol in [-1, 0, 1]:
                    rowToAdd = row + dRow
                    colToAdd = col + dCol
                    if (rowToAdd in range(0, self.map.numRows)) and (colToAdd in range(0, self.map.numCols)):
                        currentMapCells.append(self.map.getMapCell(rowToAdd, colToAdd))
            self.tanks[i].setCurrentMapCells(currentMapCells)
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

    # Check whether any projectile hits any tank; if so, remove the projectile and tank.
    # If only 1 tank is remaining (i.e. wins round), return tank.id
    def checkHits(self):
        # TEMP: Really basic hit detection right now. TO CHANGE
        i = 0
        while i < len(self.tanks):
            isHitDetected = False
            j = 0
            while j < len(self.projectiles):
                # If Tank and Projectile hit (within a certain Pythagorean distance)
                if (((self.tanks[i].x - self.projectiles[j].x) ** 2 + (self.tanks[i].y - self.projectiles[j].y) ** 2) ** 0.5 < self.settings["TANK_SIZE"] / 2):
                    self.tanks.pop(i)
                    self.projectiles.pop(j)
                    isHitDetected = True
                    break
                j += 1
            if isHitDetected == False:
                i += 1
            isHitDetected = False

        # Check win/draw conditions
        if len(self.tanks) == 1:
            return self.tanks[0].id
        elif len(self.tanks) == 0:
            pass # DRAW - how to handle this?



