# this is gonna just be me testing how to do raycasting.
# the tutorial which I'm gonna base this on is
# https://lodev.org/cgtutor/raycasting.html and https://www.youtube.com/watch?v=eOCQfxRQ2pY

#first let's make a tile system
import pygame
from math import pi, radians, sin, cos, tan
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
)
TILE_SIZE = 32

from random import randint
Default_Map = [
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,2,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,3,0,0,0,3,0,0,0,1],
  [1,0,0,0,0,0,2,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,2,2,0,2,2,0,0,0,0,3,0,3,0,3,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,5,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Overview():
    def createTiles(SCREEN_SIZE, TILE_SIZE):
        # theMap = tuple([
        #     tuple([TileObjects(x*TILE_SIZE, y*TILE_SIZE)
        #         for x in range(SCREEN_SIZE[0]//TILE_SIZE)])
        #      for y in range(SCREEN_SIZE[1]//TILE_SIZE)])
        # return tuple([i for y in theMap for i in y]), theMap

        theMap = tuple([
            tuple([TileObjects(x*TILE_SIZE, y*TILE_SIZE, val)
                for x, val in enumerate(row)])
             for y, row in enumerate(Default_Map)])
        return tuple([i for y in theMap for i in y]), theMap

class screenObjects():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TileObjects(screenObjects):
    def __init__(self, x,y, val):
        super().__init__(x,y)
        self.image = pygame.surface.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255,255,255))
        self.val = val
    def __bool__(self):
        return self.val

class PlayerObject(screenObjects):
    def  __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.surface.Surface((TILE_SIZE/2, TILE_SIZE/2))
        self.image.fill((255,0,255))
    
    def findXYandDxDy(self):
        tilePos = self.x//TILE_SIZE*TILE_SIZE, self.y//TILE_SIZE*TILE_SIZE
        #return *tilePos, tilePos[0]-self.x, tilePos[1]-self.y
        return *tilePos, self.x-tilePos[0], self.y- tilePos[1]
    
    def screenPos(self):
        return (self.x - self.image.get_width()/2, self.y - self.image.get_height()/2)




#first lets state some stuff
#x and y is the position the player is relative to the tile system. not the actual coordinate. for this. this will be a multiple of 32
#dx and dy is what position the player is relative inside the tile it is in. 

#let's create a find x and y within the Player. DONE
#to reach the first vertical line I know that the first vertical line collision is -dy, the x to that will be tan(theta)*-dy 
# where theta is the ray angle. 

#due to pygame radians going anti - clockwise this would mean that I'm gonna formalise it to clockwise

def cw(angle):
    '''
    angle has to be in radians. turns it into 2*pi - angle. just turns it clockwise
    '''
    return 2*pi - angle



def drawGridLine(SCREEN, TILE_SIZE):
    width = SCREEN.get_width()
    height = SCREEN.get_height()
    #draw coloumn
    for x in range(0, width, TILE_SIZE):
        pygame.draw.line(SCREEN, (64, 64, 64), (x, 0), (x, height))
    for y in range(0, height, TILE_SIZE):
        pygame.draw.line(SCREEN, (64, 64, 64), (0, y), (width, y))

def main():
    SCREEN_WIDTH = 768  # <show> pixel Width of the game
    SCREEN_HEIGHT = 768  # <show> pixel height of the game
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    TILES, theMap = Overview.createTiles(SCREEN_SIZE, TILE_SIZE)
    PLAYER = PlayerObject(234, 210)
    RAYANGLE = radians(315)
    clock = pygame.time.Clock()
    theta = cw(RAYANGLE)
    
    program_running = True
    while program_running:
        #Event
        for event in pygame.event.get(): #<show> for new events happening
            if event.type == KEYDOWN: #if a key is pressed down
                if event.key == K_ESCAPE: #<show> if new event is quit
                    program_running = False #<show> program sto running
            elif event.type == QUIT: #<show> if new event is quit
                program_running = False

        x, y, dx, dy = PLAYER.findXYandDxDy()
        print (x, y, dx, dy)
        # print (tan(7*pi/4), tan(pi/4))
        # I had to negate (dy,dx)/tan(theta) since it never did the actual collision spots. 
        # Looking back at it it could have done. it just starts at the -1 of the collision.
        xStep, yStep = tan(theta),1/tan(theta)
        xIntercept = x+dx + dy/tan(theta)# this is the first row collision
        yIntercept = y+dy - dx/tan(theta) # this is the first coloumn collision
        print (xIntercept, yIntercept)
        deltax = -tan(theta) # y offset between each collision of deltax
        deltay = 1/tan(theta)# x offset between each collsion of deltay

        drawGridLine(SCREEN, TILE_SIZE)
        #Drawing
        for tile in TILES:
            if tile.val:
                SCREEN.blit(tile.image, (tile.x, tile.y))
        SCREEN.blit(PLAYER.image, PLAYER.screenPos())
        pygame.draw.line(SCREEN, (0,255,0), (PLAYER.x, PLAYER.y), (PLAYER.x+cos(RAYANGLE)*30, PLAYER.y+sin(RAYANGLE)*30), width=2)
        pygame.display.update()
        break



        #clock.tick()
        #print(clock.get_fps())






if __name__ == '__main__':
    main()
