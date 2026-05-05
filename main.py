import pygame
import sys
from maze import generate_maze, get_neighbors, move_player, is_exit, ROWS, COLS
from render import Render, TILE_SIZE
from word import load_words, assign_words
from Scoreboard import load_scores, save_score

PENALTY_DURATION = 2.0  # seconds blocked after a wrong letter

# --- Screen Setup ---
MAZE_WIDTH    = COLS * TILE_SIZE
MAZE_HEIGHT   = ROWS * TILE_SIZE
HUD_HEIGHT    = 60
SCREEN_WIDTH  = MAZE_WIDTH
SCREEN_HEIGHT = MAZE_HEIGHT + HUD_HEIGHT

def get_direction_positions(maze, player_pos):
    """Return a dict of {direction: (col, row)} for open neighbors."""
    neighbors = get_neighbors(maze, player_pos)
    return {direction: pos for direction, pos in neighbors}

def new_game(word_pool):
    """Set up a fresh game state."""
    maze        = generate_maze(ROWS, COLS)
    player_pos  = (1, 1)
    exit_pos    = (COLS - 2, ROWS - 2)
    dir_positions   = get_direction_positions(maze, player_pos)
    direction_words = assign_words(list(dir_positions.keys()), word_pool)
    return maze, player_pos, exit_pos, dir_positions, direction_words

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Word Runner")
    clock      = pygame.time.Clock()
    font       = pygame.font.SysFont(None, 24)
    word_pool  = load_words()
    renderer   = Render()

    maze, player_pos, exit_pos, dir_positions, direction_words = new_game(word_pool)

    # Typing state
    active_dir = None
    progress   = 0
    wrong      = False
    won        = False
    scores     = load_scores()

    # Timer state
    start_ticks    = pygame.time.get_ticks()
    elapsed        = 0.0

    # Penalty state
    penalty_active    = False
    penalty_end_time  = 0.0   # in seconds from start

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # delta time in seconds

        # Update elapsed time (always keeps going)
        if not won:
            elapsed = (pygame.time.get_ticks() - start_ticks) / 1000.0

        # Update penalty countdown
        if penalty_active and elapsed >= penalty_end_time:
            penalty_active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # Win screen controls
                if won:
                    if event.key == pygame.K_r:
                        maze, player_pos, exit_pos, dir_positions, direction_words = new_game(word_pool)
                        active_dir     = None
                        progress       = 0
                        wrong          = False
                        won            = False
                        penalty_active = False
                        start_ticks    = pygame.time.get_ticks()
                        elapsed        = 0.0
                        scores         = load_scores()
                    elif event.key == pygame.K_q:
                        running = False
                    continue

                # Block input during penalty
                if penalty_active:
                    continue

                # Escape clears current selection
                if event.key == pygame.K_ESCAPE:
                    active_dir = None
                    progress   = 0
                    wrong      = False
                    continue

                if event.unicode.isalpha():
                    char = event.unicode.lower()

                    if active_dir is None:
                        # Check if char matches any word's first letter
                        for direction, word in direction_words.items():
                            if word[0] == char:
                                active_dir = direction
                                progress   = 1
                                wrong      = False
                                break
                        else:
                            # No match — trigger penalty
                            wrong          = True
                            penalty_active = True
                            penalty_end_time = elapsed + PENALTY_DURATION

                    else:
                        word = direction_words[active_dir]
                        if char == word[progress]:
                            progress += 1
                            wrong    = False

                            if progress == len(word):
                                # Word complete — move player
                                new_pos    = dir_positions[active_dir]
                                player_pos = move_player(maze, player_pos, new_pos)

                                if is_exit(maze, player_pos):
                                    won    = True
                                    scores = save_score(elapsed)
                                    active_dir = None
                                    progress   = 0
                                else:
                                    dir_positions   = get_direction_positions(maze, player_pos)
                                    direction_words = assign_words(list(dir_positions.keys()), word_pool)
                                    active_dir = None
                                    progress   = 0
                        else:
                            # Wrong letter — new word + penalty
                            wrong = True
                            direction_words[active_dir] = assign_words(
                                [active_dir], word_pool
                            )[active_dir]
                            progress         = 0
                            active_dir       = None
                            penalty_active   = True
                            penalty_end_time = elapsed + PENALTY_DURATION

        # --- Drawing ---
        screen.fill((0, 0, 0))
        renderer.drawMaze(screen, maze)
        renderer.drawExit(screen, exit_pos)
        renderer.drawWordsOnTiles(screen, maze, player_pos, direction_words, font,
                                  active_dir, progress, wrong)
        renderer.drawPlayer(screen, player_pos)

        penalty_remaining = max(0.0, penalty_end_time - elapsed)
        renderer.drawHUD(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                         active_dir, direction_words, progress, wrong,
                         elapsed, penalty_active, penalty_remaining)

        if won:
            renderer.drawWinScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT, elapsed, scores)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()