import pygame

tileSize = 32


class Render:


    def __init__(self):
        self.assets = {
                "verticalWall" : pygame.image.load("assets/verticalWall2.png"),
                "horizontalWall" : pygame.image.load("assets/horizontalWall2.png"),
                "floor" : pygame.image.load("assets/floor.png"),
                "player" : pygame.image.load("assets/player2.png"),
                "exit" : pygame.image.load("assets/exit.png") 
            }

    def drawMaze(self, screen, maze):

        rows = len(maze)
        cols = len(maze[0])

        for row in range(rows):
            for col in range(cols):

                tile = maze[row][col]
                x = col * tileSize
                y = row * tileSize

                if tile == 0:
                    screen.blit(self.assets["floor"], (x,y))
                    continue

            # requires us to use ASCII when actually generating the randomized maze

                up = row > 0 and maze[row-1][col] == 1
                down = row < row-1 and maze[row+1][col] == 1
                left = col > 0 and maze[row][col-1] == 1
                right = col < 0 and maze[row][col+1] == 1

                if left or right:
                    screen.blit(self.assets["horizontalWall"], (x,y))
                elif up or down:
                    screen.blit(self.assets["verticalWall"], (x,y))
                else:
                    screen.blit(self.assets["horizontalWall"], (x,y))

    def drawPlayer(self, screen, playerPOS):

        row, col = playerPOS

        x = row * tileSize
        y = col * tileSize

        screen.blit(self.assets["player"], (x,y))

    def drawExit(self, screen, exitPOS):
        row, col = exitPOS

        x = row * tileSize
        y = col * tileSize
        screen.blit(self.assets["exit"], (x,y))


    

