import pygame

tileSize = 32

def loadAssests():

    # I still have to slice the assets so nothing will render as of now  
    assets = {
        "wall" : pygame.image.load("assests/wall.png"),
         "floor" : pygame.image.load("assests/floor.png"),
          "player" : pygame.image.load("assests/player.png"),
           "exit" : pygame.image.load("assests/player.png") 
    }

    return assets

    def drawMaze(screen, maze, assets):

        for row in range(len(maze)):
            for col in range(len(maze[0])):

                tile = maze[row][column]
                x = col * tileSize
                y = row * tileSize

                if tile == 1:
                    screen.blit(assets["wall"], (x,y))
                else:
                    screenblit(assets["floor"], (x,y))