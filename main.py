from graphics import *
from time import sleep
import random

###########
# Classes #
###########
class RectangleButton():
    def __init__(self, topLeftX, topLeftY, width, height, text):
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.width = width
        self.height = height
        self.text = text
        self.rectangle = Rectangle(Point(topLeftX, topLeftY), Point(topLeftX + width, topLeftY + height))
        self.textBox = Text(Point(topLeftX + width / 2, topLeftY + height / 2), text)

    def draw(self, graphicsWindow):
        self.rectangle.draw(graphicsWindow)
        self.textBox.draw(graphicsWindow)

    def clickedInside(self, x, y):
        if(
            x > self.topLeftX and
            x < self.topLeftX + self.width and
            y > self.topLeftY and
            y < self.topLeftY + self.height
        ):
            return True
        else:
            return False

    def getCanvas(self):
        return self.rectangle.canvas
    
    def setText(self, text):
        self.setText(text)

    def undraw(self):
        self.rectangle.undraw()
        self.textBox.undraw()

class RectangleText():
    def __init__(self, topLeftX, topLeftY, width, height, value):
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.width = width
        self.height = height
        self.rectangle = Rectangle(Point(topLeftX, topLeftY), Point(topLeftX + width, topLeftY + height))
        self.textBox = Text(Point(topLeftX + width / 2, topLeftY + height / 2), str(value) if value != 0 else "")
        self.textBox.setSize(18)
        self.textBox.setStyle("bold")
        self.color_by_value(value)

    def draw(self, graphicsWindow):
        self.rectangle.draw(graphicsWindow)
        self.textBox.draw(graphicsWindow)

    def text(self, text):
        self.textBox.setText(text)

    def color_by_value(self, value):
        colors = {
            0: "white",
            2: "yellow",
            4: "orange",
            8: "pink",
            16: "red",
            32: "light green",
            64: "green",
            128: "light blue",
            256: "blue",
            512: "purple",
            1024: "gold",
            2048: "black"
        }
        self.rectangle.setFill(colors.get(value, "gray"))

    def getCanvas(self):
        return self.rectangle.canvas

    def undraw(self):
        self.rectangle.undraw()
        self.textBox.undraw()

####################
# Global variables #
####################
GRID = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 2, 0, 0]
]
GRID_MERGED = [
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False],
    [False, False, False, False]
]
tileBadText = [256, 512]
grid_drawings = []

pauseButton = RectangleButton(400, 575, 200, 75, "Pause")
unpauseButton = RectangleButton(200, 200, 300, 200, "Unpause")
resetButton = RectangleButton(100, 575, 200, 75, "Reset")
backgroundRec = Rectangle(Point(-1, -1), Point(701, 701))
gameOverOverlay = RectangleButton(100, 25, 500, 600, "Game Over")
gameOverOverlay.rectangle.setFill("grey")
howToPlayButton = RectangleButton(535, 100, 150, 100, "How To Play")
howToPlayOverlay = [
    Text(Point(350, 50), "How To Play"),
    Text(Point(350, 250), "Use the arrow keys or WASD to move the tiles.")
]
howToPlayOverlayButton = RectangleButton(250, 500, 200, 100, "Back")

paused = False

##################
# Helper methods #
##################
def draw_grid():
    global grid_drawings
    for cell in grid_drawings:
        cell.undraw()
    
    grid_drawings = []
    cell_size = 120
    padding = 10
    for row in range(4):
        for col in range(4):
            x = padding + col * (cell_size + padding)
            y = padding + row * (cell_size + padding)
            value = GRID[row][col]
            tile = RectangleText(x, y, cell_size, cell_size, value)
            tile.draw(win)
            grid_drawings.append(tile)
            if value in (64, 256, 512, 2048):
                tile.textBox.setTextColor("white")

def undraw_grid(graphicsWindow):
    backgroundRec.draw(graphicsWindow)
    backgroundRec.setFill(color_rgb(240, 240, 240))

