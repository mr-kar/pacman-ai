# =========================================================
# PAC-MAN
# =========================================================

import pygame

from utils.config import (
    TILE_SIZE,
    YELLOW,
    PACMAN_RADIUS,
    PACMAN_SPEED
)

from game.maze import (
    OFFSET_X,
    OFFSET_Y,
    grid_to_pixel,
    pixel_to_grid,
    is_walkable
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
# PAC-MAN CLASS
# =========================================================

class Pacman:

    def __init__(self):

        self.x = (
            OFFSET_X
            + TILE_SIZE * 1
            + TILE_SIZE // 2
        )

        self.y = (
            OFFSET_Y
            + TILE_SIZE * 1
            + TILE_SIZE // 2
        )

        # Belum bergerak
        self.current_direction = None

        # Input user
        self.requested_direction = None


    # =====================================================
    # NEXT NODE
    # =====================================================

    def get_next_node(
        self,
        row,
        col,
        direction
    ):

        dr, dc = DIRECTIONS[
            direction
        ]

        return (
            row + dr,
            col + dc
        )


    # =====================================================
    # CAN MOVE
    # =====================================================

    def can_move_direction(
        self,
        row,
        col,
        direction
    ):

        if direction is None:

            return False

        next_row, next_col = self.get_next_node(
            row,
            col,
            direction
        )

        return is_walkable(
            next_row,
            next_col
        )


    # =====================================================
    # HANDLE INPUT
    # =====================================================

    def handle_input(self, event):

        if event.type != pygame.KEYDOWN:

            return

        if event.key in (
            pygame.K_UP,
            pygame.K_w
        ):

            self.requested_direction = "UP"

            if self.current_direction is None:

                self.current_direction = "UP"

        elif event.key in (
            pygame.K_DOWN,
            pygame.K_s
        ):

            self.requested_direction = "DOWN"

            if self.current_direction is None:

                self.current_direction = "DOWN"

        elif event.key in (
            pygame.K_LEFT,
            pygame.K_a
        ):

            self.requested_direction = "LEFT"

            if self.current_direction is None:

                self.current_direction = "LEFT"

        elif event.key in (
            pygame.K_RIGHT,
            pygame.K_d
        ):

            self.requested_direction = "RIGHT"

            if self.current_direction is None:

                self.current_direction = "RIGHT"


    # =====================================================
    # UPDATE
    # =====================================================

    def update(self):

        # ---------------------------------------------
        # BELUM ADA INPUT
        # ---------------------------------------------

        if self.current_direction is None:

            return

        # ---------------------------------------------
        # CURRENT GRID
        # ---------------------------------------------

        current_row, current_col = pixel_to_grid(
            self.x,
            self.y
        )

        # ---------------------------------------------
        # COBA ARAH BARU
        # ---------------------------------------------

        if self.requested_direction is not None:

            if self.can_move_direction(
                current_row,
                current_col,
                self.requested_direction
            ):

                self.current_direction = (
                    self.requested_direction
                )

        # ---------------------------------------------
        # CURRENT DIRECTION BLOCKED
        # ---------------------------------------------

        if not self.can_move_direction(
            current_row,
            current_col,
            self.current_direction
        ):

            center_x, center_y = grid_to_pixel(
                current_row,
                current_col
            )

            self.x += (
                center_x - self.x
            ) * 0.35

            self.y += (
                center_y - self.y
            ) * 0.35

            return

        # ---------------------------------------------
        # NEXT NODE
        # ---------------------------------------------

        next_row, next_col = self.get_next_node(
            current_row,
            current_col,
            self.current_direction
        )

        target_x, target_y = grid_to_pixel(
            next_row,
            next_col
        )

        # ---------------------------------------------
        # HORIZONTAL
        # ---------------------------------------------

        if self.current_direction == "LEFT":

            self.x -= PACMAN_SPEED

            center_y = grid_to_pixel(
                current_row,
                current_col
            )[1]

            self.y += (
                center_y - self.y
            ) * 0.35

        elif self.current_direction == "RIGHT":

            self.x += PACMAN_SPEED

            center_y = grid_to_pixel(
                current_row,
                current_col
            )[1]

            self.y += (
                center_y - self.y
            ) * 0.35

        # ---------------------------------------------
        # VERTICAL
        # ---------------------------------------------

        elif self.current_direction == "UP":

            self.y -= PACMAN_SPEED

            center_x = grid_to_pixel(
                current_row,
                current_col
            )[0]

            self.x += (
                center_x - self.x
            ) * 0.35

        elif self.current_direction == "DOWN":

            self.y += PACMAN_SPEED

            center_x = grid_to_pixel(
                current_row,
                current_col
            )[0]

            self.x += (
                center_x - self.x
            ) * 0.35

        # ---------------------------------------------
        # REACH NODE
        # ---------------------------------------------

        if self.current_direction in (
            "LEFT",
            "RIGHT"
        ):

            if abs(
                target_x - self.x
            ) <= PACMAN_SPEED:

                self.x = target_x

                if self.requested_direction is not None:

                    if self.can_move_direction(
                        next_row,
                        next_col,
                        self.requested_direction
                    ):

                        self.current_direction = (
                            self.requested_direction
                        )

        elif self.current_direction in (
            "UP",
            "DOWN"
        ):

            if abs(
                target_y - self.y
            ) <= PACMAN_SPEED:

                self.y = target_y

                if self.requested_direction is not None:

                    if self.can_move_direction(
                        next_row,
                        next_col,
                        self.requested_direction
                    ):

                        self.current_direction = (
                            self.requested_direction
                        )


    # =====================================================
    # GET GRID POSITION
    # =====================================================

    def get_grid_position(self):

        return pixel_to_grid(
            self.x,
            self.y
        )


    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            YELLOW,
            (
                int(self.x),
                int(self.y)
            ),
            PACMAN_RADIUS
        )