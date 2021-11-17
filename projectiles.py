import math

class Projectile():

    SPEED = 7
    RADIUS = 2
    LIFETIME_FRAMES = 50

    def __init__(self, x, y, theta): # 'theta' is angle in degrees from North

        # Initialize position
        self.x = x
        self.y = y

        # Initialize velocity
        #   - Store speed as vx and vy (theta only used temporarily in initializing projectile)
        self.vx = -self.SPEED * math.sin(math.radians(theta))
        self.vy = -self.SPEED * math.cos(math.radians(theta))

        # Initialize size
        self.r = self.RADIUS

        # Initialize despawn countdown
        self.framesLeft = self.LIFETIME_FRAMES
        self.isDespawned = False

        # Initialize .currentMapCell
        #   - Stores the MapCell object on which the projectile is currently located
        self.currentMapCell = None

    # SOON OBSOLETE
    def bounce(self, isVertical = True): # True for vertical bounce; False for horizontal bounce
        if (isVertical == True):
            self.vy = -self.vy
        else:
            self.vx = -self.vx

    def setCurrentCell(self, mapCell):
        self.currentMapCell = mapCell

    def move(self):
        nextPos = (self.x + self.vx,
                   self.y + self.vy)
        for i in range(len(self.currentMapCell.walls)):
            result = self.currentMapCells.walls[i].checkBounce(self)
            if result != None:
                nextPos = result
        self.x, self.y = self.nextPos
        self.decrementLife()

    # HELPER FUNCTION
    def decrementLife(self):
        self.framesLeft -= 1
        if (self.framesLeft <= 0):
            self.isDespawned = True

class Bullet(Projectile):
    def __init__(self, x, y, theta):
        super().__init__(x, y, theta)