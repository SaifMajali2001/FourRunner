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