#   
#   V1.0.14
#   
#   + Added instruction text
#

import os
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
        click_sound.play()

def escape_1(req,p):   # escape: main menu
    global escape
    global scene
    if req:     # requirements to draw button
        return escape
    else:       # buttons actions
        escape = False
        scene = "main_menu"
        click_sound.play()

def main_menu_0(req,p):   # main_menu: level selection
    global scene
    if req:     # requirements to draw button
        return scene == "main_menu"
    else:       # buttons actions
        scene = "lvl_selection"
        click_sound.play()

def main_menu_1(req,p):   # main_menu: level selection
    global scene
    if req:     # requirements to draw button
        return scene == "main_menu"
    else:       # buttons actions
        scene = "instructions"
        click_sound.play()

def load_level(req,p):   # level selection: level 1
    global scene
    if req:     # requirements to draw button
        return scene == "lvl_selection"
    else:       # buttons actions
        loadLevel(p)
        click_sound.play()

def back_arrow(req,p):   # load main menu
    global scene
    if req:     # requirements to draw button
        return scene == "lvl_selection" or scene == "instructions"
    else:       # buttons actions
        scene = "main_menu"
        click_sound.play()
        

def lvl_finish_0(req,p):   # lvl_finish: load main menu
    global lvl_finish
    global scene
    if req:     # requirements to draw button
        return lvl_finish == True
    else:       # buttons actions
        lvl_finish = False
        scene = "main_menu"
        print("Returned to main menu")
        click_sound.play()

def lvl_finish_1(req,p):   # lvl_finish: replay level
    global lvl_finish
    if req:     # requirements to draw button
        return lvl_finish == True
    else:       # buttons actions
        lvl_finish = False
        currentLevel = scene[6:len(scene)]
        loadLevel(int(currentLevel))
        print("Replaying level")
        click_sound.play()

def lvl_finish_2(req,p):   # lvl_finish: next level
    global lvl_finish
    global scene
    if req:     # requirements to draw button
        return lvl_finish == True
    else:       # buttons actions
        currentLevel = int(scene[6:len(scene)])
        if records[currentLevel] <= star_times[currentLevel][2]:
            lvl_finish = False
            loadLevel(currentLevel + 1)
            print("Loaded next level")
        click_sound.play()

# --- Scene function --- #
def loadLevel(n):
    if n == 0 or (records[n-1] != None and records[n-1] <= star_times[n-1][2]):
        print("Level " + str(n) + " was loaded.")
        resetPlayer()
        global lvl_start
        lvl_start = True
        global scene
        scene = "level_" + str(n)
        global boxes
        boxes = level[n]
        global lvl_timer
        lvl_timer = 0
        global lvl_timer_on
        lvl_timer_on = False

def resetPlayer():
    player[0] = size[0]/2 - (player[2]/2)
    player[1] = size[1] - 70 - player[3]
    player[2] = 50
    player[3] = 50
    vel[0] = 0
    vel[1] = 0

def submitLevelTime(time,level):
    global records
    if records[level] == None or records[level] > time:
        records[level] = time

def createImage(name,w,h):
    img = pygame.image.load(name)
    img = pygame.transform.scale(img,(w,h))
    return img

def centreTextX(label,rect):
    textPos = label.get_rect()  # get rectangle the text fits into
    textPos[0] = centreRectX(textPos,rect)
    return textPos[0]      # return x coord of text

def centreRectX(rect1,rect2):   # return the x coord of rect1 for it to be centered in rect2
    return rect2[0] + (rect2[2]/2) - (rect1[2]/2)

def drawCenteredText(txt,colour,font,yCoord,rect):
    label = font.render(txt, 1, colour)
    label_pos = [centreTextX(label,rect), yCoord]
    screen.blit(label, label_pos)

