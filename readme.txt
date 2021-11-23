--------------------
MK-AZ by Mingkai Chen (Mingkaic)
--------------------

MK-AZ is a 2D Python game where players steer tanks around a maze-based map,
fighting other players and/or game AIs with projectiles that bounce off walls.

The game map is built upon a randomly generated maze, but gameplay is not
restricted to the map grid (i.e. tanks and projectiles can move in any
direction in 2D within the bounds of the walls).

--------------------
1. HOW TO RUN
--------------------

First, ensure that all required Python modules are installed (see below for
list). For most systems, all required modules should already be installed with
Python as MK-AZ does not use any module outside of the Python Standard Library.

Run main.py to start the game.

All game settings (except TARGET_FPS) can be changed by editing the dictionary
values in settings.py.

To change TARGET_FPS (which affects the frame refresh delay), edit the
TARGET_FPS global constant in main.py. A value of 60 is recommended for most
computers and displays. A running average of the current measured FPS is
displayed in the top-left corner of the window during gameplay.

MK-AZ uses the CMU_112_Graphics tkinter wrapper used in Carnegie Mellon
University's 15-112 Fundamentals of Programming and Computer Science course.
This comes in the cmu_112_graphics.py file and does not need to be installed.

--------------------
2. LIBRARIES & MODULES
--------------------

Python Standard Library:
    tkinter
    math
    random
    time
    statistics

CMU 15-112 Fundamentals of Programming and Computer Science:
    cmu_112_graphics.py

--------------------
3. SHORTCUT COMMANDS
--------------------

Press R to kill the current round and start a new round.