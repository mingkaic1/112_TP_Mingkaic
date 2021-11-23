import math

class GameAI():
    def __init__(self, tank, round):
        self.tank = tank
        self.round = round

        # Initialize .path
        #   - .path stores the MapCell path to nearest Tank
        self.path = None

        # Variables to control the AI's firing rate
        self.fireDelay = self.round.settings["AI_FIRE_DELAY"]
        self.framesSinceLastFire = 0

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
            pass # TO DO

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

    # Follow .path to move toward the target node
    def moveTowardNode(self):
        self.isInitialSteeringDone = False
        self.steer()
        if (self.isInitialSteeringDone == True):
            self.tank.startMovingForward()

    # Steer along the path
    def steer(self):
        angleToNextNode = self.getAngleToNextNode()
        # If AI is currently not facing next node
        if self.constrainAngle(self.tank.theta, 0, 360) != angleToNextNode:
            self.rotateTowardAngle(angleToNextNode)
        # If AI is facing next node
        else:
            self.stopRotation()
            self.isInitialSteeringDone = True

    # Keep on rotating (in the nearest direction: clockwise or counterclockwise) toward a target angle
    #   - Can be used when AI Tank is moving (steering), or stationary (rotating)
    #   - Does NOT stop steering once the target angle is reached
    #       - To avoid oscillation bug, use .stopRotation()
    def rotateTowardAngle(self, targetAngle):
        # Find the difference in angle to turn through (ensure within -180 to 180)
        dAngle = targetAngle - self.constrainAngle(self.tank.theta, 0, 360)
        dAngle = self.constrainAngle(dAngle, -180, 180)
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



    def stopRotation(self):
        self.tank.stopSteeringLeft()
        self.tank.stopSteeringRight()

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

    # Stop moving and rotate toward targetTank; if aiming directly, shoot (with the necessary fire delay)
    def shootAtTargetTank(self):
        self.framesSinceLastFire += 1
        self.tank.stopMovingForward()
        angleToTarget = self.getAngleToTargetTank()
        # If AI is not facing/aiming at .targetTank (needs to rotate)
        if self.constrainAngle(self.tank.theta, 0, 360) != angleToTarget:
            self.rotateTowardAngle(angleToTarget)
        # If AI is currently facing/aiming at .targetTank
        else:
            self.stopRotation() # This fixed oscillation bug
            if (self.framesSinceLastFire >= self.fireDelay):
                projectile = self.tank.fire()
                if projectile != None:
                    self.round.projectiles.append(projectile)
                    self.framesSinceLastFire = 0

    # Get the angle that .targetTank is in relation to AI tank
    def getAngleToTargetTank(self):
        dX = self.targetTank.x - self.tank.x
        dY = self.tank.y - self.targetTank.y
        atan2Angle = math.degrees(math.atan2(dX, dY)) # Angle from positive-x axis
        angleToTarget = self.roundToNearest(self.constrainAngle(360 - atan2Angle, 0, 360), self.round.settings["D_THETA"])
        return angleToTarget

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

# --------------------
# MATH & GEOMETRY HELPER FUNCTIONS
# --------------------

    def roundToNearest(self, value, d):
        return round((value // d) * d)

    def getPythagoreanDistance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

    # Return the "principle range" of an angle as defined by min (inclusive) and max (exclusive)
    #   - Basically, add 360 or -360 until angle falls within the range
    def constrainAngle(self, angle, min, max):
        while angle < min:
            angle += 360
        while angle >= 360:
            angle -= 360
        return angle