class GameAI():
    def __init__(self, tank, round):
        self.tank = tank
        self.round = round

        # Initialize .path, .route, .targetTank
        #   - .path stores the MapCell path to nearest Tank
        #   - .route stores the x, y conversion of path
        #   - .targetTank is the Tank that AI is targeting
        self.path = None
        self.getNewPath()

    def update(self):
        if self.path != None:
            # If .targetTank is not yet within line-of-sight
            if self.inLineOfSight() == False:
                self.moveTowardTargetTank()
            # If .targetTank is within line-of-sight
            else:
                self.shootAtTargetTank()

    # Check if .targetTank is within line of sight (and hence AI can begin shooting)
    #   - Currently implemented naively (checking if .path is a straight line of nodes)
    #   - Better way: Linear algebra (vector/line segment to .targetTank, and check if it intersects any Wall)
    def inLineOfSight(self):
        isInSameRow = True
        isInSameCol = True
        for i in range(len(self.path) - 1):
            if (self.path[i][0] != self.path[i + 1][0]):
                isInSameRow = False
            if (self.path[i][1] != self.path[i + 1][1]):
                isInSameCol = False
        if (isInSameRow == True) or (isInSameCol == True):
            return True
        return False


    def moveTowardTargetTank(self):
        print(self.tank.theta)

    def shootAtTargetTank(self):
        pass

    # Get new path by calling pathfinding algorithms in .round.graph
    def getNewPath(self):
        print("getting new path")
        # Find the nearest Tank to target
        minDistance = float("inf")
        for i in range(self.round.settings["NUM_PLAYERS"]):
            tankX = self.round.tanks[i].x
            tankY = self.round.tanks[i].y
            distance = self.getPythagoreanDistance((tankX, tankY), (self.tank.x, self.tank.y))
            if distance <= minDistance:
                minDistance = distance
                self.targetTank = self.round.tanks[i]
        # Get .path by calling pathfinding algorithms
        # (If .targetTank has no .centralMapCell (likely not yet updated at start of round), skip)
        if (self.targetTank.centralMapCell != None) and (self.tank.centralMapCell != None):
            selfNode = (self.tank.centralMapCell.row, self.tank.centralMapCell.col)
            targetNode = (self.targetTank.centralMapCell.row, self.targetTank.centralMapCell.col)
            self.path = self.round.graph.findPath(selfNode, targetNode)
            print(self.path)

    # HELPER FUNCTION
    def getPythagoreanDistance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5