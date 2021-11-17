class Game():

    DEFAULT_CONTROLS = {
        1: {
            "forward": "Up",
            "backward": "Down",
            "left": "Left",
            "right": "Right",
            "fire": "Space"
        },
        2: {
            "forward": "w",
            "backward": "s",
            "left": "a",
            "right": "d",
            "fire": "Tab"
        }
    }

    def __init__(self, numPlayers = 2):
        self.numPlayers = numPlayers

        # Initialize score
        self.scores = {}
        for i in range(1, self.numPlayers + 1):
            self.scores[i] = 0

        # Initialize controls
        self.controls = {}
        for i in range(1, self.numPlayers + 1):
            self.controls[i] = self.DEFAULT_CONTROLS[i]

        # Initialize round number
        self.roundNum = 0

    def startRound(self):
        self.round = Round(self.numPlayers)
        self.roundNum += 1