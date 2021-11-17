class Sprite():

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def makePolygon(self, polygon):
        # Store a list of tuples, each represnting coordinates of a point
        self.polygon = polygon
        
