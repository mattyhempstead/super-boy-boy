#   
#   V1.0.6.1
#   
#   ~ Tweaked function code
#
#

import pygame
import random

def printStats():
    print("\nplayer[0]: " + str(player[0]))
    print("player[1]: " + str(player[1]))
    print("velocity: " + str(vel) + "\n")

def playerJumpAllowed():
    for i in range(len(boxes)):
        if ( max(player[0]+player[2],boxes[i][0]+boxes[i][2]) - min(player[0],boxes[i][0]) ) < ( player[2] + boxes[i][2] ): 
                if (player[1] + player[3]) == boxes[i][1]:
                    return True

def playerWallJumpAllowed():
    print("")

def rectToRectCollision(a,b):
    leftSide = min( a[0], b[0] )                        # Side furthest left
    rightSide = max( a[0]+a[2], b[0]+b[2] )             # Side furthest right
    if ( rightSide - leftSide ) < ( a[2] + b[2] ):      # if distance between outer edges of boxes is less than the width of them both combined
        topSide = min( a[1], b[1] )                     # Side furthest up
        bottomSide = max( a[1]+a[3], b[1]+b[3] )        # Side furthest down
        if ( bottomSide - topSide ) < ( a[3] + b[3] ):  # if distance between top and bottom of boxes is less than the height of them both combined
            return True


  

BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)

pygame.init()
size = (1080, 720)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("mygame.my")

done = False
 
clock = pygame.time.Clock()
#           [x, y,  w,  h,  c]
player =    [0, 0,  50, 50, RED]
player[0] = size[0]/2 - (player[2]/2)
player[1] = size[1] - 70 - player[3]
player[1] = player[1]
vel = [0,0]
playerSpeed = 8
playerJump = 9

GRAVITY = 13      # pixels per second
FRICTION = 0.95

boxes = []
boxes.append([  0,            size[1]-50,     size[0],    50,       GREEN   ]) # Ground
boxes.append([  0,            -45,            size[0],    50,       GREEN   ])        # Roof
boxes.append([  -45,          0,              50,         size[1],  GREEN   ])        # Left wall
boxes.append([  size[0]-5,    0,              50,         size[1],  GREEN   ])  # Right wall

for x in range(0,10):
    for y in range(1,6):
        if random.random() < 0.5:
            w = size[0]/10
            h = size[1]/7
            boxes.append([  x*w,    y*h,    w,  20, GREEN   ])

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
    if moveRight:
        if playerJumpAllowed():
            vel[0] -= 2*playerSpeed/60
        else:
            vel[0] -= playerSpeed/60
        if vel[0] < -playerSpeed:
            vel[0] = -playerSpeed
    elif moveLeft:
        if playerJumpAllowed():
            vel[0] += 2*playerSpeed/60
        else:
            vel[0] += playerSpeed/60
        if vel[0] > playerSpeed:
            vel[0] = playerSpeed

    # --- Jumping --- #
    if moveUp:
        vel[1] = playerJump
        moveUp = False

    # --- Gravity --- #
    vel[1] -= GRAVITY/60

    # --- Friction -- #
    if not moveLeft and not moveRight and playerJumpAllowed():  # only perform friction if player is not moving and player is on ground
        if vel[0] != 0:
            vel[0] *= FRICTION
        if vel[0] < 1/60 and vel[0] > -1/60:
            vel[0] = 0
        

    # --- Velocity Movement --- #
    player[0] -= vel[0]
    player[1] -= vel[1]

    # --- Collision --- #
    for i in range(len(boxes)):     # For every box in boxes array
        if(rectToRectCollision(player,boxes[i])):   # if player colliding with box
            N = player[1] + player[3] - boxes[i][1]     # distance between bottom of player and top of box
            E = boxes[i][0] + boxes[i][2] - player[0]   # distance between right of box and left of player
            S = boxes[i][1] + boxes[i][3] - player[1]   # distance between bottom of box and top of player
            W = player[0] + player[2] - boxes[i][0]     # distance between right of player and left of box
            # find which has smallest distance and set back player that way
            if min(N,S,E,W) == N:
                player[1] = boxes[i][1] - player[3]
                if vel[1] < 0:
                    vel[1] = 0
            elif min(E,S,W) == S:
                player[1] = boxes[i][1] + boxes[i][3]
                if vel[1] > 0:
                    vel[1] = 0
            elif (E<W):
                player[0] = boxes[i][0] + boxes[i][2]
                if vel[0] > 0:
                    vel[0] = 0
            else:
                player[0] = boxes[i][0] - player[2]
                if vel[0] < 0:
                    vel[0] = 0
    

    # --- Rendering --- #
    
    screen.fill(BLUE)

    # Draw player
    pygame.draw.rect(screen, player[4], [player[0],player[1],player[2],player[3]])

    for i in range(len(boxes)):         # Draws boxes
        pygame.draw.rect(screen, boxes[i][4], [boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])


    pygame.display.flip()
    clock.tick(60)

    
pygame.quit()   # quit game

