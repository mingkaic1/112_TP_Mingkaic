settings = {
    "NUM_PLAYERS": 2,
    "NUM_AI": 0,
    "DEFAULT_CONTROLS": {
        1: {
            "forward": "Up",
            "backward": "Down",
            "left": "Left",
            "right": "Right",
            "fire": "Space"
        },
        0: {
            "forward": "w",
            "backward": "s",
            "left": "a",
            "right": "d",
            "fire": "Tab"
        }
    },
    "PLAYER_COLORS": {
        0: "blue",
        1: "red",
        2: "green",
        3: "orange",
        4: "pink",
        5: "purple",
        6: "brown"
    },
    "WINDOW_WIDTH": 1200,
    "WINDOW_HEIGHT": 1000,
    "MAPCELL_SIZE": 100,
    "WALL_HALF_WIDTH": 5,
    "TANK_SIZE": 30,
    "TANK_PROPORTION": 0.75,
    "PROJECTILE_RADIUS": 4, # Default for Projectiles
    "BULLET_RADIUS": 4,
    "NUM_ROWS": 7,
    "NUM_COLS": 10,
    "MARGIN": 100, # Adjust to center map
    "TANK_SPEED": 3,
    "MODE": "pvp", # "pvp" or "pvai"
    "MIN_STARTING_MANHATTAN_SEPARATION_RATIO": 0.1, # E.g. If NUM_COLS = 10, Tanks' starting positions must be at least 0.7*10 = 7 cells apart (Manhattan distance)
    "TANK_STARTING_AMMO": 5,
    "TANK_MAX_AMMO": 5,
    "PROJECTILE_LIFETIME_FRAMES": 400
}