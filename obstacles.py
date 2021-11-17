class Obstacle():
    def __init__(self):
        pass

class Wall(Obstacle):

    # 'p1' and 'p2' are 2-tuples representing coordinates of top-left and bottom-right points
    def __init__(self, p1, p2):
        super().__init__()

        self.x1, self.y1 = p1
        self.x2, self.y2 = p2

    # Takes as input a Projectile object; if it will imminently collide, return
    #   its next position after bounce. Otherwise, return None.
    def checkBounce(self, projectile):
        # Bounce on lower surface
        if (projectile.y > self.y2) and (projectile.nextPos[1] < self.y2):
            pass

        # Bounce on upper surface
        if (projectile.y < self.y1) and (projectile.nextPos[1] > self.y1):
            pass

        # Bounce on left surface
        if (projectile.x < self.x1) and (projectile.nextPos[0] > self.x1):
            pass

        # Bounce on right surface
        if (projectile.x > self.x2) and (projectile.nextPos[0] < self.x2):
            pass

