from cmu_112_graphics import *
from maze import *
from map import *
from tank import *
from projectiles import *
from obstacles import *
from fpsmeter import *
from round import *
from game import *

# Settings
WIDTH = 1200
HEIGHT = 1000

MAPCELL_SIZE = 100
WALL_HALF_WIDTH = 5
TANK_SIZE = 30
TANK_PROPORTION = 0.75
PROJECTILE_RADIUS = 4


# --------------------
# START APP
# --------------------

def appStarted(app):
    pass

# --------------------
# GAME MODE
# --------------------

def redrawAll(app, canvas):
    # MapCell
    # canvas.create_rectangle(100, 100, 100 + MAPCELL_SIZE, 100 + MAPCELL_SIZE)
    # Walls
    canvas.create_rectangle(100 - WALL_HALF_WIDTH,
                            100 - WALL_HALF_WIDTH,
                            100 + MAPCELL_SIZE + WALL_HALF_WIDTH,
                            100 + WALL_HALF_WIDTH,
                            fill = "black")
    canvas.create_rectangle(100 - WALL_HALF_WIDTH,
                            100 - WALL_HALF_WIDTH,
                            100 + WALL_HALF_WIDTH,
                            100 + MAPCELL_SIZE+ WALL_HALF_WIDTH,
                            fill="black")
    canvas.create_rectangle(100 - WALL_HALF_WIDTH,
                            100 + MAPCELL_SIZE - WALL_HALF_WIDTH,
                            100 + MAPCELL_SIZE + WALL_HALF_WIDTH,
                            100 + MAPCELL_SIZE + WALL_HALF_WIDTH,
                            fill="black")
    # Tank
    canvas.create_rectangle(120, 120, 120 + TANK_PROPORTION * TANK_SIZE, 120 + TANK_SIZE, fill = "black")
    # Projectile
    canvas.create_oval(200, 150, 200 + 2*PROJECTILE_RADIUS, 150 + 2*PROJECTILE_RADIUS, fill = "black")


runApp(width = WIDTH, height = HEIGHT)