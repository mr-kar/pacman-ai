# =========================================================
# BFS AI
# =========================================================

from collections import deque


# =========================================================
# BUILD GRAPH
# =========================================================

def build_graph(
    rows,
    cols,
    is_walkable,
    get_neighbors
):

    graph = {}

    for row in range(rows):

        for col in range(cols):

            if is_walkable(
                row,
                col
            ):

                node = (
                    row,
                    col
                )

                graph[node] = get_neighbors(
                    node
                )

    return graph


# =========================================================
# BFS
# =========================================================

def bfs(
    graph,
    start,
    goal
):

    queue = deque([start])

    visited = {start}

    parent = {
        start: None
    }

    while queue:

        current = queue.popleft()

        if current == goal:

            break

        for neighbor in graph.get(
            current,
            []
        ):

            if neighbor not in visited:

                visited.add(neighbor)

                parent[neighbor] = current

                queue.append(neighbor)

    # =====================================================
    # NO PATH
    # =====================================================

    if goal not in parent:

        return [], visited

    # =====================================================
    # RECONSTRUCT PATH
    # =====================================================

    path = []

    current = goal

    while current is not None:

        path.append(current)

        current = parent[current]

    path.reverse()

    return path, visited