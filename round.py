class Round():
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.isOver = False
        self.maze = Maze(10, 10)
        self.map = Map(self.maze, 1000, 1000)

        # Create Tank objects
        self.tanks = {}
        for i in range(1, self.numPlayers + 1):
            self.tanks[i] = Tank(0, 0)