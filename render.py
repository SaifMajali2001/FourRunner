import pygame

tileSize = 32

def loadAssets():
    assets = {
        "verticalWall" : pygame.image.load("assets/verticalWall2.png"),
        "horizontalWall" : pygame.image.load("assets/horizontalWall2.png"),
        "floor" : pygame.image.load("assets/floor.png"),
        "player" : pygame.image.load("assets/player2.png"),
        "exit" : pygame.image.load("assets/exit.png") 
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
            down = row < rows-1 and maze[row+1][col] == 1  # fixed: rows-1
            left = col > 0 and maze[row][col-1] == 1
            right = col < cols-1 and maze[row][col+1] == 1  # fixed: cols-1

            if left or right:
                screen.blit(assets["horizontalWall"], (x,y))
            elif up or down:
                screen.blit(assets["verticalWall"], (x,y))
            else:
                screen.blit(assets["horizontalWall"], (x,y))

def drawPlayer(screen, playerPOS, assets):
    row, col = playerPOS

    x = col * tileSize  # fixed: col drives x
    y = row * tileSize  # fixed: row drives y

    screen.blit(assets["player"], (x,y))

def drawExit(screen, exitPOS, assets):
    row, col = exitPOS

    x = col * tileSize  # fixed: col drives x
    y = row * tileSize  # fixed: row drives y

    screen.blit(assets["exit"], (x,y))