import pygame

TILE_SIZE = 34  # sized to fit on 1080p screen

class Render:

    def __init__(self):
        self.assets = {
            "verticalWall":   pygame.image.load("assets/verticalWall2.png"),
            "horizontalWall": pygame.image.load("assets/horizontalWall2.png"),
            "floor":          pygame.image.load("assets/floor.png"),
            "player":         pygame.image.load("assets/player2.png"),
            "exit":           pygame.image.load("assets/exit.png")
        }
        # Scale all assets to new tile size
        for key in self.assets:
            self.assets[key] = pygame.transform.scale(self.assets[key], (TILE_SIZE, TILE_SIZE))

    def drawMaze(self, screen, maze):
        rows = len(maze)
        cols = len(maze[0])

        for row in range(rows):
            for col in range(cols):
                tile = maze[row][col]
                x = col * TILE_SIZE
                y = row * TILE_SIZE

                if tile == 0 or tile == 2:
                    screen.blit(self.assets["floor"], (x, y))
                    continue

                up    = row > 0        and maze[row - 1][col] == 1
                down  = row < rows - 1 and maze[row + 1][col] == 1
                left  = col > 0        and maze[row][col - 1] == 1
                right = col < cols - 1 and maze[row][col + 1] == 1

                if left or right:
                    screen.blit(self.assets["horizontalWall"], (x, y))
                elif up or down:
                    screen.blit(self.assets["verticalWall"], (x, y))
                else:
                    screen.blit(self.assets["horizontalWall"], (x, y))

    def drawPlayer(self, screen, playerPOS):
        col, row = playerPOS
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        screen.blit(self.assets["player"], (x, y))

    def drawExit(self, screen, exitPOS):
        col, row = exitPOS
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        screen.blit(self.assets["exit"], (x, y))

    def drawWordsOnTiles(self, screen, maze, player_pos, direction_words, font, active_dir=None, progress=0, wrong=False):
        """
        Draw each direction's word on its tile:
        - up:         word above the tile
        - down:       word below the tile (so player sprite doesn't block it)
        - left/right: word centered on the tile
        """
        col, row = player_pos

        dir_offsets = {
            "up":    (col,     row - 1),
            "down":  (col,     row + 1),
            "left":  (col - 1, row),
            "right": (col + 1, row),
        }

        for direction, word in direction_words.items():
            if direction not in dir_offsets:
                continue

            tc, tr = dir_offsets[direction]
            tile_x = tc * TILE_SIZE
            tile_y = tr * TILE_SIZE

            total_width = sum(font.size(c)[0] + 1 for c in word)

            if direction == "up":
                letter_x = tile_x + (TILE_SIZE - total_width) // 2
                letter_y = tile_y - font.get_height() - 2
            elif direction == "down":
                letter_x = tile_x + (TILE_SIZE - total_width) // 2
                letter_y = tile_y + TILE_SIZE + 2
            else:  # left or right
                letter_x = tile_x + (TILE_SIZE - total_width) // 2
                letter_y = tile_y + (TILE_SIZE - font.get_height()) // 2

            for i, char in enumerate(word):
                if active_dir == direction:
                    if i < progress:
                        color = (0, 160, 0)     # green - correct
                    elif i == progress and wrong:
                        color = (200, 0, 0)     # red - wrong letter
                    else:
                        color = (0, 0, 0)       # black - not yet typed
                else:
                    color = (0, 0, 0)           # black - inactive

                char_surf = font.render(char.upper(), True, color)
                screen.blit(char_surf, (letter_x, letter_y))
                letter_x += char_surf.get_width() + 1

    def drawHUD(self, screen, screen_width, screen_height, active_dir, direction_words, progress, wrong):
        """Draw the bottom HUD bar showing current word being typed."""
        hud_y = screen_height - 60
        pygame.draw.rect(screen, (20, 20, 20), (0, hud_y, screen_width, 60))

        if not active_dir or active_dir not in direction_words:
            hint = pygame.font.SysFont(None, 28).render("Start typing to move!", True, (150, 150, 150))
            screen.blit(hint, (10, hud_y + 18))
            return

        word = direction_words[active_dir]
        font = pygame.font.SysFont(None, 36)
        label = pygame.font.SysFont(None, 24).render(f"{active_dir.upper()}:", True, (180, 180, 180))
        screen.blit(label, (10, hud_y + 20))

        letter_x = 80
        for i, char in enumerate(word):
            if i < progress:
                color = (0, 255, 0)
            elif i == progress and wrong:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            surf = font.render(char.upper(), True, color)
            screen.blit(surf, (letter_x, hud_y + 15))
            letter_x += surf.get_width() + 2

    def drawWinScreen(self, screen, screen_width, screen_height):
        """Draw a simple win overlay."""
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        font_big = pygame.font.SysFont(None, 72)
        font_small = pygame.font.SysFont(None, 36)
        win_text = font_big.render("YOU WIN!", True, (255, 215, 0))
        sub_text = font_small.render("Press R to play again or Q to quit", True, (255, 255, 255))
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, screen_height // 2 - 60))
        screen.blit(sub_text, (screen_width // 2 - sub_text.get_width() // 2, screen_height // 2 + 20))