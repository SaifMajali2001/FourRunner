import pygame
 
def get_neighbors(position):
    """Return a list of valid walkable neighboring tiles."""
    col, row = position
    neighbors = []
    for dc, dr in [(0,-1), (0,1), (-1,0), (1,0)]:  # up, down, left, right
        nc, nr = col + dc, row + dr
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE[nr][nc] != 1:
            neighbors.append((nc, nr))
    return neighbors
 
 
def move_player(new_position):
    """Move player if new_position is a valid neighbor. Returns True if successful."""
    global player_pos
    if new_position in get_neighbors(player_pos):
        player_pos = new_position
        return True
    return False
 
 
def is_exit(position):
    """Return True if the position is the exit tile."""
    col, row = position
    return MAZE[row][col] == 2
 