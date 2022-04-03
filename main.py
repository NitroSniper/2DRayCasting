# this is gonna just be me testing how to do raycasting.
# the tutorial which I'm gonna base this on is
# https://lodev.org/cgtutor/raycasting.html and https://www.youtube.com/watch?v=eOCQfxRQ2pY

#first let's make a tile system
import pygame
from math import pi, radians, sin, cos, tan, floor
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
)
TILE_SIZE = 32
FIRSTQUAD = pi/2
THIRDQUAD = 3*pi/2

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
        self.image = pygame.surface.Surface((TILE_SIZE/4, TILE_SIZE/4))
        self.image.fill((255,0,255))
    
    def findXY(self):
        return self.x//TILE_SIZE*TILE_SIZE, self.y//TILE_SIZE*TILE_SIZE
    
    def findtileXY(self):
        return self.x//TILE_SIZE, self.y//TILE_SIZE
    
    def screenPos(self):
        return (self.x - self.image.get_width()/2, self.y - self.image.get_height()/2)
    def DXDY(self):
        tilex, tiley = self.findXY()
        dy = self.y - tiley
        dx = self.x - tilex
        return dx, dy
    def tileDXDY(self):
        tilex, tiley = self.findXY()
        dy = self.y - tiley
        dx = self.x - tilex
        return dx/TILE_SIZE, dy/TILE_SIZE

    def findRelativeCoordinates(self, theta):
        tilex, tiley = self.findXY()
        if 0<theta<180: # theta going upwards in diagram
            dy = self.y - tiley
        else:# theta going downwards
            dy = (self.y - tiley) - TILE_SIZE
        if 90<theta<270: # theta going left
            dx = self.x - tilex
        else: # theta going right
            dx = (self.x - tilex) - TILE_SIZE
        
        return (
            self.x - tilex, #player x position within the tile
            self.y - tiley, #player y position within the tile
            dx, dy, #player direction distance to the grid boundary
            tilex, tiley # tile position
        )
    
#first lets state some stuff
#x and y is the position the player is relative to the tile system. not the actual coordinate. for this. this will be a multiple of 32
#dx and dy is what position the player is relative inside the tile it is in. 

#let's create a find x and y within the Player. DONE
#to reach the first vertical line I know that the first vertical line collision is -dy, the x to that will be tan(theta)*-dy 
# where theta is the ray angle. 

#due to pygame radians going anti - clockwise this would mean that I'm gonna formalise it to clockwise

# if theta is in the first quadrant, x+, y-, 2nd - x-, y-. 3rd -  x-, y+, 4th - x+, y+

#i*pi/4 where i is range(8)
# sin [0.0, 0.7071, 1.0, 0.7071, 0.0, -0.7071, -1.0, -0.7071]
# cos [1.0, 0.7071, 0.0, -0.7071, -1.0, -0.7071, -0.0, 0.7071]
# tan [0.0, 1.0, BIG, -1.0, -0.0, 1.0, BIG, -1.0]
# tan - pos pos, neg pos, neg neg, pos neg

def calculate_angle(theta, PLAYER, theMap):

    px, py, dx, dy, tilex, tiley, = PLAYER.findRelativeCoordinates(theta)
    #print (px, py, dx, dy, tilex, tiley)
    theta = radians(theta)
    ratio = 1/tan(theta) if tan(theta) else 100
    xIntercept = tilex + px + dy*ratio # the x coordinate of the ray passing the first row
    yRow = tiley + py - dy
    yIntercept = tiley + py + dx/ratio # the y coordinate of the ray passing the first coloumn
    xRow = tilex + px - dx
    #print (dx)
    #print (xIntercept, yRow, yIntercept, xRow)
    return ((xIntercept, yRow), (xRow, yIntercept))



              
##        theta = radians(theta)
##        #print (theta)
##        x, y= PLAYER.findXY()
##        tilex, tiley = PLAYER.findtileXY()
##        dx, dy = PLAYER.DXDY()
##        tiledx, tiledy = PLAYER.tileDXDY()
##        # print (tan(7*pi/4), tan(pi/4))
##        # I had to negate (dy,dx)/tan(theta) since it never did the actual collision spots. 
##        # Looking back at it it could have done. it just starts at the -1 of the collision.
##
##        deltax, deltay = -tan(theta), 1/tan(theta)
##        #print (deltax, deltay)
##
##        #---check horizontal
##
##        xIntercept = x+dx-dy/tan(theta) # the x coordinate of the ray passing the first row
##        yIntercept = y+dy+dx/tan(theta) # the y coordinate of the ray passing the first coloumn
##        
##        tilexIntercept = tilex+tiledx-tiledy/tan(theta)
##        tileyIntercept = tiley+tiledy+tiledx/tan(theta)
##        
##        print (f'({tilexIntercept}, {tiley}), ({tileyIntercept}, {tilex}), {xStep}, {yStep}')
##        
##        #figure out theta,
##
##        #find vertical collision
##        #x is tilex and y is tiley
####        while 0 <= tileyIntercept < 24:
####            #print (tilex, tileyIntercept)
####            if theMap[floor(tileyIntercept)][tilex].val:
####                theMap[floor(tileyIntercept)][tilex].image.fill((255,0,0))
####                
####                break
####            tilex += xStep
####            tileyIntercept += deltax
            


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
    PLAYER = PlayerObject(234, 210) # 224, 192 -> 256, 224
    #theta = radians(45)
    clock = pygame.time.Clock()
    e = 45
    program_running = True
    while program_running:
        #Event
        for event in pygame.event.get(): #<show> for new events happening
            if event.type == KEYDOWN: #if a key is pressed down
                if event.key == K_ESCAPE: #<show> if new event is quit
                    program_running = False #<show> program sto running
            elif event.type == QUIT: #<show> if new event is quit
                program_running = False

        for tile in TILES:
            tile.image.fill((255, 255, 255))
        
        xinter, yinter = calculate_angle(e%360, PLAYER, theMap)
        SCREEN.fill((0,0,0))
        drawGridLine(SCREEN, TILE_SIZE)
        #Drawing
        for tile in TILES:
            if tile.val:
                SCREEN.blit(tile.image, (tile.x, tile.y))
        SCREEN.blit(PLAYER.image, PLAYER.screenPos())
        
        pygame.draw.line(SCREEN, (0,255,0), (PLAYER.x, PLAYER.y), (PLAYER.x+cos(radians(e))*30, PLAYER.y-sin(radians(e))*30))
        pygame.draw.line(SCREEN, (255,0,0), (PLAYER.x, PLAYER.y),xinter)
        pygame.draw.line(SCREEN, (0,0,255), (PLAYER.x, PLAYER.y),yinter)
        #pygame.draw.line(SCREEN, (0,255,0), (PLAYER.x, PLAYER.y), (xIntercept, 192))
        pygame.display.update()
        e += 1
        #break

        clock.tick(20)

        # clock.tick()
        # print(clock.get_fps())
    pygame.display.quit()





if __name__ == '__main__':
    main()