def add_random():
    added = False
    while not added:
        x = random.randint(0, 3)
        y = random.randint(0, 3)

        value = random.choice([2, 4])

        if GRID[y][x] == 0:
            GRID[y][x] = value
            added = True

def update():
    global paused
    mouse = win.checkMouse()
    keyboard = win.checkKey()

    if mouse:
        if not paused:
            if pauseButton.getCanvas() and pauseButton.clickedInside(mouse.getX(), mouse.getY()):
                pause_game()
            elif resetButton.getCanvas() and resetButton.clickedInside(mouse.getX(), mouse.getY()):
                resetGRID()
                resetGRID_MERGED()
            elif gameOverOverlay.getCanvas() and gameOverOverlay.clickedInside(mouse.getX(), mouse.getY()):
                gameOverOverlay.undraw()
                resetGameOver()
            elif howToPlayButton.getCanvas() and howToPlayButton.clickedInside(mouse.getX(), mouse.getY()):
                howToPlayButton.undraw()
                pause_game_()
                for item in howToPlayOverlay:
                    item.draw(win)
                howToPlayOverlay[0].setSize(36)
                howToPlayOverlay[1].setSize(18)
                howToPlayOverlayButton.draw(win)
        else:
            if unpauseButton.getCanvas() and unpauseButton.clickedInside(mouse.getX(), mouse.getY()):
                unpause_game()
            elif howToPlayOverlayButton.getCanvas() and howToPlayOverlayButton.clickedInside(mouse.getX(), mouse.getY()):
                unpause_game_()
                howToPlayOverlayButton.undraw()
                for item in howToPlayOverlay:
                    item.undraw()

    if not paused:
        if keyboard == "w":
            up()
        elif keyboard == "Up":
            up()
        elif keyboard == "a":
            left()   
        elif keyboard == "Left":
            left()
        elif keyboard == "s":
            down()
        elif keyboard == "Down":
            down()
        elif keyboard == "d":
            right()
        elif keyboard == "Right":
            right()
        sleep(.3)

        if game_over(GRID):
            pass

def initialSetup(graphicsWindow):
    pauseButton.draw(graphicsWindow)
    resetButton.draw(graphicsWindow)
    howToPlayButton.draw(graphicsWindow)

def undrawSetup():
    pauseButton.undraw()
    resetButton.undraw()
    backgroundRec.undraw()
    howToPlayButton.undraw()

def resetGRID():
    global GRID
    GRID = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [2, 2, 0, 0]
    ]
    resetGRID_MERGED()
    draw_grid()

def resetGRID_MERGED():
    global GRID_MERGED
    GRID_MERGED = [
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False],
        [False, False, False, False]
    ]

def resetGameOver():
    global GRID
    GRID = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [2, 2, 0, 0]
    ]
    resetGRID_MERGED()
    draw_grid()
    initialSetup(win)

def pause_game():
    global paused
    paused = True
    undrawSetup()
    backgroundRec.draw(win)
    backgroundRec.setFill(color_rgb(240, 240, 240))
    unpauseButton.draw(win)

def pause_game_():
    global paused
    paused = True
    undrawSetup()
    backgroundRec.draw(win)
    backgroundRec.setFill(color_rgb(240, 240, 240))

def unpause_game():
    global paused
    paused = False
    unpauseButton.undraw()
    initialSetup(win)
    draw_grid()

def unpause_game_():
    global paused
    paused = False
    initialSetup(win)
    draw_grid()

def gameOverCountdown():
    gameOverCountdown = Text(Point(350, 300), "")
    gameOverCountdown.draw(win)
    for i in range(5, -1, -1):
        gameOverCountdown.setText(str(i))
        gameOverCountdown.undraw()
        gameOverCountdown.draw(win)
        time.sleep(1)

