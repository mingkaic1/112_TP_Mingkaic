def drawWalls(app, canvas):

    for wall in app.game.round.map.translatedWallRectangles:
        canvas.create_rectangle(*wall, fill="black")

def drawTanks(app, canvas):

    # Get list of lists, each containing 4 tuples representing corners of tank polygon
    tanksTranslatedCorners = app.game.round.getTanksTranslatedCorners()
    for i in range(len(tanksTranslatedCorners)):
        if tanksTranslatedCorners[i] != None:
            color = app.game.settings["PLAYER_COLORS"].get(i, "black")
            canvas.create_polygon(tanksTranslatedCorners[i], fill=color)

def drawProjectiles(app, canvas):

    # Get list of tuples, each representing 4 canvas coordinates of circle
    projectilesTranslatedCoordinates = app.game.round.getProjectilesTranslatedCoordinates()
    for i in range(len(projectilesTranslatedCoordinates)):
        canvas.create_oval(projectilesTranslatedCoordinates[i], fill="black")

def drawFPS(app, canvas):

    canvas.create_text(5, 5, text=f"{round(app.fpsMeter.getFPS())}", anchor="nw")

def drawScores(app, canvas):

    xGap = app.game.settings["WINDOW_WIDTH"] // (app.game.settings["NUM_PLAYERS"] + app.game.settings["NUM_AI"] + 1)
    x0 = (app.game.settings["WINDOW_WIDTH"] - (app.game.settings["NUM_PLAYERS"] + app.game.settings["NUM_AI"] - 1) * xGap) // 2
    y = ((app.game.settings["MARGIN"] + app.game.settings["NUM_ROWS"] * app.game.settings["MAPCELL_SIZE"]) + app.game.settings["WINDOW_HEIGHT"]) // 2
    for i in range(app.game.settings["NUM_PLAYERS"] + app.game.settings["NUM_AI"]):
        color = app.game.settings["PLAYER_COLORS"].get(i, "black")
        canvas.create_text(x0 + i * xGap, y, font="Arial 80 bold", fill=color, text=f"{app.game.scores[i]}")
