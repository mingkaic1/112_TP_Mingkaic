import math

class Projectile():

    SPEED = 4
    RADIUS = 10
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
        self.nextX = self.x + self.vx
        self.nextY = self.y + self.vy
        for i in range(len(self.currentMapCell.walls)):
            wall = self.currentMapCell.walls[i]
            self.checkBounce(wall)
        self.x = self.nextX
        self.y = self.nextY
        self.decrementLife()

    # HELPER FUNCTION
    # Takes as input a Wall object, and if the Projectile will imminently bounce on Wall, change the .nextX and/or .nextY attributes
    def checkBounce(self, wall):

        # Check for bounce on BOTTOM surface of Wall
        if ((self.vy < 0) and                   # Projectile moving up
            (self.y - self.r > wall.y2) and     # Projectile below Wall
            (self.nextY - self.r < wall.y2)):   # Projectile will imminently move above Wall's bottom surface
            threshold = abs((self.vx / self.vy)*(self.y - wall.y2))     # Projectile must currently be at least this far within Wall's horizontal span
            if (wall.x1 + threshold < self.x < wall.x2 - threshold):
                # Bounce
                self.nextY = wall.y2 + (abs(self.vy) - (self.y - wall.y2)) + 2 * self.r
                self.vy = -self.vy

        # Check for bounce on TOP surface of Wall
        if ((self.vy > 0) and                   # Projectile moving down
            (self.y + self.r < wall.y1) and     # Projectile above Wall
            (self.nextY + self.r > wall.y1)):   # Projectile will imminently move below Wall's top surface
            threshold = abs((self.vx / self.vy) * (wall.y1 - self.y))
            if (wall.x1 + threshold < self.x < wall.x2 - threshold):
                # Bounce
                self.nextY = wall.y1 - (abs(self.vy) - (wall.y1 - self.y)) - 2 * self.r
                self.vy = -self.vy

        # Check for bounce on RIGHT surface of Wall
        if ((self.vx < 0) and                   # Projectile moving left
            (self.x - self.r > wall.x2) and     # Projectile to the right of Wall
            (self.nextX - self.r < wall.x2)):   # Projectile will imminently move to the left of Wall's right surface
            threshold = abs((self.vy / self.vx)*(self.x - wall.x2))
            if (wall.y1 + threshold < self.y < wall.y2 - threshold):
                # Bounce
                self.nextX = wall.x2 + (abs(self.vx) - (self.x - wall.x2)) + 2 * self.r
                self.vx = -self.vx

        # Check for bounce on LEFT surface of Wall
        if ((self.vx > 0) and                   # Projectile moving right
            (self.x + self.r < wall.x1) and     # Projectile to the left of Wall
            (self.nextX + self.r > wall.x1)):   # Projectile will imminently move to the right of Wall's left surface
            threshold = abs((self.vy / self.vx) * (wall.x1 - self.x))
            if (wall.y1 + threshold < self.y < wall.y2 - threshold):
                # Bounce
                self.nextX = wall.x1 - (abs(self.vx) - (wall.x1 - self.x)) - 2 * self.r
                self.vx = -self.vx

        # Crudely stop glitching through walls:
        # *Not sure if this is working at all - consider deleting and re-implementing something else
        if ((wall.x1 < self.x < wall.x2) and (wall.y1 < self.y < wall.y2)):
            if abs(self.vx) > abs(self.vy):
                self.vy = -self.vy
            else:
                self.vx = -self.vx

    # HELPER FUNCTION
    def decrementLife(self):
        self.framesLeft -= 1
        if (self.framesLeft <= 0):
            self.isDespawned = True

class Bullet(Projectile):
    def __init__(self, x, y, theta):
        super().__init__(x, y, theta)