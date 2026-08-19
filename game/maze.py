# =========================================================
# MAZE
# =========================================================

from utils.config import (
    WIDTH,
    HEIGHT,
    TILE_SIZE,
    BLUE
)


# =========================================================
# MAZE DATA
# =========================================================

MAZE = [
    "#####################",
    "#                   #",
    "# ### ##### ### ### #",
    "# #               # #",
    "# # ### ##### ### # #",
    "#                   #",
    "### ### ##### ### ###",
    "#                   #",
    "# ### ###   ### ### #",
    "#     #     #       #",
    "##### # ### # ##### #",
    "#       # #         #",
    "# ### # # # # ### # #",
    "#     #     #       #",
    "#####################",
]

ROWS = len(MAZE)
COLS = len(MAZE[0])

MAZE_WIDTH = COLS * TILE_SIZE
MAZE_HEIGHT = ROWS * TILE_SIZE

OFFSET_X = (WIDTH - MAZE_WIDTH) // 2
OFFSET_Y = (HEIGHT - MAZE_HEIGHT) // 2


# =========================================================
# CHECK WALKABLE
# =========================================================

def is_walkable(row, col):

    if row < 0 or row >= ROWS:
        return False

    if col < 0 or col >= COLS:
        return False

    return MAZE[row][col] != "#"


# =========================================================
# GRID NEIGHBORS
# =========================================================

def get_neighbors(node):

    row, col = node

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if is_walkable(
            new_row,
            new_col
        ):

            neighbors.append(
                (new_row, new_col)
            )

    return neighbors


# =========================================================
# GRID -> PIXEL
# =========================================================

def grid_to_pixel(row, col):

    x = (
        OFFSET_X
        + col * TILE_SIZE
        + TILE_SIZE // 2
    )

    y = (
        OFFSET_Y
        + row * TILE_SIZE
        + TILE_SIZE // 2
    )

    return x, y


# =========================================================
# PIXEL -> GRID
# =========================================================

def pixel_to_grid(x, y):

    col = round(
        (
            x
            - OFFSET_X
            - TILE_SIZE / 2
        )
        / TILE_SIZE
    )

    row = round(
        (
            y
            - OFFSET_Y
            - TILE_SIZE / 2
        )
        / TILE_SIZE
    )

    return row, col


# =========================================================
# DRAW MAZE
# =========================================================

def draw_maze(screen):

    for row in range(ROWS):

        for col in range(COLS):

            x = (
                OFFSET_X
                + col * TILE_SIZE
            )

            y = (
                OFFSET_Y
                + row * TILE_SIZE
            )

            if MAZE[row][col] == "#":

                import pygame

                pygame.draw.rect(
                    screen,
                    BLUE,
                    (
                        x,
                        y,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                )