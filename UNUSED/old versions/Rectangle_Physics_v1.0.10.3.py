#   
#   V1.0.10.4
#   
#   + Added level start and level finish with buttons
#   ~ Resized blocks to be 60x60 pixels to fit screen properly
#


import pygame
import pygame.gfxdraw
import random
pygame.init()

def printStats():
    print("\n")
    print("scene: " + scene)
    print("escape: " + str(escape))
    print("pause: " + str(pause))
    print("")
    print("player[0]: " + str(player[0]))
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

# --- Button functions --- #
def pointInsideRectangle(a, b):
    if a[0] > b[0] and a[0] < b[0] + b[2]:        # Point in rectangle on x axis
        if a[1] > b[1] and a[1] < b[1] + b[3]:    # Point in rectangle on y axis
            return True
        
def colourCorrection(rgb):      # Removes numbers >255 & <0 from rbg colour arrays
    if rgb[0] < 0:
        rgb[0] = 0
    elif rgb[0] > 255:
        rgb[0] = 255
    if rgb[1] < 0:
        rgb[1] = 0
    elif rgb[1] > 255:
        rgb[1] = 255
    if rgb[2] < 0:
        rgb[2] = 0
    elif rgb[2] > 255:
        rgb[2] = 255
    return rgb

def colourChanger(rgb, x):       # Alters all values from rbg colour arrays by a set amount
    rgb[0] = rgb[0] + x
    rgb[1] = rgb[1] + x
    rgb[2] = rgb[2] + x
    rgb = colourCorrection(rgb)
    return rgb

# --- Buttons --- #
def escape_0(req,p):   # escape: return to game
    global escape
    if req:     # if asking for requirements to draw button, return whether or not it should be drawn
        return escape
    else:       # if not asking for requirements and wanting to peform buttons action
        escape = False

def escape_1(req,p):   # escape: main menu
    global escape
    global scene
    if req:     # requirements to draw button
        return escape
    else:       # buttons actions
        escape = False
        scene = "main_menu"

def main_menu_0(req,p):   # main_menu: level selection
    global scene
    if req:     # requirements to draw button
        return scene == "main_menu"
    else:       # buttons actions
        scene = "lvl_selection"

def load_level(req,p):   # level selection: level 1
    global scene
    if req:     # requirements to draw button
        return scene == "lvl_selection"
    else:       # buttons actions
        loadLevel(p)

def level_finish_0(req,p):   # level_finish: load main menu
    global level_finish
    global scene
    if req:     # requirements to draw button
        return level_finish == True
    else:       # buttons actions
        level_finish = False
        scene = "main_menu"
        print("Returned to main menu")

def level_finish_1(req,p):   # level_finish: replay level
    global level_finish
    if req:     # requirements to draw button
        return level_finish == True
    else:       # buttons actions
        level_finish = False
        currentLevel = scene[6:len(scene)]
        loadLevel(int(currentLevel))
        print("Replaying level")

def level_finish_2(req,p):   # level_finish: next level
    global level_finish
    if req:     # requirements to draw button
        return level_finish == True
    else:       # buttons actions
        level_finish = False
        currentLevel = scene[6:len(scene)]
        loadLevel(int(currentLevel) + 1)
        print("Loaded next level")

# --- Scene function --- #
def loadLevel(n):
    print("Level " + str(n) + " was loaded.")
    resetPlayer()
    global level_start
    level_start = True
    global scene
    scene = "level_" + str(n)
    global boxes
    boxes = level[n]

def resetPlayer():
    player[0] = size[0]/2 - (player[2]/2)
    player[1] = size[1] - 70 - player[3]
    player[2] = 50
    player[3] = 50
    vel[0] = 0
    vel[1] = 0


BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
RED     = ( 255,   0,   0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)
YELLOW  = ( 255, 255,   0)
AQUA    = (   0, 255, 255)
PURPLE  = ( 255,   0, 255)


