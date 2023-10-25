#   
#   V1.0.8.0
#   
#   + Added double jumping
#


import pygame
import random
pygame.init()

def printStats():
    print("\nplayer[0]: " + str(player[0]))
    print("player[1]: " + str(player[1]))
    print("velocity: " + str(vel))
    print("playerJumpAllowed: " + str(playerJumpAllowed()))
    print("playerLeftWallJumpAllowed: " + str(playerLeftWallJumpAllowed()))
    print("playerRightWallJumpAllowed: " + str(playerRightWallJumpAllowed()))
    print("jumpAllowed: " + str(jumpAllowed))
    print("doubleJumpAllowed: " + str(doubleJumpAllowed))
    print("doubleJump: " + str(doubleJump))
    print("inAir: " + str(inAir))
    print("\n")

def playerJumpAllowed():
    for i in range(len(boxes)):
        if ( max(player[0]+player[2],boxes[i][0]+boxes[i][2]) - min(player[0],boxes[i][0]) ) < ( player[2] + boxes[i][2] ): 
            if (player[1] + player[3]) == boxes[i][1]:
                return True
    return False

def playerLeftWallJumpAllowed():
    for i in range(len(boxes)):
        if ( max(player[1]+player[3],boxes[i][1]+boxes[i][3]) - min(player[1],boxes[i][1]) ) < ( player[3] + boxes[i][3] ): 
            if player[0] == boxes[i][0] + boxes[i][2]:
                return True
    return False

def playerRightWallJumpAllowed():
    for i in range(len(boxes)):
        if ( max(player[1]+player[3],boxes[i][1]+boxes[i][3]) - min(player[1],boxes[i][1]) ) < ( player[3] + boxes[i][3] ): 
            if player[0] + player[2] == boxes[i][0]:
                return True
    return False

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

size = (1080, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("mygame.my")
clock = pygame.time.Clock()
done = False
 
#           [x, y,  w,  h,  c]
player =    [0, 0,  50, 50, RED]
player[0] = size[0]/2 - (player[2]/2)
player[1] = size[1] - 70 - player[3]
player[1] = player[1]
vel = [0,0]
playerSpeed = 8
playerJump = 6

GRAVITY = 13      # pixels per second
FRICTION = 0.95

boxes = []
boxes.append([  0,            size[1]-50,     size[0],    50,       GREEN   ]) # Ground
boxes.append([  0,            -45,            size[0],    50,       GREEN   ])        # Roof
boxes.append([  -45,          0,              50,         size[1],  GREEN   ])        # Left wall
boxes.append([  size[0]-5,    0,              50,         size[1],  GREEN   ])  # Right wall

for x in range(0,10):
    for y in range(1,6):
        if random.random() < 0.25:
            w = size[0]/10
            h = size[1]/7
            boxes.append([  x*w,    y*h,    w,  20, GREEN   ])

jumpAllowed = False     # variable to stop repeated jumping
doubleJumpAllowed = False
doubleJump = False      # variable to enable double jumping
inAir = True            # tracks whether player was in air in the previous frame

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
            vel[0] -= playerSpeed/30
        else:
            vel[0] -= playerSpeed/(30*2)
        if vel[0] < -playerSpeed:
            vel[0] = -playerSpeed
    elif moveLeft:
        if playerJumpAllowed():
            vel[0] += playerSpeed/30
        else:
            vel[0] += playerSpeed/(30*2)
        if vel[0] > playerSpeed:
            vel[0] = playerSpeed

    # --- Jumping --- #
    jumpGround = playerJumpAllowed()
    jumpLeft = playerLeftWallJumpAllowed()
    jumpRight = playerRightWallJumpAllowed()
    jumpAny = playerJumpAllowed() or playerLeftWallJumpAllowed() or playerRightWallJumpAllowed()    # whether any jumping is allowed
    
    if not inAir and not jumpAny:   # allow double jumping if player was on ground in previous frame but not in the current frame
        doubleJump = True
    if jumpAny:         # if all of the types of jumping are not allowed, player is "inAir"
        inAir = False
    else:
        inAir = True
    
    if not moveUp:      # when player lets go of jump key
        jumpAllowed = True      # stops repeated jumping

    elif jumpAllowed:  
        if jumpGround:
            vel[1] = playerJump
            jumpAllowed = False
        elif jumpLeft:
            if vel[1] < 0:
                vel[1] = playerJump
                vel[0] = -2
                jumpAllowed = False
        elif jumpRight:
            if vel[1] < 0:
                vel[1] = playerJump
                vel[0] = 2
                jumpAllowed = False
        elif doubleJump:
            vel[1] = playerJump
            doubleJump = False
            doubleJumpAllowed = False

    # double jump if no jumping is allowed and

    # --- Gravity --- #
    vel[1] -= GRAVITY/60

    # --- Friction -- #
    if not moveLeft and not moveRight and playerJumpAllowed():  # only perform friction if player is not moving and player is on ground
        if vel[0] != 0:
            vel[0] *= FRICTION
        if vel[0] < 1/60 and vel[0] > -1/60:    # makes players velocity actually reach zero and not extremely small
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
                vel[0] *= 0.8       # slow players x velocity when player hits a roof
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