def drawStar(level_No,rect):
    global lvl_timer
    star_txt = ""
    if records[level_No] <= star_times[level_No][0]:     # player got gold
        screen.blit(gold_star_img, (centreRectX([0,0,128,128],box),280))
        star_txt = "You have recieved a Gold Star in this level!"
    elif records[level_No] <= star_times[level_No][1]:   # player got silver
        screen.blit(silver_star_img, (centreRectX([0,0,128,128],box),280))
        star_txt = "Score a time of at least " + str(round(star_times[level_No][0]/1000,3)) + " seconds to be awarded a Gold Star."
    elif records[level_No] <= star_times[level_No][2]:   # player got bronze
        screen.blit(bronze_star_img, (centreRectX([0,0,128,128],box),280))
        star_txt = "Score a time of at least " + str(round(star_times[level_No][1]/1000,3)) + " seconds to be awarded a Silver Star."
    else:
        screen.blit(none_star_img, (centreRectX([0,0,128,128],box),280))
        star_txt = "Score a time of at least " + str(round(star_times[level_No][2]/1000,3)) + " seconds to be awarded a Bronze Star."
    drawCenteredText(star_txt,AQUA,font0,440,rect)
        

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

# --- Image Definition --- #
tile_img = createImage("grey_tile.png",60,60)
finish_img = createImage("finish.png",60,60)
player_img = createImage("player.png",50,50)
background_img = createImage("cave_background.png",1080,720)
button_mainmenu_img = createImage("button_mainmenu.png",100,100)
button_replay_img = createImage("button_replay.png",100,100)
button_nextlvl_img = createImage("button_nextlvl.png",100,100)
button_back_img = createImage("button_back.png",100,50)

none_star_img = createImage("star_none.png",128,128)
bronze_star_img = createImage("star_bronze.png",128,128)
silver_star_img = createImage("star_silver.png",128,128)
gold_star_img = createImage("star_gold.png",128,128)
none_star_small_img = createImage("star_none.png",30,30)
bronze_star_small_img = createImage("star_bronze.png",30,30)
silver_star_small_img = createImage("star_silver.png",30,30)
gold_star_small_img = createImage("star_gold.png",30,30)
lock_small_img = createImage("lock.png",30,30)

font0 = pygame.font.Font(None, 36)
font1 = pygame.font.Font(None, 72)
font2 = pygame.font.Font(None, 90)
font3 = pygame.font.Font(None, 45)
font4 = pygame.font.Font(None, 60)

# --- Text Definition --- #
level_completed_txt = font2.render("Level Completed!", 1, AQUA)
level_completed_pos = [centreTextX(level_completed_txt,[80,80,920,560]) ,110]

start_level_txt = font3.render("Press SPACEBAR to begin...", 1, AQUA)
start_level_pos = [centreTextX(start_level_txt,[200,475,680,150]) ,575]

pygame.mixer.music.load('sound/background_music.wav')
pygame.mixer.music.play(-1)

jump_sound = pygame.mixer.Sound('sound/jump_effect.wav')
walljump_sound = pygame.mixer.Sound('sound/walljump_effect.wav')
doublejump_sound = pygame.mixer.Sound('sound/doublejump_effect.wav')
die_sound = pygame.mixer.Sound('sound/die_effect.wav')
click_sound = pygame.mixer.Sound('sound/click_effect.wav')
welcome_sound = pygame.mixer.Sound('sound/welcome_effect.wav')
levelcompleted_sound = pygame.mixer.Sound('sound/levelcompleted_effect.wav')

welcome_sound.play()

scene = "main_menu"
escape = False
pause = False
lvl_start = False
lvl_finish = False
lvl_timer_on = False
lvl_timer = 0
 
#           [x, y,  w,  h,  c]
player =    [0, 0,  50, 50, RED]
player[0] = size[0]/2 - (player[2]/2)
player[1] = size[1] - 70 - player[3]
vel = [0,0]
playerSpeed = 8
playerJump = 6

GRAVITY = 13      # pixels per second
FRICTION = 0.95

records = []
star_times = [
    [2850,3100,3500],
    [4000,5000,6000],
    [4000,5000,6000],
    [4000,5000,6000],
    [4000,5000,6000],
    [4000,5000,6000],
    [4000,5000,6000],
    [4000,5000,6000],
    [4000,5000,6000],
    [4000,5000,6000]
]
level = []     #   Common factors of 1080 and 720 are: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120, 180, 360 
level_No = 0
for i in range(10):
    level.append([])    # add ten blank levels
    records.append(None)  # add ten blank records

                #   x,          y,          width,      height, colour,         collision,  type (None,"finish","kill")
