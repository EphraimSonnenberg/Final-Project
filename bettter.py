from graphics import *
from time import sleep
import random

########### Classes ###########
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
        return (self.topLeftX < x < self.topLeftX + self.width) and (self.topLeftY < y < self.topLeftY + self.height)

    def getCanvas(self):
        return self.rectangle.canvas

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

    def undraw(self):
        self.rectangle.undraw()
        self.textBox.undraw()

########### Globals ###########
GRID = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [2, 2, 0, 0]
]
GRID_MERGED = [[False]*4 for _ in range(4)]
grid_drawings = []

pauseButton = RectangleButton(400, 575, 200, 75, "Pause")
unpauseButton = RectangleButton(200, 200, 300, 200, "Unpause")
resetButton = RectangleButton(100, 575, 200, 75, "Reset")

########### Functions ###########
def draw_grid():
    global grid_drawings
    for cell in grid_drawings:
        cell.undraw()
    
    grid_drawings = []
    cell_size = 100
    padding = 10
    for row in range(4):
        for col in range(4):
            x = padding + col * (cell_size + padding)
            y = padding + row * (cell_size + padding)
            value = GRID[row][col]
            tile = RectangleText(x, y, cell_size, cell_size, value)
            tile.draw(win)
            grid_drawings.append(tile)

def update():
    mouse = win.checkMouse()
    key = win.checkKey()

    if mouse:
        if pauseButton.getCanvas() and pauseButton.clickedInside(mouse.getX(), mouse.getY()):
            undrawSetup()
            unpauseButton.draw(win)
        elif unpauseButton.getCanvas() and unpauseButton.clickedInside(mouse.getX(), mouse.getY()):
            initialSetup(win)
            unpauseButton.undraw()
        elif resetButton.getCanvas() and resetButton.clickedInside(mouse.getX(), mouse.getY()):
            resetGRID()
            draw_grid()

    if key in ("w", "Up"):
        up()
    elif key in ("s", "Down"):
        down()

def initialSetup(graphicsWindow):
    pauseButton.draw(graphicsWindow)
    resetButton.draw(graphicsWindow)

def undrawSetup():
    pauseButton.undraw()
    resetButton.undraw()

def resetGRID():
    global GRID
    GRID = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [2, 2, 0, 0]]
    resetGRID_MERGE()

def resetGRID_MERGE():
    global GRID_MERGED
    GRID_MERGED = [[False]*4 for _ in range(4)]

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
        resetGRID_MERGE()
        draw_grid()

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
        resetGRID_MERGE()
        draw_grid()

########### Run the Game ###########
win = GraphWin("2048 (Zelle Graphics)", 700, 700)
initialSetup(win)
draw_grid()

while True:
    update()
    sleep(0.01)
