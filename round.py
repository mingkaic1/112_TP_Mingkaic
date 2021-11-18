from maze import *
from map import *
from tank import *

class Round():
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.isOver = False
        self.maze = Maze(10, 10)
        self.map = Map(self.maze, 1000, 1000)

        # Create Tank objects
        self.tanks = []
        for i in range(self.numPlayers):
            # self.tanks[i] = Tank(100, 100)
            self.tanks.append(Tank(100, 100))