level[0].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[0].append([   360,        280,        360,        120,    GREEN,          True,       None    ])      # Middle Platform
level[0].append([   0,          180,        120,        540,    GREEN,          True,       None    ])      # Left block
level[0].append([   780,        540,        300,        120,    GREEN,          True,       None    ])      # Right step 1
level[0].append([   900,        420,        180,        120,    GREEN,          True,       None    ])      # Right step 2
level[0].append([   510,        140,        60,        120,     YELLOW,         True,       "finish"])      # Finish

level[1].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[1].append([   420,        240,        360,        60,     GREEN,          True,       None    ])      # Middle Platform 1
level[1].append([   360,        300,        360,        60,     GREEN,          True,       None    ])      # Middle Platform 2
level[1].append([   300,        360,        360,        60,     GREEN,          True,       None    ])      # Middle Platform 3
level[1].append([   1080-60,      0,         60,       720,     GREEN,          True,       None    ])      # Right wall
level[1].append([   1080-300,   600,        240,        60,     GREEN,          True,       None    ])      # Right step 1
level[1].append([   1080-240,   540,        180,        60,     GREEN,          True,       None    ])      # Right step 2
level[1].append([   1080-180,   480,        120,        60,     GREEN,          True,       None    ])      # Right step 3
level[1].append([   1080-120,   420,         60,        60,     GREEN,          True,       None    ])      # Right step 4
level[1].append([   1080-360,     0,        360,        60,     GREEN,          True,       None    ])      # Right roof 1
level[1].append([   1080-240,    60,        240,        60,     GREEN,          True,       None    ])      # Right roof 2
level[1].append([   1080-120,   120,        120,        60,     GREEN,          True,       None    ])      # Right roof 2
level[1].append([   450,        100,         60,       120,     YELLOW,         True,       "finish"])      # Finish

level[2].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[2].append([   600,        480,        60,         180,    GREEN,          True,       None    ])      # Right wall next to player
level[2].append([   180,        480,        420,        60,     GREEN,          True,       None    ])      # Roof above player
level[2].append([   180,        300,        60,         180,    GREEN,          True,       None    ])      # Left wall
level[2].append([   180,        180,        720,        120,    GREEN,          True,       None    ])      # Roof 2 above player
level[2].append([   840,        300,        60,         240,    GREEN,          True,       None    ])      # Right wall
level[2].append([   270,        340,        60,         120,    YELLOW,         True,       "finish"])      # Finish

level[3].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[4].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[5].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[6].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[7].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[8].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground
level[9].append([   0,          660,        1080,       60,     GREEN,          True,       None    ])      # Ground


boxes = []      # layout of the current level


jumpAllowed = False         # variable to stop repeated jumping
doubleJumpAllowed = False
doubleJump = False          # variable to enable double jumping
inAir = True                # tracks whether player was in air in the previous frame

moveUp = False
moveRight = False
moveLeft = False

mouseDown = False
buttons = []    #   x,      y,      width,  height, colour,         pressed,    functionName,   parameters, image,  text
buttons.append([    340,    200,    400,    100,    (200,200,200),  False,      "escape_0",         None,   None,   "Return to Game"    ])      # escape: return to game
buttons.append([    390,    400,    300,    100,    (200,200,200),  False,      "escape_1",         None,   None,   "Main Menu"         ])      # escape: load main_menu
buttons.append([    340,    300,    400,    100,    (200,200,200),  False,      "main_menu_0",      None,   None,   "Select Level"      ])      # main_menu: load level_selection
buttons.append([    340,    450,    400,    100,    (200,200,200),  False,      "main_menu_1",      None,   None,   "How to play"       ])      # main_menu: load instructions
for i in range(5):
    buttons.append([    140 + (175*i),    200,    100,    100,    (220,220,220),      False,    "load_level",   i,      None,   str(i+1)])      # level_selection: load level_"i"
for i in range(5):
    buttons.append([    140 + (175*i),    370,    100,    100,    (220,220,220),      False,    "load_level",   i+5,    None,   str(i+6)])      # level_selection: load level_"i"
buttons.append([    50,     50,     100,    50,    (200,200,200),   False,      "back_arrow",       None,   button_back_img,        None])      # level_selection/instructions: load main_menu

