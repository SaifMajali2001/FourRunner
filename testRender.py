import pygame
from render import Render
import random

pygame.init()

screen = pygame.display.set_mode((640, 720))
pygame.display.set_caption("Render Test")

renderer = Render()
font = pygame.font.SysFont(None, 28)

maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,1,0,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1],
    [1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1],
    [1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,0,1,1,1,0,1,1,1,0,1,1,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

playerPOS = (1, 1)
exitPOS = (18, 18)

# Hardcoded word list for testing
word_list = ["apple", "brave", "crane", "delta", "eagle"]
words = {
    "up":    random.choice(word_list),
    "down":  random.choice(word_list),
    "left":  random.choice(word_list),
    "right": random.choice(word_list)
}

# Typing state
selected_dir = None
progress = 0
wrong = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Select direction with arrow keys only
            if event.key == pygame.K_UP:
                selected_dir = "up"
                progress = 0
                wrong = False
            elif event.key == pygame.K_DOWN:
                selected_dir = "down"
                progress = 0
                wrong = False
            elif event.key == pygame.K_LEFT:
                selected_dir = "left"
                progress = 0
                wrong = False
            elif event.key == pygame.K_RIGHT:
                selected_dir = "right"
                progress = 0
                wrong = False

            # Only check letters if NOT a direction key
            elif event.unicode.isalpha() and selected_dir:
                char = event.unicode.lower()
                expected = words[selected_dir][progress]

                if char == expected:
                    progress += 1
                    wrong = False

                    # Word complete
                    if progress == len(words[selected_dir]):
                        print(f"Correct! Moving {selected_dir}")
                        words[selected_dir] = random.choice(word_list)
                        progress = 0
                        selected_dir = None
                else:
                    # Wrong letter - new word
                    wrong = True
                    words[selected_dir] = random.choice(word_list)
                    progress = 0

    # Draw everything
    renderer.drawMaze(screen, maze)
    renderer.drawPlayer(screen, playerPOS)
    renderer.drawExit(screen, exitPOS)
    if selected_dir:
        renderer.drawWords(screen, words, font, selected_dir, progress, wrong)
    pygame.display.flip()

pygame.quit()