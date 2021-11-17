class Map():
    def __init__(self, maze = None):
        self.grid = []
        if (maze != None):
            self.makeGrid(maze)

    def makeGrid(self, maze):
        if (isinstance(maze, Maze) == False):
            return
        pass # Convert Maze to Map

class MapCell():
    def __init__(self):
        pass

class Wall():
    def __init__(self):
        pass

class Space():
    def __init__(self):
        pass