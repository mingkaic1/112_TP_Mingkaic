# --------------------
# SETTINGS.PY
# - settings constant
#   - All game settings (except TARGET_FPS) can be edited here
# --------------------

settings = {

    # Numbers of players and GameAIs
    #   - Any combination "works," but higher numbers become buggier
    #   - A Tank's controls must be defined below in "DEFAULT_CONTROLS" to be
    #     player-controlled (otherwise, it just sits there)
    #   - The Round will instantly end if there is only 1 Tank
    "NUM_PLAYERS": 3,
    "NUM_AI": 0,

    # Define keyboard controls here
    #   - If a non-AI Tank has no controls defined, it won't move, but the game
    #     wouldn't crash
    "DEFAULT_CONTROLS": {
        0: {
            "forward": "w",
            "backward": "s",
            "left": "a",
            "right": "d",
            "fire": "Tab"
        },
        1: {
            "forward": "Up",
            "backward": "Down",
            "left": "Left",
            "right": "Right",
            "fire": "Space"
        },
        # Add more player(s) here
    },

    # Define Tank colors here
    #   - Any Tank with no color defined would be colored black
    "PLAYER_COLORS": {
        0: "blue",
        1: "red",
        2: "green",
        3: "orange",
        4: "pink",
        5: "purple",
        6: "brown",
        7: "cyan"
    },

    # Size of game window
    "WINDOW_WIDTH": 1200,
    "WINDOW_HEIGHT": 1000,

    # Size of each square MapCell
    "MAPCELL_SIZE": 100,

    # Half the width of each Wall
    #   - Each Wall is placed along the boundary between 2 MapCells
    "WALL_HALF_WIDTH": 5,

    # Length (front to back) of each Tank
    "TANK_SIZE": 30,

    # The ratio of each Tank's width to its length (as defined by "TANK_SIZE")
    "TANK_PROPORTION": 0.75,

    # Radius of Projectiles
    "PROJECTILE_RADIUS": 4, # Default for Projectiles

    # Radius for Bullets
    "BULLET_RADIUS": 4,

    # Number of rows and columns of the Maze/Map
    "NUM_ROWS": 7,
    "NUM_COLS": 10,

    # Adjust this to ensure that the Map is drawn in the center of the window
    "MARGIN": 100,

    # Default speed of Tanks (number of pixels moved each frame)
    "TANK_SPEED": 3,

    # Important parameter in determining tank starting positions
    #   - Describes the minimum Manhattan separation (rows between + cols
    #     between) between any pair of 2 Tanks, as a ratio of the minimum
    #     of the number of rows and number of cols
    #   - E.g. If set to 0.4, and Map has 5 rows and 10 cols, game would
    #     ensure that any pair of Tanks would be separated by at least
    #     0.4 * 5 = 2 cells
    #   - For a particular combination of number of Tanks and size of Map,
    #     there is a maximum value for this parameter - if it is set to
    #     anything greater, the game would take an extremely long time to
    #     find accepted starting positions
    #   - Use a high value (e.g. 0.5) for 2 Tanks
    #   - Use 0 for larger numbers of Tanks, or to avoid crashing
    "MIN_STARTING_MANHATTAN_SEPARATION_RATIO": 0,

    # Bullets each Tank starts with (replenishes when Bullet despawns)
    "TANK_STARTING_AMMO": 5,

    # Maximum number of Bullets each Tank can have
    "TANK_MAX_AMMO": 5,

    # Number of frames each Projectile lasts before despawning
    "PROJECTILE_LIFETIME_FRAMES": 400,

    # Quantization level of the Tank's direction angle
    "D_THETA": 5,

    # Number of frames of delay in AI's firing rate
    #   - Without this setting, AI would fire once per frame, which is too fast
    "AI_FIRE_DELAY": 10
}