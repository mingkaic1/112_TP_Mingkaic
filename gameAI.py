import math

class GameAI():
    def __init__(self, tank, round):
        self.tank = tank
        self.round = round

        # Initialize .path, .route, .targetTank
        #   - .path stores the MapCell path to nearest Tank
        #   - .route stores the x, y conversion of path
        #   - .targetTank is the Tank that AI is targeting
        self.path = None

        self.framesSinceLastFire = 0

        self.fireDelay = self.round.settings["AI_FIRE_DELAY"]

    def update(self):
        # If AI still has ammo, hunt for the nearest player Tank
        if self.tank.ammo > 0:
            self.getPathToTargetTank()
            # Skip this .update() iteration if .getPathToTargetTank() failed to give a path
            #   - (May happen at beginning of round, when player Tank(s) have yet to be assigned MapCells)
            if self.path != None:
                # If .targetTank is not yet within line-of-sight
                if (self.inLineOfSight() == False):
                    self.moveTowardNode()
                # If .targetTank is within line-of-sight
                else:
                    self.shootAtTargetTank()
        # If AI has no ammo, avoid/ run away from players
        else:
            pass

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

    def moveTowardNode(self):
        self.isInitialSteeringDone = False
        self.steer()
        if (self.isInitialSteeringDone == True):
            self.tank.startMovingForward()

    def steer(self):
        angleToNextNode = self.getAngleToNextNode()
        # If AI is currently not facing next node
        if self.constrainAngle(self.tank.theta) != angleToNextNode:
            self.rotateToAngle(angleToNextNode)
        # If AI is facing next node
        else:
            self.stopRotation()
            self.isInitialSteeringDone = True

    def rotateToAngle(self, targetAngle):
        # Find the difference in angle to turn through (ensure within -180 to 180)
        dAngle = targetAngle - self.constrainAngle(self.tank.theta)
        while dAngle <= -180:
            dAngle += 360
        while dAngle > 180:
            dAngle -= 360
        # If faster to turn counterclockwise
        if (dAngle > 0):
            self.tank.startSteeringLeft()
            self.tank.stopSteeringRight()
        # If faster to turn clockwise
        elif (dAngle < 0):
            self.tank.startSteeringRight()
            self.tank.stopSteeringLeft()
        # If targetAngle is already reached
        else:
            self.stopRotation()

    # Constrain an angle to 0-359
    def constrainAngle(self, angle):
        while angle < 0:
            angle += 360
        while angle >= 360:
            angle -= 360
        return angle

    def stopRotation(self):
        self.tank.stopSteeringLeft()
        self.tank.stopSteeringRight()

    # HELPER FUNCTION
    # Get the angle (0, 90, 180, 270 deg) that the next node is in relation to current node
    def getAngleToNextNode(self):
        currentNode = self.path[0]
        nextNode = self.path[1]
        # If nextNode is in same row
        if nextNode[0] == currentNode[0]:
            # If nextNode is to the left
            if nextNode[1] < currentNode[1]:
                angleToNextNode = 90
            # If nextNode is to the right
            else:
                angleToNextNode = 270
        # If nextNode is in same col
        else:
            # If nextNode is above
            if nextNode[0] < currentNode[0]:
                angleToNextNode = 0
            # If nextNode is below
            else:
                angleToNextNode = 180
        return angleToNextNode

    def shootAtTargetTank(self):
        self.framesSinceLastFire += 1
        self.tank.stopMovingForward()
        angleToTarget = self.getAngleToTargetTank()
        print(angleToTarget, self.constrainAngle(self.tank.theta))
        # If AI is not facing/aiming at .targetTank (needs to rotate)
        if self.constrainAngle(self.tank.theta) != angleToTarget:
            self.rotateToAngle(angleToTarget)
        # If AI is currently facing/aiming at .targetTank
        else:
            self.stopRotation() # This fixed oscillation bug
            if (self.framesSinceLastFire >= self.fireDelay):
                projectile = self.tank.fire()
                if projectile != None:
                    self.round.projectiles.append(projectile)
                    self.framesSinceLastFire = 0

    # HELPER FUNCTION
    # Get the angle that .targetTank is in relation to AI tank
    def getAngleToTargetTank(self):
        dX = self.targetTank.x - self.tank.x
        dY = self.tank.y - self.targetTank.y
        atan2Angle = math.degrees(math.atan2(dX, dY)) # Angle from positive-x axis
        angleToTarget = self.roundToNearest(self.constrainAngle(360 - atan2Angle), self.round.settings["D_THETA"])
        return angleToTarget

    # HELPER FUNCTION
    def roundToNearest(self, value, d):
        return round((value // d) * d)

    # Get new path by calling pathfinding algorithms in .round.graph
    def getPathToTargetTank(self):
        # Find the nearest Tank to target
        minDistance = float("inf")
        for i in range(self.round.settings["NUM_PLAYERS"]):
            # Skip if player Tank is already dead
            if (self.round.tanks[i].isAlive == False):
                continue
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

    # HELPER FUNCTION
    def getPythagoreanDistance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5