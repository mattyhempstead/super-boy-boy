#   
#   V1.0.4
#   
#   ~ Tweaked collision script
#   + Added ability to adjust player height/width seperately
#
#

import pygame
import random

def printStats():
    print("\nplayer[0]: " + str(player[0]))
    print("player[1]: " + str(player[1]))
    print("velocity: " + str(velocity) + "\n")

def playerJumpAllowed():
    for i in range(len(boxes)):
        if ( max(player[0]+player[2],boxes[i][0]+boxes[i][2]) - min(player[0],boxes[i][0]) ) < ( player[2] + boxes[i][2] ): 
                if (player[1] + player[3]) == boxes[i][1]:
                    return True



BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)
PI = 3.141592653

pygame.init()

size = (1000, 700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("mygame.my")

done = False
 
clock = pygame.time.Clock()
#           [x, y,  w,  h]
player =    [0, 0,  50, 50]
player[0] = size[0]/2 - (player[2]/2)
player[1] = size[1] - 70 - player[3]
player[1] = player[1]
velocity = 0
playerSpeed = 5
playerJump = 8

gravity = 9.8

boxes = []
boxes.append([0,size[1]-50,size[0],50]) # Ground
boxes.append([0,-45,size[0],50])        # Roof
boxes.append([-45,0,50,size[1]])        # Left wall
boxes.append([size[0]-5,0,50,size[1]])  # Right wall

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
        player[0] = player[0] + playerSpeed
    elif (moveLeft):
        player[0] = player[0] - playerSpeed

    # --- Jumping --- #
    if moveUp:
        velocity = playerJump
        moveUp = False

    # --- Gravity --- #
    player[1] -= velocity
    velocity -= gravity/60

    # --- Collision --- #
    for i in range(len(boxes)):     # For every box in boxes array
        leftSide = min( player[0], boxes[i][0] )                        # Side furthest left
        rightSide = max( player[0]+player[2], boxes[i][0]+boxes[i][2] ) # Side furthest right
        if ( rightSide - leftSide ) < ( player[2] + boxes[i][2] ):      # if distance between outer edges of boxes is less than the width of them both combined
            topSide = min( player[1], boxes[i][1] )                         # Side furthest up
            bottomSide = max( player[1]+player[3], boxes[i][1]+boxes[i][3] )# Side furthest down
            if ( bottomSide - topSide ) < ( player[3] + boxes[i][3] ):      # if distance between top and bottom of boxes is less than the height of them both combined
                #print("Collided")
                N = player[1] + player[3] - boxes[i][1]
                E = boxes[i][0] + boxes[i][2] - player[0]
                S = boxes[i][1] + boxes[i][3] - player[1]
                W = player[0] + player[2] - boxes[i][0]
                if min(N,E,S,W) == N:
                    player[1] = boxes[i][1] - player[3]
                    if velocity < 0:
                        velocity = 0
                elif min(E,S,W) == E:
                    player[0] = boxes[i][0] + boxes[i][2]
                elif (S<W):
                    player[1] = boxes[i][1] + boxes[i][3]
                    if velocity > 0:
                        velocity = 0
                else:
                    player[0] = boxes[i][0] - player[2]              
    

    # --- Rendering --- #
    
    screen.fill(backgroundColour)

    pygame.draw.rect(screen, squareColour, [player[0],player[1],player[2],player[3]])

    for i in range(len(boxes)):         # Draws boxes
        pygame.draw.rect(screen, squareColour, [boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])
    
    #pygame.draw.polygon(screen, BLACK, [[100, 100], [90, 200], [200, 200]], 50)
    
    pygame.display.flip()
    clock.tick(60)

    
pygame.quit()

