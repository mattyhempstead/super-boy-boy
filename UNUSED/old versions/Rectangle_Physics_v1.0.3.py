#   
#   V1.0.3
#   
#   - Disabled repeated jumping
#   + Added Randomised, Scaleable Block Layout
#   + Gravity variable
#
#

import pygame
import random

def printStats():
    print("\nxCoord: " + str(xCoord))
    print("yCoord: " + str(yCoord))
    print("velocity: " + str(velocity) + "\n")

def playerJumpAllowed():
    for i in range(len(boxes)):
        if ( max(xCoord+playerSize,boxes[i][0]+boxes[i][2]) - min(xCoord,boxes[i][0]) ) < ( playerSize + boxes[i][2] ): 
                if (yCoord + playerSize) == boxes[i][1]:
                    return True



BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
WHITE = (0xFF, 0xFF, 0xFF)
PI = 3.141592653

pygame.init()

size = (1000, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("mygame.my")

done = False
 
clock = pygame.time.Clock()

playerSize = 50
xCoord = size[0]/2 - (playerSize/2)
yCoord = size[1]-70-playerSize
velocity = 0
playerSpeed = 5
playerJump = 8
gravity = 9.8

boxes = []
boxes.append([0,size[1]-50,size[0],50]) # Ground
boxes.append([0,-45,size[0],50]) # Roof
boxes.append([-45,0,50,size[1]]) # Left wall
boxes.append([size[0]-5,0,50,size[1]]) # Right wall

for x in range(0,10):
    for y in range(1,6):
        if random.random() < 0.5:
            w = size[0]/10
            h = size[1]/7
            boxes.append([x*w,y*h,w,20])
            

squareColour = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
backgroundColour = (255-squareColour[0],255-squareColour[1],255-squareColour[2])

moveUp = False
moveRight = False
moveLeft = False


print("Welcome to rectangle thingy with: ")
print("  - Left/Right Movement")
print("  - Jumping")
print("  - Gravity")
print("  - Collision with other rectangles")

 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # If user clicked close
            print("User tried to quit")
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if playerJumpAllowed():
                    moveUp = True
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True
            elif event.key == pygame.K_s:
                printStats()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moveUp = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
        
    # --- xAxis Movement --- #    
    if (moveRight):
        xCoord = xCoord+playerSpeed
    elif (moveLeft):
        xCoord = xCoord-playerSpeed

    # --- Jumping --- #
    if moveUp:
        velocity = playerJump
        moveUp = False

    # --- Gravity --- #
    yCoord -= velocity
    velocity -= gravity/60

    # --- Collision --- #
    for i in range(len(boxes)):     # For every box in boxes array
        if ( max(xCoord+playerSize,boxes[i][0]+boxes[i][2]) - min(xCoord,boxes[i][0]) ) < ( playerSize + boxes[i][2] ):         # if distance between outer edges of boxes is less than the width of them both combined
            if ( max(yCoord+playerSize,boxes[i][1]+boxes[i][3]) - min(yCoord,boxes[i][1]) ) < ( playerSize + boxes[i][3] ):     # if distance between top and bottom of boxes is less than the height of them both combined
                #print("Collided")
                N = yCoord + playerSize - boxes[i][1]
                E = boxes[i][0] + boxes[i][2] - xCoord
                S = boxes[i][1] + boxes[i][3] - yCoord
                W = xCoord + playerSize - boxes[i][0]
                if min(N,E,S,W) == N:
                    yCoord = boxes[i][1] - playerSize
                    if velocity < 0:
                        velocity = 0
                elif min(E,S,W) == E:
                    xCoord = boxes[i][0] + boxes[i][2]
                elif (S<W):
                    yCoord = boxes[i][1] + boxes[i][3]
                    if velocity > 0:
                        velocity = 0
                else:
                    xCoord = boxes[i][0] - playerSize

    #   if player is colliding with rectangle
    #       
    #       if difference between lowest x and highest x is larger than added width's
    #   
    #       if ( max(xCoord+playerSize,boxes[i][0]+boxes[i][2]) - min(xCoord,boxes[i][0]) ) > ( playerSize + boxes[i][2] )
    #
    #
    #
    #
                        
                        
                        
    

    # ----------------- #
    
    screen.fill(backgroundColour)

    pygame.draw.rect(screen, squareColour, [xCoord,yCoord,playerSize,playerSize])

    for i in range(len(boxes)):         # Draws boxes
        pygame.draw.rect(screen, squareColour, [boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])
    
    #pygame.draw.polygon(screen, BLACK, [[100, 100], [90, 200], [200, 200]], 50)
    
    pygame.display.flip()
    clock.tick(60)

    
pygame.quit()

