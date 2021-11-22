class GameAI():
    def __init__(self, tank, round):
        self.tank = tank
        self.round = round

        # Initialize .path, .route, .targetTank
        #   - .path stores the MapCell path to nearest Tank
        #   - .route stores the x, y conversion of path
        #   - .targetTank is the Tank that AI is targeting
        self.getNewPath()

    def update(self):
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