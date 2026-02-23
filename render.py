import pygame

tileSize = 32

def loadAssets():

    # I still have to slice the assets so nothing will render as of now  
    assets = {
        "verticalWall" : pygame.image.load("assets/verticalWall.png"),
        "horizontalWall" : pygame.image.load("assets/horizontalWall.png"),
         "floor" : pygame.image.load("assets/floor.png"),
          "player" : pygame.image.load("assets/player.png"),
           "exit" : pygame.image.load("assets/player.png") 
    }

    return assets

def drawMaze(screen, maze, assets):

    rows = len(maze)
    cols = len(maze[0])

    for row in range(rows):
        for col in range(cols):

            tile = maze[row][col]
            x = col * tileSize
            y = row * tileSize

            if tile == 0:
                screen.blit(assets["floor"], (x,y))
                continue

            up = row > 0 and maze[row-1][col] == 1
            down = row < row-1 and maze[row+1][col] == 1
            left = col > 0 and maze[row][col-1] == 1
            right = col < 0 and maze[row][col+1] == 1

            if left or right:
                screen.blit(assets["horizontalWall"], (x,y))
            elif up or down:
                screen.blit(assets["verticalWall"], (x,y))
            else:
                screen.blit(assets["horizontalWall"], (x,y))
            