buttons.append([    300,    500,    100,    100,    (200,200,200),  False,      "lvl_finish_0",     None,   button_mainmenu_img,    None])      # lvl_finish: load main_menu
buttons.append([    490,    500,    100,    100,    (200,200,200),  False,      "lvl_finish_1",     None,   button_replay_img,      None])      # lvl_finish: replay level
buttons.append([    680,    500,    100,    100,    (200,200,200),  False,      "lvl_finish_2",     None,   button_nextlvl_img,     None])      # lvl_finish: next level


print("Welcome to rectangle thingy with: ")
print("  - Left/Right Movement")
print("  - Jumping")
print("  - Gravity")
print("  - Collision with other rectangles")

 
# -------- Main Program Loop -----------
while not done:
    ## MAIN EVENT LOOP ##
    mousePos = pygame.mouse.get_pos()
    if "level" in scene:
        level_No = int(scene[6:len(scene)])
    
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
                if escape:
                    escape = False
                    lvl_timer_on = True
                elif "level" in scene and not lvl_finish:  # only open escape menu if playing a level:
                    escape = True
                    lvl_timer_on = False
            elif event.key == pygame.K_SPACE:
                if lvl_start:
                    lvl_start = False
                    lvl_timer_on = True

##            # extra keydowns
##            elif event.key == pygame.K_s:
##                printStats()
##            elif event.key == pygame.K_r:
##                if lvl_finish_1(True,None):
##                    lvl_finish_1(False,None)
##                else:
##                    loadLevel(level_No)
##            elif event.key == pygame.K_m:
##                scene = "main_menu"
##            elif event.key == pygame.K_1:
##                loadLevel(0)
##            elif event.key == pygame.K_2:
##                loadLevel(1)
                
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

    elif scene == "instructions":
        # --- Rendering --- #
        screen.fill((127,127,127))
        instructions1_txt = "Instructions:"
        drawCenteredText(instructions1_txt,AQUA,font2,70,[0,0,1080,720])
        instructions2_txt = "Up arrow key to Jump"
        drawCenteredText(instructions2_txt,YELLOW,font3,250,[0,0,1080,720])
        instructions2_txt = "Left/Right arrow keys for left/right movement"
        drawCenteredText(instructions2_txt,YELLOW,font3,325,[0,0,1080,720])
        instructions2_txt = "ESCAPE to pause game AND/OR return to main menu"
        drawCenteredText(instructions2_txt,YELLOW,font3,400,[0,0,1080,720])
        instructions2_txt = "Aim: Complete all the levels as fast as possible!"
        drawCenteredText(instructions2_txt,GREEN,font3,550,[0,0,1080,720])
        
    
    elif "level" in scene:    # if current scene is a level
        if escape or lvl_start or lvl_finish:
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
                        jump_sound.play()
                    elif jumpLeft:
                        if vel[1] < 0:
                            vel[1] = playerJump
                            vel[0] = -2
                            jumpAllowed = False
                            walljump_sound.play()
                    elif jumpRight:
                        if vel[1] < 0:
                            vel[1] = playerJump
                            vel[0] = 2
                            jumpAllowed = False
                            walljump_sound.play()
                if doubleJump:
                    vel[1] = playerJump
                    doubleJump = False
                    doublejump_sound.play()
                    
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
                            print("Level Completed")
                            levelcompleted_sound.play()
                            lvl_finish = True
                            lvl_timer_on = False
                            submitLevelTime(int(lvl_timer),level_No)
                        elif boxes[i][6] == "kill":
                            print("Player Died")
                            die_sound.play()
                            loadLevel(level_No)

            # --- Outside Map Reset --- #
            if player[0] + player[2] < 0 or player[0] > size[0] or player[1] > size[1]:
                print("Player went outside the map.")
                die_sound.play()
                loadLevel(level_No)
        
        
        # --- Rendering --- #
        
        screen.fill(BLUE)
        screen.blit(background_img, (0,0))

        for i in range(len(boxes)):
            pygame.draw.rect(screen, boxes[i][4], [boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]])    # Draw boxes
            wR = boxes[i][2]/60
            hR = boxes[i][3]/60
            for w in range(int(wR)):
                for h in range(int(hR)):
                    if boxes[i][6] == None:
                        screen.blit(tile_img, (boxes[i][0]+(60*w), boxes[i][1]+(60*h)))
                    elif boxes[i][6] == "finish":
                        screen.blit(finish_img, (boxes[i][0]+(60*w), boxes[i][1]+(60*h)))

                            
                        

        #pygame.draw.rect(screen, player[4], [player[0],player[1],player[2],player[3]])
        screen.blit(player_img, (player[0],player[1]))       # Draw player after boxes to allow for boxes without collision

        if escape:      # render transparent escape screen
            MARGIN = 40
            pygame.gfxdraw.box(screen, pygame.Rect(MARGIN,MARGIN,size[0]-(2*MARGIN),size[1]-(2*MARGIN)), (15,15,15,191))

        if lvl_start:
            pygame.gfxdraw.box(screen, pygame.Rect(200,475,680,150), (15,15,15,191))
            screen.blit(start_level_txt, start_level_pos)
            level_txt = "Level " + str(level_No+1)
            drawCenteredText(level_txt,AQUA,font1,490,[200,475,680,150])

        if lvl_finish:
            box = (80,80,920,560)
            pygame.gfxdraw.box(screen, pygame.Rect(box), (15,15,15,191))
            #image
            drawStar(level_No,box)
            #text
            screen.blit(level_completed_txt, level_completed_pos)
            timer_txt = "Time taken: " + str(lvl_timer/1000) + " seconds"
            drawCenteredText(timer_txt,AQUA,font0,200,box)
            record_txt = "Level record: " + str(records[level_No]/1000) + " seconds"
            drawCenteredText(record_txt,AQUA,font0,240,box)

    # render buttons regardless of what scene
    for i in range(len(buttons)):   # Draws buttons
        buttonColour = [ buttons[i][4][0], buttons[i][4][1], buttons[i][4][2]]
        if buttons[i][5]:
            buttonColour = colourChanger(buttonColour, -63)    # Changes colour if player is pressing
        if globals()[buttons[i][6]](True,buttons[i][7]):  # draw button if requirements are met
            buttonRect = [buttons[i][0],buttons[i][1],buttons[i][2],buttons[i][3]]
            pygame.draw.rect(screen, buttonColour, buttonRect)
            if buttons[i][8] != None:
                screen.blit(buttons[i][8], (buttons[i][0], buttons[i][1]))
            if buttons[i][9] != None:
                drawCenteredText(buttons[i][9],BLUE,font1,buttons[i][1]+20,buttonRect)

    # render stars in bottom corner of levels
    if scene == "lvl_selection":
        for i in range(5):
            if records[i] != None:
                if records[i] <= star_times[i][0]:
                    screen.blit(gold_star_small_img, (205+(i*175),265))
                elif records[i] <= star_times[i][1]:
                    screen.blit(silver_star_small_img, (205+(i*175),265))
                elif records[i] <= star_times[i][2]:
                    screen.blit(bronze_star_small_img, (205+(i*175),265))
            else:
                if i != 0 and (records[i-1] == None or records[i-1] > star_times[i-1][2]):
                    screen.blit(lock_small_img, (205+(i*175),265))
        for i in range(5,10):
            if records[i] != None:
                if records[i] <= star_times[i][0]:
                    screen.blit(gold_star_small_img, (205+((i-5)*175),435))
                elif records[i] <= star_times[i][1]:
                    screen.blit(silver_star_small_img, (205+((i-5)*175),435))
                elif records[i] <= star_times[i][2]:
                    screen.blit(bronze_star_small_img, (205+((i-5)*175),435))
            else:
                if records[i-1] == None or records[i-1] > star_times[i-1][2]:
                    screen.blit(lock_small_img, (205+((i-5)*175),435))

    if lvl_finish and records[level_No] > star_times[level_No][2]:
        screen.blit(lock_small_img, (745,565))

    # render text
    if "level" in scene:
        pygame.gfxdraw.box(screen, pygame.Rect(10,5,260,36), (15,15,15,127))
        lvl_timer_text = font0.render("Time: " + str(round(lvl_timer/1000,3)) + " seconds", 1, WHITE)
        screen.blit(lvl_timer_text, (20,10))

        
    pygame.display.flip()
    if lvl_timer_on:
        lvl_timer += clock.get_time()
    clock.tick(60)

pygame.quit()   # quit game

