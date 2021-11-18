from round import *

class Game():

    DEFAULT_CONTROLS = {
        0: {
            "forward": "Up",
            "backward": "Down",
            "left": "Left",
            "right": "Right",
            "fire": "Space"
        },
        1: {
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
        for i in range(self.numPlayers):
            self.scores[i] = 0

        # Initialize controls
        self.controls = {}
        for i in range(self.numPlayers):
            self.controls[i] = self.DEFAULT_CONTROLS[i]

        # Initialize round number
        self.roundNum = 0

        # Initialize round
        self.round = None

    def startRound(self):
        self.round = Round(self.numPlayers)
        self.roundNum += 1
        print(f"Game: Round {self.roundNum} started!")