size = (1080, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("mygame.my")
clock = pygame.time.Clock()
done = False

#   main_menu, instructions, level_selection, level_(1-10), credits
scene = "main_menu"
escape = False
pause = False
level_start = False
level_finish = False
 
#           [x, y,  w,  h,  c]
player =    [0, 0,  50, 50, RED]
player[0] = size[0]/2 - (player[2]/2)
player[1] = size[1] - 70 - player[3]
vel = [0,0]
playerSpeed = 8
playerJump = 6

GRAVITY = 13      # pixels per second
FRICTION = 0.95

level = []     # MAKE ALL WIDTH/HEIGHTS DIVISIBLE BY 60 SO THAT TEXTURES CAN LINE PROPERLY (12x18 Blocks)
for i in range(10):
    level.append([])    # add ten blank levels

                #   x,          y,          width,      height, colour,         collision,  type (None,"finish","kill")
level[0].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[0].append([   360,        280,        360,        120,    GREEN,          True,       None    ])      # Middle Platform
level[0].append([   0,          180,        120,        540,    GREEN,          True,       None    ])      # Left block
level[0].append([   780,        540,        300,        120,    GREEN,          True,       None    ])      # Right step 1
level[0].append([   900,        420,        180,        120,    GREEN,          True,       None    ])      # Right step 2
level[0].append([   480,        140,        120,        120,    YELLOW,         True,       "finish"])      # Finish

level[1].append([   0,          670,        1080,       50,     GREEN,          True,       None    ])      # Ground
level[1].append([   500,        250,        350,        100,    GREEN,          True,       None    ])      # Middle Platform
level[1].append([   1080-50,    0,          50,         720,    GREEN,          True,       None    ])      # Right wall
level[1].append([   1080-300,   620,        250,        50,     GREEN,          True,       None    ])      # Right step 1
level[1].append([   1080-250,   570,        200,        50,     GREEN,          True,       None    ])      # Right step 2
level[1].append([   1080-200,   520,        150,        50,     GREEN,          True,       None    ])      # Right step 3
level[1].append([   1080-150,   470,        100,        50,     GREEN,          True,       None    ])      # Right step 4
level[1].append([   1080-100,   420,        50,         50,     GREEN,          True,       None    ])      # Right step 5

level[2].append([   0,          670,        1080,       50,     GREEN,          True,       None    ])      # Ground
level[2].append([   360,        250,        350,        100,    GREEN,          True,       None    ])      # Middle Platform

level[3].append([   0,          size[1]-50, size[0],    50,     (0,  255,0),    True,       None    ])      # Ground
level[4].append([   0,          size[1]-50, size[0],    50,     (40, 255,40),   True,       None    ])      # Ground
level[5].append([   0,          size[1]-50, size[0],    50,     (80, 255,80),   True,       None    ])      # Ground
level[6].append([   0,          size[1]-50, size[0],    50,     (120,255,120),  True,       None    ])      # Ground
level[7].append([   0,          size[1]-50, size[0],    50,     (160,255,160),  True,       None    ])      # Ground
level[8].append([   0,          size[1]-50, size[0],    50,     (200,255,200),  True,       None    ])      # Ground
level[9].append([   0,          size[1]-50, size[0],    50,     (240,255,240),  True,       None    ])      # Ground


boxes = []      # layout of the current level


jumpAllowed = False         # variable to stop repeated jumping
doubleJumpAllowed = False
doubleJump = False          # variable to enable double jumping
inAir = True                # tracks whether player was in air in the previous frame

moveUp = False
moveRight = False
moveLeft = False

mouseDown = False
buttons = []    #   x,      y,      width,  height, colour,             pressed,    functionName,   parameters
buttons.append([    390,    200,    300,    100,    (200,200,200),      False,      "escape_0",     None])      # escape: return to game
buttons.append([    390,    400,    300,    100,    (200,200,200),      False,      "escape_1",     None])      # escape: load main_menu
buttons.append([    340,    200,    400,    100,    (200,200,200),      False,      "main_menu_0",  None])      # main_menu: load level_selection
for i in range(5):
    buttons.append([    140 + (175*i),    200,    100,    100,    (200,200,200),      False,    "load_level",   i])     # level_selection: load level_"i"
for i in range(5):
    buttons.append([    140 + (175*i),    400,    100,    100,    (200,200,200),      False,    "load_level",   i+5])     # level_selection: load level_"i"
buttons.append([    300,    500,    100,    100,    (200,200,200),      False,      "level_finish_0",None])     # level_finish: load main_menu
buttons.append([    490,    500,    100,    100,    (200,200,200),      False,      "level_finish_1",None])     # level_finish: replay level
buttons.append([    680,    500,    100,    100,    (200,200,200),      False,      "level_finish_2",None])     # level_finish: next level


print("Welcome to rectangle thingy with: ")
print("  - Left/Right Movement")
print("  - Jumping")
print("  - Gravity")
print("  - Collision with other rectangles")

 
# -------- Main Program Loop -----------
while not done:
    ## MAIN EVENT LOOP ##
    mousePos = pygame.mouse.get_pos()
    
    # --- User Input --- #
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
            elif event.key == pygame.K_ESCAPE:
                if "level" in scene and not level_start:     # only open escape menu if in a level and not level_start
                    if escape:
                        escape = False
                    else:
                        escape = True
            elif event.key == pygame.K_SPACE:
                level_start = False
            elif event.key == pygame.K_s:
                printStats()
            elif event.key == pygame.K_m:
                escape = False
                scene = "main_menu"
            elif event.key == pygame.K_1:
                loadLevel(0)
            elif event.key == pygame.K_2:
                loadLevel(1)
            elif event.key == pygame.K_3:
                loadLevel(2)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                moveUp = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
        # -- Button stuff -- #
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouseDown == False:
                for i in range(len(buttons)):
                    if pointInsideRectangle(mousePos,buttons[i]):
                        if globals()[buttons[i][6]](True, buttons[i][7]):      # if button is being drawn
                            buttons[i][5] = True    # button is being pressed
            mouseDown = True
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if mouseDown == True:
                for i in range(len(buttons)):
                    if pointInsideRectangle(mousePos,buttons[i]):
                        if buttons[i][5] == True:
                            if globals()[buttons[i][6]](True, buttons[i][7]):      # if button is being drawn
                                print("Button " + str(buttons[i][6]) + " has been pressed", end="")
                                if buttons[i][7] != None:
                                    print(" with parameter " + str(buttons[i][7]))
                                else:
                                    print("")
                                globals()[buttons[i][6]](False, buttons[i][7])     # peform buttons actions
                    buttons[i][5] = False
            mouseDown = False

    if scene == "main_menu":
        # --- Rendering --- #
        screen.fill((127,127,127))

    elif scene == "lvl_selection":
        # --- Rendering --- #
        screen.fill((127,127,127))
        
    
    elif "level" in scene:    # if current scene is a level
        if escape or level_start or level_finish:
            pause = True
        else:
            pause = False
        if not pause:      # only peform player movement if not paused
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
                doubleJumpAllowed = True
            if jumpAny:             # if all of the types of jumping are not allowed, player is "inAir"
                inAir = False
            else:
                inAir = True
            if doubleJumpAllowed and not moveUp:    # if double jumping is allowed and player lets go of jump key 
                doubleJumpAllowed = False   
                doubleJump = True
            
            if not moveUp:
                if jumpAny:
                    jumpAllowed = True      # stops repeated jumping

            else:
                if jumpAllowed:  
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
                if doubleJump:
                    vel[1] = playerJump
                    doubleJump = False        
            # --- Rendering --- #
            
            screen.fill(BLUE)

            pygame.draw.rect(screen, player[4], [player[0],player[1],player[2],player[3]])      # Draw player 

            for i in range(len(boxes)):
                pygame.draw.rect(screen, boxes[i][4], [boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])    # Draw boxes


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
                if(boxes[i][5]):    # if boxes collision is true
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

                        if boxes[i][6] == "finish":
                            level_finish = True
                        elif boxes[i][6] == "kill":
                            print("Player Died")
                            resetPlayer()

            # --- Outside Map Reset --- #
            if player[0] + player[2] < 0:   # left side
                resetPlayer()
            elif player[0] > size[0]:       # right side
                resetPlayer()
            elif player[1] > size[1]:       # bottom of map
                resetPlayer()
        
        
        # --- Rendering --- #
        
        screen.fill(BLUE)

        for i in range(len(boxes)):
            pygame.draw.rect(screen, boxes[i][4], [boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])    # Draw boxes

        pygame.draw.rect(screen, player[4], [player[0],player[1],player[2],player[3]])      # Draw player after boxes to allow for boxes without collision


        if escape:      # render transparent escape screen
            MARGIN = 40
            pygame.gfxdraw.box(screen, pygame.Rect(MARGIN,MARGIN,size[0]-(2*MARGIN),size[1]-(2*MARGIN)), (15,15,15,191))

        if level_start:
            pygame.gfxdraw.box(screen, pygame.Rect(200,525,680,100), (15,15,15,191))

        if level_finish:
            MARGIN = 80
            pygame.gfxdraw.box(screen, pygame.Rect(MARGIN,MARGIN,size[0]-(2*MARGIN),size[1]-(2*MARGIN)), (15,15,15,191))

    # render buttons regardless of what scene
    for i in range(len(buttons)):   # Draws buttons
        buttonColour = [ buttons[i][4][0], buttons[i][4][1], buttons[i][4][2]]
        if buttons[i][5]:
            buttonColour = colourChanger(buttonColour, -63)    # Changes colour if player is pressing
        if globals()[buttons[i][6]](True,buttons[i][7]):  # draw button if requirements are met
            pygame.draw.rect(screen, buttonColour, [buttons[i][0],buttons[i][1],buttons[i][2],buttons[i][3]])
        
    pygame.display.flip()
    clock.tick(60)

pygame.quit()   # quit game

