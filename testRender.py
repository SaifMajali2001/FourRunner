import pygame
from render import loadAssets, drawMaze

pygame.init()

screen = pygame.display.set_mode((640,640))

pygame.display.set_caption("Render Test")

assets = loadAssets()

maze = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,0,1], [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1], [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1], [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1], [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        drawMaze(screen, maze, assets)
        pygame.display.flip()

pygame.quit()