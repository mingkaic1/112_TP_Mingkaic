import math

class Projectile():

    SPEED = 7
    R = 2
    LIFETIME = 50

    def __init__(self, x, y, theta): # 'theta' is angle in degrees from North
        self.x = x
        self.y = y
        self.vx = -self.SPEED * math.sin(math.radians(theta))
        self.vy = -self.SPEED * math.cos(math.radians(theta))
        self.lifeLeft = self.LIFETIME
        self.shouldDespawn = False

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
        self.lifeLeft -= 1
        if (self.lifeLeft <= 0):
            self.shouldDespawn = True

class Bullet(Projectile):
    def __init__(self, x, y, theta):
        super().__init__(x, y, theta)