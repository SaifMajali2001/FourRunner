import pygame

TILE_SIZE = 48  # larger tiles since maze is now smaller

class Render:

    def __init__(self):
        # Scale everything except player to tile size
        self.assets = {
            "verticalWall":   pygame.transform.scale(pygame.image.load("assets/verticalWall2.png"), (TILE_SIZE, TILE_SIZE)),
            "horizontalWall": pygame.transform.scale(pygame.image.load("assets/horizontalWall2.png"), (TILE_SIZE, TILE_SIZE)),
            "floor":          pygame.transform.scale(pygame.image.load("assets/floor.png"), (TILE_SIZE, TILE_SIZE)),
            "exit":           pygame.transform.scale(pygame.image.load("assets/exit.png"), (TILE_SIZE, TILE_SIZE)),
        }

        # Load player and scale preserving aspect ratio so it isn't squished
        raw_player = pygame.image.load("assets/player2.png")
        pw, ph = raw_player.get_size()
        scale_factor = TILE_SIZE / max(pw, ph)
        new_w = int(pw * scale_factor)
        new_h = int(ph * scale_factor)
        self.assets["player"] = pygame.transform.scale(raw_player, (new_w, new_h))
        self.player_size = (new_w, new_h)

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
        # Center player sprite on the tile
        pw, ph = self.player_size
        x = col * TILE_SIZE + (TILE_SIZE - pw) // 2
        y = row * TILE_SIZE + (TILE_SIZE - ph) // 2
        screen.blit(self.assets["player"], (x, y))

    def drawExit(self, screen, exitPOS):
        col, row = exitPOS
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        screen.blit(self.assets["exit"], (x, y))

    def _measureWord(self, font, word):
        """Return the actual pixel width of the full word string."""
        return font.size(word.upper())[0]

    def _drawWordWithBackground(self, screen, font, word, x, y, active, progress, wrong):
        """Draw a word with a solid dark background box behind it."""
        padding = 4
        total_width = self._measureWord(font, word)
        bg_rect = pygame.Rect(x - padding, y - padding, total_width + padding * 2, font.get_height() + padding * 2)

        # Draw solid background (no alpha needed, simpler and more reliable)
        pygame.draw.rect(screen, (30, 30, 30), bg_rect, border_radius=3)
        pygame.draw.rect(screen, (100, 100, 100), bg_rect, 1, border_radius=3)

        lx = x
        for i, char in enumerate(word):
            if active:
                if i < progress:
                    color = (0, 220, 0)
                elif i == progress and wrong:
                    color = (230, 60, 60)
                else:
                    color = (255, 255, 255)
            else:
                color = (210, 210, 210)

            surf = font.render(char.upper(), True, color)
            screen.blit(surf, (lx, y))
            lx += surf.get_width() + 1

    def drawWordsOnTiles(self, screen, maze, player_pos, direction_words, font, active_dir=None, progress=0, wrong=False):
        """
        Draw each direction's word on its tile with a background:
        - up:    word above the tile, centered
        - down:  word below the tile, centered
        - left:  word on the left tile, right-aligned so it doesn't overlap the player
        - right: word on the right tile, left-aligned
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
            total_width = self._measureWord(font, word)
            is_active = (active_dir == direction)
            padding = 4

            if direction == "up":
                lx = tile_x + (TILE_SIZE - total_width) // 2
                ly = tile_y - font.get_height() - padding * 2 - 2
            elif direction == "down":
                lx = tile_x + (TILE_SIZE - total_width) // 2
                ly = tile_y + TILE_SIZE + 4
            elif direction == "left":
                # Right-align the word within the left tile so it stays away from the player
                lx = tile_x + TILE_SIZE - total_width - padding - 2
                ly = tile_y + (TILE_SIZE - font.get_height()) // 2
            else:  # right
                lx = tile_x + padding + 2
                ly = tile_y + (TILE_SIZE - font.get_height()) // 2

            self._drawWordWithBackground(screen, font, word, lx, ly, is_active, progress, wrong)

    def drawHUD(self, screen, screen_width, screen_height, active_dir, direction_words, progress, wrong, elapsed_seconds, penalty_active, penalty_remaining):
        """Draw the bottom HUD bar with word progress, timer, and penalty indicator."""
        hud_y = screen_height - 60
        pygame.draw.rect(screen, (20, 20, 20), (0, hud_y, screen_width, 60))

        # Timer (right side of HUD)
        timer_font = pygame.font.SysFont(None, 30)
        mins = int(elapsed_seconds) // 60
        secs = int(elapsed_seconds) % 60
        timer_str = f"Time: {mins:02d}:{secs:02d}"
        timer_surf = timer_font.render(timer_str, True, (255, 255, 100))
        screen.blit(timer_surf, (screen_width - timer_surf.get_width() - 10, hud_y + 18))

        # Penalty message
        if penalty_active:
            penalty_font = pygame.font.SysFont(None, 28)
            penalty_surf = penalty_font.render(f"PENALTY! {penalty_remaining:.1f}s", True, (255, 80, 80))
            screen.blit(penalty_surf, (10, hud_y + 18))
            return

        if not active_dir or active_dir not in direction_words:
            hint = pygame.font.SysFont(None, 28).render("Start typing to move!", True, (150, 150, 150))
            screen.blit(hint, (10, hud_y + 18))
            return

        word = direction_words[active_dir]
        hud_font  = pygame.font.SysFont(None, 36)
        label     = pygame.font.SysFont(None, 24).render(f"{active_dir.upper()}:", True, (180, 180, 180))
        screen.blit(label, (10, hud_y + 20))

        letter_x = 80
        for i, char in enumerate(word):
            if i < progress:
                color = (0, 255, 0)
            elif i == progress and wrong:
                color = (255, 80, 80)
            else:
                color = (255, 255, 255)
            surf = hud_font.render(char.upper(), True, color)
            screen.blit(surf, (letter_x, hud_y + 15))
            letter_x += surf.get_width() + 2

    def drawWinScreen(self, screen, screen_width, screen_height, elapsed_seconds, scores):
        """Draw win overlay with final time and top 8 scoreboard."""
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        font_big   = pygame.font.SysFont(None, 64)
        font_med   = pygame.font.SysFont(None, 36)
        font_small = pygame.font.SysFont(None, 28)

        win_text = font_big.render("YOU WIN!", True, (255, 215, 0))
        screen.blit(win_text, (screen_width // 2 - win_text.get_width() // 2, 30))

        mins = int(elapsed_seconds) // 60
        secs = int(elapsed_seconds) % 60
        time_text = font_med.render(f"Your time: {mins:02d}:{secs:02d}", True, (255, 255, 255))
        screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, 100))

        sb_title = font_med.render("Top 8 Times", True, (255, 215, 0))
        screen.blit(sb_title, (screen_width // 2 - sb_title.get_width() // 2, 145))

        for i, score in enumerate(scores[:8]):
            sm = int(score) // 60
            ss = int(score) % 60
            rank_color = (255, 215, 0) if i == 0 else (200, 200, 200)
            entry = font_small.render(f"#{i+1}  {sm:02d}:{ss:02d}", True, rank_color)
            screen.blit(entry, (screen_width // 2 - entry.get_width() // 2, 185 + i * 30))

        hint = font_small.render("R = play again    Q = quit", True, (150, 150, 150))
        screen.blit(hint, (screen_width // 2 - hint.get_width() // 2, screen_height - 40))