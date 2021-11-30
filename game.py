# --------------------
# GAME.PY
# - Game class
#   - Handles high-level game mechanics (keyboard controls & starting rounds)
# --------------------

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

    def __init__(self, settings):
        self.settings = settings

        self.numPlayers = settings["NUM_PLAYERS"]
        self.numAI = settings["NUM_AI"]

        # Initialize score
        self.scores = {}
        for i in range(self.numPlayers + self.numAI):
            self.scores[i] = 0

        # Initialize controls
        self.controls = {}
        for i in range(self.numPlayers):
            self.controls[i] = self.settings["DEFAULT_CONTROLS"].get(i, None)

        # Initialize round number
        self.roundNum = 0

        # Initialize round
        self.round = None

    def startRound(self):
        self.round = Round(self.settings)
        self.roundNum += 1
        print(f"Game: Round {self.roundNum} started!")

    def checkKeyPressed(self, key):
        for i in self.controls:
            if (self.controls[i] != None):
                for binding in self.controls[i]:
                    if key == self.controls[i][binding]:
                        self.round.controlTank(i, binding, "pressed")
                        return

    def checkKeyReleased(self, key):
        for i in self.controls:
            if (self.controls[i] != None):
                for binding in self.controls[i]:
                    if key == self.controls[i][binding]:
                        self.round.controlTank(i, binding, "released")
                        return

    def checkHits(self):
        result = self.round.checkHits()
        # If there is 1 Tank remaining after hits (round.checkHits() returns Tank.id)
        if result != None:
            self.scores[result] += 1
            self.round.isOver = True
