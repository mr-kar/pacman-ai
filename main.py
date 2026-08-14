import pygame
import sys
from collections import deque

# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()

WIDTH = 900
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man AI - BFS")

clock = pygame.time.Clock()


# =========================================================
# COLORS
# =========================================================

BLACK = (0, 0, 0)
BLUE = (30, 60, 180)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

PATH_COLOR = (0, 200, 255)
VISITED_COLOR = (80, 80, 80)


# =========================================================
# MAZE
# =========================================================

TILE_SIZE = 40

MAZE = [
    "#####################",
    "#                   #",
    "# ### ##### ### ### #",
    "# #               # #",
    "# # ### ##### ### # #",
    "#                   #",
    "### ### ##### ### ###",
    "#                   #",
    "# ### ### # ### ### #",
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
# PAC-MAN
# =========================================================

PACMAN_RADIUS = 12
PACMAN_SPEED = 3

pacman_x = (
    OFFSET_X
    + TILE_SIZE * 1
    + TILE_SIZE // 2
)

pacman_y = (
    OFFSET_Y
    + TILE_SIZE * 1
    + TILE_SIZE // 2
)

# Arah yang sedang digunakan Pac-Man
# None = belum bergerak
current_direction = None

# Arah yang diminta player
requested_direction = None


# =========================================================
# GHOST
# =========================================================

GHOST_RADIUS = 12
GHOST_SPEED = 2

ghost_x = (
    OFFSET_X
    + TILE_SIZE * 19
    + TILE_SIZE // 2
)

ghost_y = (
    OFFSET_Y
    + TILE_SIZE * 13
    + TILE_SIZE // 2
)


# =========================================================
# DIRECTIONS
# =========================================================

DIRECTIONS = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


# =========================================================
# GRAPH
# =========================================================

def is_walkable(row, col):

    if row < 0 or row >= ROWS:
        return False

    if col < 0 or col >= COLS:
        return False

    return MAZE[row][col] != "#"


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

        if is_walkable(new_row, new_col):

            neighbors.append(
                (new_row, new_col)
            )

    return neighbors


def build_graph():

    graph = {}

    for row in range(ROWS):

        for col in range(COLS):

            if is_walkable(row, col):

                node = (row, col)

                graph[node] = get_neighbors(node)

    return graph


GRAPH = build_graph()


# =========================================================
# BFS
# =========================================================

def bfs(start, goal):

    queue = deque([start])

    visited = {start}

    parent = {
        start: None
    }

    while queue:

        current = queue.popleft()

        if current == goal:

            break

        for neighbor in GRAPH[current]:

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    # Tidak ada path
    if goal not in parent:

        return [], visited

    # -----------------------------------------
    # RECONSTRUCT PATH
    # -----------------------------------------

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path, visited


# =========================================================
# GRID <-> PIXEL
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
# PAC-MAN GRID HELPERS
# =========================================================

def get_next_node(row, col, direction):

    dr, dc = DIRECTIONS[direction]

    return (
        row + dr,
        col + dc
    )


def can_move_direction(
    row,
    col,
    direction
):

    if direction is None:

        return False

    next_row, next_col = get_next_node(
        row,
        col,
        direction
    )

    return is_walkable(
        next_row,
        next_col
    )


# =========================================================
# PAC-MAN MOVEMENT
# =========================================================

def update_pacman():

    global pacman_x
    global pacman_y
    global current_direction

    # =====================================================
    # BELUM ADA INPUT
    # =====================================================

    if current_direction is None:

        return

    # =====================================================
    # POSISI GRID
    # =====================================================

    current_row, current_col = pixel_to_grid(
        pacman_x,
        pacman_y
    )

    # =====================================================
    # COBA ARAH BARU
    # =====================================================

    if requested_direction is not None:

        if can_move_direction(
            current_row,
            current_col,
            requested_direction
        ):

            current_direction = requested_direction

    # =====================================================
    # CEK ARAH SAAT INI
    # =====================================================

    if not can_move_direction(
        current_row,
        current_col,
        current_direction
    ):

        # Tidak bisa maju.
        # Pac-Man berhenti di tengah tile,
        # bukan menabrak wall.

        center_x, center_y = grid_to_pixel(
            current_row,
            current_col
        )

        pacman_x += (
            center_x - pacman_x
        ) * 0.35

        pacman_y += (
            center_y - pacman_y
        ) * 0.35

        return

    # =====================================================
    # NODE TUJUAN
    # =====================================================

    next_row, next_col = get_next_node(
        current_row,
        current_col,
        current_direction
    )

    target_x, target_y = grid_to_pixel(
        next_row,
        next_col
    )

    # =====================================================
    # GERAK HORIZONTAL
    # =====================================================

    if current_direction == "LEFT":

        pacman_x -= PACMAN_SPEED

        center_y = grid_to_pixel(
            current_row,
            current_col
        )[1]

        pacman_y += (
            center_y - pacman_y
        ) * 0.35

    elif current_direction == "RIGHT":

        pacman_x += PACMAN_SPEED

        center_y = grid_to_pixel(
            current_row,
            current_col
        )[1]

        pacman_y += (
            center_y - pacman_y
        ) * 0.35

    # =====================================================
    # GERAK VERTIKAL
    # =====================================================

    elif current_direction == "UP":

        pacman_y -= PACMAN_SPEED

        center_x = grid_to_pixel(
            current_row,
            current_col
        )[0]

        pacman_x += (
            center_x - pacman_x
        ) * 0.35

    elif current_direction == "DOWN":

        pacman_y += PACMAN_SPEED

        center_x = grid_to_pixel(
            current_row,
            current_col
        )[0]

        pacman_x += (
            center_x - pacman_x
        ) * 0.35

    # =====================================================
    # SAMPAI NODE BERIKUTNYA
    # =====================================================

    if current_direction in (
        "LEFT",
        "RIGHT"
    ):

        if abs(target_x - pacman_x) <= PACMAN_SPEED:

            pacman_x = target_x

            # Coba belok langsung jika tersedia
            if requested_direction is not None:

                if can_move_direction(
                    next_row,
                    next_col,
                    requested_direction
                ):

                    current_direction = requested_direction

    elif current_direction in (
        "UP",
        "DOWN"
    ):

        if abs(target_y - pacman_y) <= PACMAN_SPEED:

            pacman_y = target_y

            # Coba belok langsung jika tersedia
            if requested_direction is not None:

                if can_move_direction(
                    next_row,
                    next_col,
                    requested_direction
                ):

                    current_direction = requested_direction


# =========================================================
# DRAW MAZE
# =========================================================

def draw_maze():

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


# =========================================================
# DRAW BFS
# =========================================================

def draw_bfs(
    visited,
    path
):

    # -----------------------------------------
    # VISITED NODE
    # -----------------------------------------

    for row, col in visited:

        x, y = grid_to_pixel(
            row,
            col
        )

        pygame.draw.circle(
            screen,
            VISITED_COLOR,
            (x, y),
            3
        )

    # -----------------------------------------
    # BFS PATH
    # -----------------------------------------

    for row, col in path:

        x, y = grid_to_pixel(
            row,
            col
        )

        pygame.draw.circle(
            screen,
            PATH_COLOR,
            (x, y),
            6
        )


# =========================================================
# DRAW PAC-MAN
# =========================================================

def draw_pacman():

    pygame.draw.circle(
        screen,
        YELLOW,
        (
            int(pacman_x),
            int(pacman_y)
        ),
        PACMAN_RADIUS
    )


# =========================================================
# DRAW GHOST
# =========================================================

def draw_ghost():

    pygame.draw.circle(
        screen,
        RED,
        (
            int(ghost_x),
            int(ghost_y)
        ),
        GHOST_RADIUS
    )


# =========================================================
# GHOST AI - BFS
# =========================================================

def move_ghost_using_bfs(path):

    global ghost_x
    global ghost_y

    # Tidak ada path
    if len(path) < 2:

        return

    # =====================================================
    # POSISI GRID GHOST
    # =====================================================

    current_row, current_col = pixel_to_grid(
        ghost_x,
        ghost_y
    )

    current_node = (
        current_row,
        current_col
    )

    # =====================================================
    # CARI NODE GHOST DALAM PATH
    # =====================================================

    try:

        current_index = path.index(
            current_node
        )

    except ValueError:

        return

    # =====================================================
    # SUDAH SAMPAI TUJUAN
    # =====================================================

    if current_index >= len(path) - 1:

        return

    # =====================================================
    # NODE BERIKUTNYA
    # =====================================================

    next_row, next_col = path[
        current_index + 1
    ]

    target_x, target_y = grid_to_pixel(
        next_row,
        next_col
    )

    # =====================================================
    # JARAK
    # =====================================================

    dx = target_x - ghost_x
    dy = target_y - ghost_y

    distance = max(
        abs(dx),
        abs(dy)
    )

    # =====================================================
    # SUDAH SANGAT DEKAT
    # =====================================================

    if distance <= GHOST_SPEED:

        ghost_x = target_x
        ghost_y = target_y

        return

    # =====================================================
    # HORIZONTAL
    # =====================================================

    if next_row == current_row:

        if dx > 0:

            ghost_x += GHOST_SPEED

        elif dx < 0:

            ghost_x -= GHOST_SPEED

        center_y = grid_to_pixel(
            current_row,
            current_col
        )[1]

        ghost_y += (
            center_y - ghost_y
        ) * 0.20

    # =====================================================
    # VERTICAL
    # =====================================================

    elif next_col == current_col:

        if dy > 0:

            ghost_y += GHOST_SPEED

        elif dy < 0:

            ghost_y -= GHOST_SPEED

        center_x = grid_to_pixel(
            current_row,
            current_col
        )[0]

        ghost_x += (
            center_x - ghost_x
        ) * 0.20


# =========================================================
# GAME LOOP
# =========================================================

running = True

while running:

    # =====================================================
    # EVENTS
    # =====================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        # =================================================
        # KEYBOARD
        # =================================================

        elif event.type == pygame.KEYDOWN:

            # ---------------------------------------------
            # UP
            # ---------------------------------------------

            if event.key in (
                pygame.K_UP,
                pygame.K_w
            ):

                requested_direction = "UP"

                if current_direction is None:

                    current_direction = "UP"

            # ---------------------------------------------
            # DOWN
            # ---------------------------------------------

            elif event.key in (
                pygame.K_DOWN,
                pygame.K_s
            ):

                requested_direction = "DOWN"

                if current_direction is None:

                    current_direction = "DOWN"

            # ---------------------------------------------
            # LEFT
            # ---------------------------------------------

            elif event.key in (
                pygame.K_LEFT,
                pygame.K_a
            ):

                requested_direction = "LEFT"

                if current_direction is None:

                    current_direction = "LEFT"

            # ---------------------------------------------
            # RIGHT
            # ---------------------------------------------

            elif event.key in (
                pygame.K_RIGHT,
                pygame.K_d
            ):

                requested_direction = "RIGHT"

                if current_direction is None:

                    current_direction = "RIGHT"

    # =====================================================
    # UPDATE PAC-MAN
    # =====================================================

    update_pacman()

    # =====================================================
    # GET GRID POSITION
    # =====================================================

    ghost_start = pixel_to_grid(
        ghost_x,
        ghost_y
    )

    pacman_goal = pixel_to_grid(
        pacman_x,
        pacman_y
    )

    # =====================================================
    # BFS
    # =====================================================

    bfs_path, bfs_visited = bfs(
        ghost_start,
        pacman_goal
    )

    # =====================================================
    # GHOST AI
    # =====================================================

    move_ghost_using_bfs(
        bfs_path
    )

    # =====================================================
    # DRAW
    # =====================================================

    screen.fill(BLACK)

    draw_maze()

    draw_bfs(
        bfs_visited,
        bfs_path
    )

    draw_pacman()

    draw_ghost()

    pygame.display.flip()

    clock.tick(60)


# =========================================================
# CLEANUP
# =========================================================

pygame.quit()
sys.exit()