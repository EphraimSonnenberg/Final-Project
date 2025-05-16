from graphics import *
import random

# Window setup
win = GraphWin("2048 in Zelle Graphics", 450, 450)
win.setBackground("white")

# Grid data
grid = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 4, 0, 0],
    [2, 0, 0, 0]
]

grid_merged = [
    [False] * 4,
    [False] * 4,
    [False] * 4,
    [False] * 4
]

# Colors for tiles
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

# Tile size
cell_size = 100
padding = 5

# Rectangle + Text wrapper
class RectangleText:
    def __init__(self, x, y, size, value):
        self.rect = Rectangle(Point(x, y), Point(x + size, y + size))
        self.text = Text(Point(x + size / 2, y + size / 2), str(value) if value != 0 else "")
        self.text.setSize(18)
        self.text.setStyle("bold")
        self.update(value)

    def update(self, value):
        self.rect.setFill(colors.get(value, "white"))
        self.text.setText("" if value == 0 else str(value))
        if value == 0:
            self.text.setTextColor("white")
        else:
            self.text.setTextColor("blue")

    def draw(self, win):
        self.rect.draw(win)
        self.text.draw(win)

    def undraw(self):
        self.rect.undraw()
        self.text.undraw()

# Draw the entire grid
def draw_grid():
    global grid_drawings
    for cell in grid_drawings:
        cell.undraw()

    grid_drawings = []
    for row in range(4):
        for col in range(4):
            x = padding + col * (cell_size + padding)
            y = padding + row * (cell_size + padding)
            value = grid[row][col]
            cell = RectangleText(x, y, cell_size, value)
            cell.draw(win)
            grid_drawings.append(cell)

def reset_grid_merged():
    global grid_merged
    grid_merged = [[False] * 4 for _ in range(4)]

def add_random():
    empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = random.choice([2, 4])

def up():
    moved = False
    for col in range(4):
        for row in range(1, 4):
            if grid[row][col] != 0:
                curr_row = row
                while curr_row > 0 and grid[curr_row - 1][col] == 0:
                    grid[curr_row - 1][col] = grid[curr_row][col]
                    grid[curr_row][col] = 0
                    curr_row -= 1
                    moved = True
                if curr_row > 0 and grid[curr_row - 1][col] == grid[curr_row][col] and not grid_merged[curr_row - 1][col]:
                    grid[curr_row - 1][col] *= 2
                    grid[curr_row][col] = 0
                    grid_merged[curr_row - 1][col] = True
                    moved = True
    if moved:
        reset_grid_merged()
        add_random()
        draw_grid()

def down():
    moved = False
    for col in range(4):
        for row in range(2, -1, -1):
            if grid[row][col] != 0:
                curr_row = row
                while curr_row < 3 and grid[curr_row + 1][col] == 0:
                    grid[curr_row + 1][col] = grid[curr_row][col]
                    grid[curr_row][col] = 0
                    curr_row += 1
                    moved = True
                if curr_row < 3 and grid[curr_row + 1][col] == grid[curr_row][col] and not grid_merged[curr_row + 1][col]:
                    grid[curr_row + 1][col] *= 2
                    grid[curr_row][col] = 0
                    grid_merged[curr_row + 1][col] = True
                    moved = True
    if moved:
        reset_grid_merged()
        add_random()
        draw_grid()

def key_handler(event):
    key = event.keysym
    if key == "Up":
        up()
    elif key == "Down":
        down()
    elif key == "Left":
        print("Left movement not implemented yet.")
    elif key == "Right":
        print("Right movement not implemented yet.")

# Initialize
grid_drawings = []
draw_grid()

# Bind keys
win.bind_all("<Key>", key_handler)

# Main loop
while True:
    key = win.checkKey()
    if key == "Escape":
        break