def up():
    moved = False
    for col in range(4):
        for row in range(1, 4):
            if GRID[row][col] != 0:
                curr_row = row
                while curr_row > 0 and GRID[curr_row - 1][col] == 0:
                    GRID[curr_row - 1][col] = GRID[curr_row][col]
                    GRID[curr_row][col] = 0
                    curr_row -= 1
                    moved = True
                if curr_row > 0 and GRID[curr_row - 1][col] == GRID[curr_row][col] and not GRID_MERGED[curr_row - 1][col]:
                    GRID[curr_row - 1][col] *= 2
                    GRID[curr_row][col] = 0
                    GRID_MERGED[curr_row - 1][col] = True
                    moved = True
    if moved:
        resetGRID_MERGED()
        add_random()
        draw_grid()
    return moved

def down():
    moved = False
    for col in range(4):
        for row in range(2, -1, -1):
            if GRID[row][col] != 0:
                curr_row = row
                while curr_row < 3 and GRID[curr_row + 1][col] == 0:
                    GRID[curr_row + 1][col] = GRID[curr_row][col]
                    GRID[curr_row][col] = 0
                    curr_row += 1
                    moved = True
                if curr_row < 3 and GRID[curr_row + 1][col] == GRID[curr_row][col] and not GRID_MERGED[curr_row + 1][col]:
                    GRID[curr_row + 1][col] *= 2
                    GRID[curr_row][col] = 0
                    GRID_MERGED[curr_row + 1][col] = True
                    moved = True
    if moved:
        resetGRID_MERGED()
        add_random()
        draw_grid()
    return moved

def left():
    moved = False
    for row in range(4):
        for col in range(1, 4):
            if GRID[row][col] != 0:
                curr_col = col
                while curr_col > 0 and GRID[row][curr_col - 1] == 0:
                    GRID[row][curr_col - 1] = GRID[row][curr_col]
                    GRID[row][curr_col] = 0
                    curr_col -= 1
                    moved = True
                if curr_col > 0 and GRID[row][curr_col - 1] == GRID[row][curr_col] and not GRID_MERGED[row][curr_col - 1]:
                    GRID[row][curr_col - 1] *= 2
                    GRID[row][curr_col] = 0
                    GRID_MERGED[row][curr_col - 1] = True
                    moved = True
    if moved:
        resetGRID_MERGED()
        add_random()
        draw_grid()
    return moved

def right():
    moved = False
    for row in range(4):
        for col in range(2, -1, -1):
            if GRID[row][col] != 0:
                curr_col = col
                while curr_col < 3 and GRID[row][curr_col + 1] == 0:
                    GRID[row][curr_col + 1] = GRID[row][curr_col]
                    GRID[row][curr_col] = 0
                    curr_col += 1
                    moved = True
                if curr_col < 3 and GRID[row][curr_col + 1] == GRID[row][curr_col] and not GRID_MERGED[row][curr_col + 1]:
                    GRID[row][curr_col + 1] *= 2
                    GRID[row][curr_col] = 0
                    GRID_MERGED[row][curr_col + 1] = True
                    moved = True
    if moved:
        resetGRID_MERGED()
        add_random()
        draw_grid()
    return moved

def has_moves(GRID):
    size = len(GRID)
    for i in range(size):
        for j in range(size):
            if GRID[i][j] == 0:
                return True  # Empty space available
            if i < size - 1 and GRID[i][j] == GRID[i+1][j]:
                return True  # Can merge vertically
            if j < size - 1 and GRID[i][j] == GRID[i][j+1]:
                return True  # Can merge horizontally
    return False

def game_over(GRID):
    if not has_moves(GRID):
        if gameOverOverlay.getCanvas() == None:
            undrawSetup()
            undraw_grid(win)
            gameOverOverlay.draw(win)
            gameOverCountdown()
            gameOverOverlay.textBox.setText("Click Me To Restart")
            gameOverOverlay.undraw()
            gameOverOverlay.draw(win)
            print("Game Over! No more moves available.")
        return True
    return False

###################
# Executable code #
###################
win = GraphWin("2048 (not for resale)", 700, 700)

initialSetup(win)
draw_grid()

while True:
    update()
