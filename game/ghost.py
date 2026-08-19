# =========================================================
# GHOST
# =========================================================

import pygame

from utils.config import (
    TILE_SIZE,
    RED,
    GHOST_RADIUS,
    GHOST_SPEED
)

from game.maze import (
    OFFSET_X,
    OFFSET_Y,
    grid_to_pixel,
    pixel_to_grid
)


# =========================================================
# GHOST CLASS
# =========================================================

class Ghost:

    def __init__(self):

        # -------------------------------------------------
        # Starting position
        # -------------------------------------------------

        self.x = (
            OFFSET_X
            + TILE_SIZE * 19
            + TILE_SIZE // 2
        )

        self.y = (
            OFFSET_Y
            + TILE_SIZE * 13
            + TILE_SIZE // 2
        )

        # -------------------------------------------------
        # AI PATH
        # -------------------------------------------------

        self.path = []

        # Index node yang sedang dituju
        #
        # path[0] = posisi awal Ghost
        # path[1] = tujuan pertama
        # path[2] = tujuan kedua
        # dst.

        self.path_index = 1

        # -------------------------------------------------
        # Posisi Pac-Man ketika path dibuat
        # -------------------------------------------------

        self.last_goal = None


    # =====================================================
    # GET GRID POSITION
    # =====================================================

    def get_grid_position(self):

        return pixel_to_grid(
            self.x,
            self.y
        )


    # =====================================================
    # SET NEW PATH
    # =====================================================

    def set_path(
        self,
        path,
        goal
    ):

        # Simpan path hasil BFS / DFS

        self.path = list(path)

        # Ghost selalu mulai mengikuti
        # node kedua dalam path

        self.path_index = 1

        # Simpan posisi Pac-Man saat
        # pencarian dilakukan

        self.last_goal = goal


    # =====================================================
    # CHECK WHETHER NEW SEARCH IS NEEDED
    # =====================================================

    def needs_new_path(
        self,
        pacman_goal,
        threshold=3
    ):

        # -------------------------------------------------
        # Belum punya path
        # -------------------------------------------------

        if len(self.path) < 2:

            return True


        # -------------------------------------------------
        # Path sudah selesai
        # -------------------------------------------------

        if self.path_index >= len(self.path):

            return True


        # -------------------------------------------------
        # Belum pernah menyimpan goal
        # -------------------------------------------------

        if self.last_goal is None:

            return True


        # -------------------------------------------------
        # Hitung perubahan posisi Pac-Man
        # -------------------------------------------------

        old_row, old_col = self.last_goal

        new_row, new_col = pacman_goal

        distance = (
            abs(new_row - old_row)
            +
            abs(new_col - old_col)
        )


        # -------------------------------------------------
        # Kalau Pac-Man sudah berpindah cukup jauh,
        # cari path baru.
        # -------------------------------------------------

        if distance >= threshold:

            return True


        return False


    # =====================================================
    # MOVE ALONG CURRENT PATH
    # =====================================================

    def update(self):

        # -------------------------------------------------
        # Tidak ada path
        # -------------------------------------------------

        if len(self.path) < 2:

            return


        # -------------------------------------------------
        # Path sudah selesai
        # -------------------------------------------------

        if self.path_index >= len(self.path):

            return


        # -------------------------------------------------
        # Posisi Ghost sekarang
        # -------------------------------------------------

        current_row, current_col = (
            self.get_grid_position()
        )


        # -------------------------------------------------
        # Target berikutnya
        # -------------------------------------------------

        target_row, target_col = self.path[
            self.path_index
        ]


        target_x, target_y = grid_to_pixel(
            target_row,
            target_col
        )


        # =================================================
        # HORIZONTAL
        # =================================================

        if target_row == current_row:

            # ---------------------------------------------
            # Bergerak kanan
            # ---------------------------------------------

            if target_x > self.x:

                self.x += GHOST_SPEED

            # ---------------------------------------------
            # Bergerak kiri
            # ---------------------------------------------

            elif target_x < self.x:

                self.x -= GHOST_SPEED


            # ---------------------------------------------
            # Tetap tepat di tengah lorong
            # ---------------------------------------------

            self.y += (
                target_y - self.y
            ) * 0.25


        # =================================================
        # VERTICAL
        # =================================================

        elif target_col == current_col:

            # ---------------------------------------------
            # Bergerak ke bawah
            # ---------------------------------------------

            if target_y > self.y:

                self.y += GHOST_SPEED

            # ---------------------------------------------
            # Bergerak ke atas
            # ---------------------------------------------

            elif target_y < self.y:

                self.y -= GHOST_SPEED


            # ---------------------------------------------
            # Tetap tepat di tengah lorong
            # ---------------------------------------------

            self.x += (
                target_x - self.x
            ) * 0.25


        # =================================================
        # CHECK REACHED TARGET
        # =================================================

        if (
            abs(target_x - self.x) <= GHOST_SPEED
            and
            abs(target_y - self.y) <= GHOST_SPEED
        ):

            # Snap tepat ke tengah tile

            self.x = target_x
            self.y = target_y

            # Lanjut ke node berikutnya

            self.path_index += 1


    # =====================================================
    # DRAW
    # =====================================================

    def draw(self, screen):

        pygame.draw.circle(
            screen,
            RED,
            (
                int(self.x),
                int(self.y)
            ),
            GHOST_RADIUS
        )