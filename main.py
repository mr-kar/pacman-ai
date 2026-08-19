# =========================================================
# PAC-MAN AI
# MAIN PROGRAM
# =========================================================

import pygame
import sys

from utils.config import (
    WIDTH,
    HEIGHT,
    BLACK,
    PATH_COLOR,
    VISITED_COLOR
)

from game.maze import (
    ROWS,
    COLS,
    get_neighbors,
    is_walkable,
    grid_to_pixel,
    draw_maze
)

from game.pacman import Pacman
from game.ghost import Ghost

from ai.bfs import (
    build_graph,
    bfs
)

from ai.dfs import (
    dfs
)


# =========================================================
# INITIALIZATION
# =========================================================

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Pac-Man AI - BFS vs DFS"
)

clock = pygame.time.Clock()


# =========================================================
# FONT
# =========================================================

font = pygame.font.Font(
    None,
    26
)


# =========================================================
# CREATE OBJECTS
# =========================================================

pacman = Pacman()

ghost = Ghost()


# =========================================================
# BUILD GRAPH
# =========================================================

graph = build_graph(
    ROWS,
    COLS,
    is_walkable,
    get_neighbors
)


# =========================================================
# AI ALGORITHM
# =========================================================

current_algorithm = "BFS"


# =========================================================
# SEARCH RESULT
# =========================================================

search_path = []

search_visited = set()


# =========================================================
# RUN SEARCH
# =========================================================

def run_search():

    global search_path
    global search_visited

    # ---------------------------------------------
    # Posisi Ghost
    # ---------------------------------------------

    ghost_start = (
        ghost.get_grid_position()
    )

    # ---------------------------------------------
    # Posisi Pac-Man
    # ---------------------------------------------

    pacman_goal = (
        pacman.get_grid_position()
    )


    # =================================================
    # BFS
    # =================================================

    if current_algorithm == "BFS":

        search_path, search_visited = bfs(
            graph,
            ghost_start,
            pacman_goal
        )


    # =================================================
    # DFS
    # =================================================

    elif current_algorithm == "DFS":

        search_path, search_visited = dfs(
            graph,
            ghost_start,
            pacman_goal
        )


    # =================================================
    # BERIKAN PATH KE GHOST
    # =================================================

    ghost.set_path(
        search_path,
        pacman_goal
    )


# =========================================================
# DRAW SEARCH VISUALIZATION
# =========================================================

def draw_search(
    visited,
    path
):

    # -----------------------------------------------------
    # VISITED NODES
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # PATH
    # -----------------------------------------------------

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
# DRAW INFORMATION
# =========================================================

def draw_information():

    # -----------------------------------------------------
    # ALGORITHM
    # -----------------------------------------------------

    algorithm_text = font.render(
        f"Algorithm: {current_algorithm}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        algorithm_text,
        (20, 10)
    )


    # -----------------------------------------------------
    # VISITED
    # -----------------------------------------------------

    visited_text = font.render(
        f"Visited: {len(search_visited)}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        visited_text,
        (280, 10)
    )


    # -----------------------------------------------------
    # PATH LENGTH
    # -----------------------------------------------------

    path_length = max(
        len(search_path) - 1,
        0
    )

    path_text = font.render(
        f"Path: {path_length} steps",
        True,
        (255, 255, 255)
    )

    screen.blit(
        path_text,
        (500, 10)
    )


    # -----------------------------------------------------
    # CONTROLS
    # -----------------------------------------------------

    control_text = font.render(
        "B = BFS    D = DFS",
        True,
        (255, 255, 255)
    )

    screen.blit(
        control_text,
        (760, 10)
    )


# =========================================================
# FIRST SEARCH
# =========================================================

run_search()


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
            # BFS
            # ---------------------------------------------

            if event.key == pygame.K_b:

                current_algorithm = "BFS"

                # Cari path baru menggunakan BFS

                run_search()


            # ---------------------------------------------
            # DFS
            # ---------------------------------------------

            elif event.key == pygame.K_d:

                current_algorithm = "DFS"

                # Cari path baru menggunakan DFS

                run_search()


        # =================================================
        # PAC-MAN INPUT
        # =================================================

        pacman.handle_input(
            event
        )


    # =====================================================
    # UPDATE PAC-MAN
    # =====================================================

    pacman.update()


    # =====================================================
    # CHECK WHETHER SEARCH IS NEEDED
    # =====================================================

    pacman_goal = (
        pacman.get_grid_position()
    )


    if ghost.needs_new_path(
        pacman_goal,
        threshold=3
    ):

        run_search()


    # =====================================================
    # MOVE GHOST
    # =====================================================

    ghost.update()


    # =====================================================
    # DRAW
    # =====================================================

    screen.fill(
        BLACK
    )


    # Maze

    draw_maze(
        screen
    )


    # AI visualization

    draw_search(
        search_visited,
        search_path
    )


    # Pac-Man

    pacman.draw(
        screen
    )


    # Ghost

    ghost.draw(
        screen
    )


    # Information

    draw_information()


    # =====================================================
    # DISPLAY
    # =====================================================

    pygame.display.flip()

    clock.tick(60)


# =========================================================
# CLEANUP
# =========================================================

pygame.quit()

sys.exit()