# --------------------
# OBSTACLES.PY
# - Obstacle class
#   - Generic parent class for all obstacles (Walls, etc.) to handle object
#     collision etc.
# - Wall(Obstacle) class
#   - A simple rectangular Obstacle defined by 2 points
# --------------------

class Obstacle():
    def __init__(self):
        pass

class Wall(Obstacle):

    # 'p1' and 'p2' are 2-tuples representing coordinates of top-left and bottom-right points
    def __init__(self, p1, p2):
        super().__init__()

        self.x1, self.y1 = p1
        self.x2, self.y2 = p2

