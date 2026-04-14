import pygame
import sys
from maze import generate_maze, get_neighbors, move_player, is_exit, ROWS, COLS
from render import Render, TILE_SIZE
from word import load_words, assign_words

# --- Screen Setup ---
MAZE_WIDTH  = COLS * TILE_SIZE
MAZE_HEIGHT = ROWS * TILE_SIZE
HUD_HEIGHT  = 60
SCREEN_WIDTH  = MAZE_WIDTH
SCREEN_HEIGHT = MAZE_HEIGHT + HUD_HEIGHT

def get_direction_positions(maze, player_pos):
    """Return a dict of {direction: (col, row)} for open neighbors."""
    neighbors = get_neighbors(maze, player_pos)
    return {direction: pos for direction, pos in neighbors}

def new_game(word_pool):
    """Set up a fresh game state."""
    maze = generate_maze(ROWS, COLS)
    player_pos = (1, 1)
    exit_pos = (COLS - 2, ROWS - 2)

    dir_positions = get_direction_positions(maze, player_pos)
    direction_words = assign_words(list(dir_positions.keys()), word_pool)

    return maze, player_pos, exit_pos, dir_positions, direction_words

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Word Runner")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    word_pool = load_words()
    renderer = Render()

    maze, player_pos, exit_pos, dir_positions, direction_words = new_game(word_pool)

    # Typing state
    active_dir = None   # direction currently being typed toward
    progress   = 0      # letters correctly typed so far
    wrong      = False  # was the last letter wrong
    won        = False  # has the player reached the exit

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # Win screen controls
                if won:
                    if event.key == pygame.K_r:
                        maze, player_pos, exit_pos, dir_positions, direction_words = new_game(word_pool)
                        active_dir = None
                        progress   = 0
                        wrong      = False
                        won        = False
                    elif event.key == pygame.K_q:
                        running = False
                    continue

                # Escape clears current selection
                if event.key == pygame.K_ESCAPE:
                    active_dir = None
                    progress   = 0
                    wrong      = False
                    continue

                if event.unicode.isalpha():
                    char = event.unicode.lower()

                    # If no active direction, check if char matches any word's first letter
                    if active_dir is None:
                        for direction, word in direction_words.items():
                            if word[0] == char:
                                active_dir = direction
                                progress   = 1      # first letter already matched
                                wrong      = False
                                break
                        else:
                            # No match - flash wrong on all
                            wrong = True

                    else:
                        # Already typing a word - check next letter
                        word = direction_words[active_dir]
                        if char == word[progress]:
                            progress += 1
                            wrong = False

                            # Check if word is complete
                            if progress == len(word):
                                # Move player one tile in active_dir
                                new_pos = dir_positions[active_dir]
                                player_pos = move_player(maze, player_pos, new_pos)

                                # Check for win
                                if is_exit(maze, player_pos):
                                    won = True
                                    active_dir = None
                                    progress   = 0
                                else:
                                    # Recalculate neighbors and assign new words
                                    dir_positions    = get_direction_positions(maze, player_pos)
                                    direction_words  = assign_words(list(dir_positions.keys()), word_pool)
                                    active_dir = None
                                    progress   = 0
                        else:
                            # Wrong letter - reset this word to a new one, reset progress
                            wrong = True
                            direction_words[active_dir] = assign_words(
                                [active_dir],
                                [w for w in word_pool if w[0] != direction_words[active_dir][0] or True]
                            )[active_dir]
                            progress = 0

        # --- Drawing ---
        screen.fill((0, 0, 0))
        renderer.drawMaze(screen, maze)
        renderer.drawExit(screen, exit_pos)
        renderer.drawWordsOnTiles(screen, maze, player_pos, direction_words, font,
                                  active_dir, progress, wrong)
        renderer.drawPlayer(screen, player_pos)
        renderer.drawHUD(screen, SCREEN_WIDTH, SCREEN_HEIGHT, active_dir, direction_words, progress, wrong)

        if won:
            renderer.drawWinScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()