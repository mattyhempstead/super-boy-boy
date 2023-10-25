#   
#   V1.0.0
#   
#   + Rectangle Physics created
#
#

import pygame
import random

def printStats():
    print("\nxCoord: " + str(xCoord))
    print("yCoord: " + str(yCoord))
    print("velocity: " + str(velocity) + "\n")

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
WHITE = (0xFF, 0xFF, 0xFF)
PI = 3.141592653

pygame.init()

size = (500, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("mygame.my")

done = False
 
clock = pygame.time.Clock()

playerSize = 50
xCoord = 225
yCoord = 300
velocity = 0

boxes = []
boxes.append([0,450,500,50]) # Ground
boxes.append([0,-45,500,50]) # Roof
boxes.append([-45,0,50,500]) # Left wall
boxes.append([495,0,50,500]) # Right wall

boxes.append([330,370,70,20]) # Bottom layer
boxes.append([100,370,70,20])

boxes.append([400,270,70,20]) # Middle-bottom layer
boxes.append([30,270,70,20])
boxes.append([215,270,70,20])

boxes.append([330,170,70,20]) # Middle-top layer
boxes.append([100,170,70,20])

boxes.append([400,70,70,20]) # Top layer
boxes.append([30,70,70,20])
boxes.append([215,70,70,20])

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
                moveUp = True
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moveUp = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
        
    # --- xAxis Movement --- #    
    if (moveRight):
        xCoord = xCoord+2
    elif (moveLeft):
        xCoord = xCoord-2

    # --- Jumping --- #
    if moveUp:
        for i in range(len(boxes)):
            if (xCoord + playerSize) > boxes[i][0]:
                if xCoord < (boxes[i][0] + boxes[i][2]):
                    if (yCoord + playerSize) == boxes[i][1]:
                        velocity = 6

    # --- Gravity --- #
    yCoord -= velocity
    velocity -= 9.8/60

    # --- Collision --- #
    for i in range(len(boxes)):
        if (xCoord + playerSize) > boxes[i][0]:
            if xCoord < (boxes[i][0] + boxes[i][2]):
                if (yCoord + playerSize) > boxes[i][1]:
                    if yCoord < (boxes[i][1] + boxes[i][3]):
                        #print("Collided")
                        N = yCoord + playerSize - boxes[i][1]
                        E = boxes[i][0] + boxes[i][2] - xCoord
                        S = boxes[i][1] + boxes[i][3] - yCoord
                        W = xCoord + playerSize - boxes[i][0]
                        if (N<E and N<S and N<W):
                            yCoord = boxes[i][1] - playerSize
                            velocity = 0
                        elif (E<S and E<W):
                            xCoord = boxes[i][0] + boxes[i][2]
                        elif (S<W):
                            yCoord = boxes[i][1] + boxes[i][3]
                            velocity = 0
                        else:
                            xCoord = boxes[i][0] - playerSize
                        
                        
                        
                        
    

    # ----------------- #
    
    screen.fill(backgroundColour)

    pygame.draw.rect(screen, squareColour, [xCoord,yCoord,playerSize,playerSize])

    for i in range(len(boxes)):         # Draws boxes
        pygame.draw.rect(screen, squareColour, [boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])
    
    #pygame.draw.polygon(screen, BLACK, [[100, 100], [90, 200], [200, 200]], 50)
    
    pygame.display.flip()
    clock.tick(60)

    
pygame.quit()

