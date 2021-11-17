import math

class Projectile():

    SPEED = 7
    RADIUS = 2
    LIFETIME_FRAMES = 50

    def __init__(self, x, y, theta): # 'theta' is angle in degrees from North
        self.x = x
        self.y = y
        # Store speed as vx and vy (theta only used temporarily in initializing projectile)
        self.vx = -self.SPEED * math.sin(math.radians(theta))
        self.vy = -self.SPEED * math.cos(math.radians(theta))
        self.framesLeft = self.LIFETIME_FRAMES
        self.isDespawned = False

    def bounce(self, isVertical = True): # True for vertical bounce; False for horizontal bounce
        if (isVertical == True):
            self.vy = -self.vy
        else:
            self.vx = -self.vx

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.decrementLife()

    def decrementLife(self):
        self.framesLeft -= 1
        if (self.framesLeft <= 0):
            self.isDespawned = True

class Bullet(Projectile):
    def __init__(self, x, y, theta):
        super().__init__(x, y, theta)