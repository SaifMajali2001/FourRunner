import random

ROWS = 21  # must be odd
COLS = 21  # must be odd

def generate_maze(rows, cols):
    """
    Generate a random solvable maze using recursive backtracking.
    1 = wall, 0 = floor, 2 = exit
    Start is always (1,1), exit is always (rows-2, cols-2).
    """
    # Start fully walled
    maze = [[1] * cols for _ in range(rows)]

    def carve(r, c):
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and maze[nr][nc] == 1:
                maze[r + dr // 2][c + dc // 2] = 0  # carve wall between
                maze[nr][nc] = 0
                carve(nr, nc)

    # Start carving from (1,1)
    maze[1][1] = 0
    carve(1, 1)

    # Place exit
    maze[rows - 2][cols - 2] = 2

    return maze


def get_neighbors(maze, position):
    """Return a list of valid walkable neighboring tile positions (col, row)."""
    col, row = position
    rows = len(maze)
    cols = len(maze[0])
    neighbors = []
    for dc, dr, direction in [(0, -1, "up"), (0, 1, "down"), (-1, 0, "left"), (1, 0, "right")]:
        nc, nr = col + dc, row + dr
        if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != 1:
            neighbors.append((direction, (nc, nr)))
    return neighbors  # list of (direction, position)


def move_player(maze, player_pos, new_position):
    """Move player if new_position is a valid neighbor. Returns new position or old if invalid."""
    valid = [pos for _, pos in get_neighbors(maze, player_pos)]
    if new_position in valid:
        return new_position
    return player_pos


def is_exit(maze, position):
    """Return True if the position is the exit tile."""
    col, row = position
    return maze[row][col] == 2