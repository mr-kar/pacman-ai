# =========================================================
# DFS AI
# Depth First Search
# =========================================================


# =========================================================
# DFS
# =========================================================

def dfs(
    graph,
    start,
    goal
):

    # -----------------------------------------------------
    # STACK
    # -----------------------------------------------------

    stack = [start]

    # -----------------------------------------------------
    # VISITED
    # -----------------------------------------------------

    visited = set()

    # -----------------------------------------------------
    # PARENT
    # Digunakan untuk membangun path
    # -----------------------------------------------------

    parent = {
        start: None
    }

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    while stack:

        # DFS mengambil node paling atas dari stack
        current = stack.pop()

        # -------------------------------------------------
        # Jika sudah pernah dikunjungi
        # -------------------------------------------------

        if current in visited:

            continue

        # Tandai sebagai visited
        visited.add(current)

        # -------------------------------------------------
        # Goal ditemukan
        # -------------------------------------------------

        if current == goal:

            break

        # -------------------------------------------------
        # Masukkan neighbor ke stack
        # -------------------------------------------------

        neighbors = graph.get(
            current,
            []
        )

        for neighbor in neighbors:

            if neighbor not in visited:

                if neighbor not in parent:

                    parent[neighbor] = current

                    stack.append(
                        neighbor
                    )

    # =====================================================
    # TIDAK ADA PATH
    # =====================================================

    if goal not in parent:

        return [], visited

    # =====================================================
    # RECONSTRUCT PATH
    # =====================================================

    path = []

    current = goal

    while current is not None:

        path.append(
            current
        )

        current = parent[current]

    # Karena kita mulai dari goal,
    # balik menjadi start -> goal

    path.reverse()

    return path, visited