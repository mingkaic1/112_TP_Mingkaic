class Obstacle():
    def __init__(self):
        pass

class Wall(Obstacle):

    # 'p1' and 'p2' are 2-tuples representing coordinates of top-left and bottom-right points
    def __init__(self, p1, p2):
        super().__init__()
