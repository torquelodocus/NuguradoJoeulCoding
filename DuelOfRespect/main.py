import pygame
import os
from time import sleep as tsleep
pygame.font.init()
pygame.mixer.init()


# DISPLAY SETTINGS;
WIDTH, HEIGHT = 1680, 1050
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# PLAYER DATA;
PLAYER_WIDTH = 100
PlAYER_HEIGHT = 100
PLAYER_VELOCITY = 12
JUMP_VELOCITY = 25
PLAYER_YELLOW_HEALTH = 5
PLAYER_RED_HEALTH = 5
CENTER_PLAYER_PLACEMENT_WIDTH = (WIDTH//2)-(PLAYER_WIDTH//2)
CENTER_PLAYER_PLACEMENT_HEIGHT = 100
STANDARD_PER_ROUND_HEALTH = 20
YELLOW_PEROUND_HEALTH = STANDARD_PER_ROUND_HEALTH
RED_PEROUND_HEALTH = STANDARD_PER_ROUND_HEALTH
YELLOW_FACING = "right"
RED_FACING = "left"
STANDARD_BULLET_COUNT = 30
YELLOW_BULLET_COUNT = STANDARD_BULLET_COUNT
RED_BULLET_COUNT = STANDARD_BULLET_COUNT

# IMAGE LOADERS;
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Photos", "Fighter_Game_BG.png")), (WIDTH, HEIGHT))

# GAME SETTINGS;
GRAVITY = 5
MAX_FPS = 60
BULLET_VELOCITY = 100 #40
GUN_KNOCKBACK_HORIZONTAL = 50
GUN_KNOCKBACK_VERTICAL = 30 #100

# MAP VALUES;
SMALL_MAP_RECTS_SIZE_WIDTH = 350
SMALL_MAP_RECTS_SIZE_HEIGHT = 30
LEFT_BOTTOM_RECT = pygame.Rect(100, 750, SMALL_MAP_RECTS_SIZE_WIDTH, SMALL_MAP_RECTS_SIZE_HEIGHT)
RIGHT_BOTTOM_RECT = pygame.Rect(WIDTH-(SMALL_MAP_RECTS_SIZE_WIDTH+100), 750, SMALL_MAP_RECTS_SIZE_WIDTH, SMALL_MAP_RECTS_SIZE_HEIGHT)
CENTER_BOTTOM_RECT = pygame.Rect(WIDTH//2-(SMALL_MAP_RECTS_SIZE_WIDTH//2), 750, SMALL_MAP_RECTS_SIZE_WIDTH, SMALL_MAP_RECTS_SIZE_HEIGHT)

# COLORS;
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (252, 161, 3)

# Called whenever a heart is lost,
# Takes the name of the heart-looser as a string and verbally says "player has died";
def playLostHeartAUDIO(whoDied):
    if whoDied == "red":
        pygame.mixer.music.load(os.path.join("Audio", "red_has_died.mp3"))
    else:
        pygame.mixer.music.load(os.path.join("Audio", "yellow_has_died.mp3"))
    pygame.mixer.music.play()


# Checks The map-rectangles for horizontal player collision;
# Takes the playerToCheck as a parameter (eg: red, yellow);
# If the player doesn't collide returns True, if the player does collide with any rectangle it returns a False;
# This way the lower-movements or gravity know which places to check vertically too for, so based of of that,
# the player is either eligible to sink-lower or not;
def mapRectHorizontalDetection(playerToCheck):
    if playerToCheck.x < LEFT_BOTTOM_RECT.x - (PLAYER_WIDTH//2) or playerToCheck.x > LEFT_BOTTOM_RECT.x + (LEFT_BOTTOM_RECT.width - (PLAYER_WIDTH//2)):
        if playerToCheck.x < CENTER_BOTTOM_RECT.x - (PLAYER_WIDTH//2) or playerToCheck.x > CENTER_BOTTOM_RECT.x + (CENTER_BOTTOM_RECT.width - (PLAYER_WIDTH//2)):
            if playerToCheck.x < RIGHT_BOTTOM_RECT.x - (PLAYER_WIDTH//2) or playerToCheck.x > RIGHT_BOTTOM_RECT.x + (RIGHT_BOTTOM_RECT.width - (PLAYER_WIDTH//2)):
                return True
                # NOTE: If I were working on a larger project, I would've written this part recursively so that i would be able to
                # Create as many platforms as I want without hardcoding the values;
                # But as this is a REALLY SMALL project AND i started learning pygame only 2 days ago i decided I will just write it like this;
            else:
                return False           
        else:
            return False
    else:
        return False   
    
# If the player doesn't collide with any rectangle vertically, retturns True;
# Otherwise, returns False;
# This function is needed for movement/physics blocking places (eg: platforms);
def mapRectVerticalDetection(playerToCheck):
    if playerToCheck.y < (LEFT_BOTTOM_RECT.y-playerToCheck.height) or playerToCheck.y > ((LEFT_BOTTOM_RECT.y+LEFT_BOTTOM_RECT.height)-PlAYER_HEIGHT):
        return True
    else:
        return False

# Moves the yellow player;
# Takes the pressed keys of the desired character and runs code based off of that;
def move_player_yellow(keys_pressed, yellow):
    global YELLOW_FACING
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= JUMP_VELOCITY
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        YELLOW_FACING = "left"
        yellow.x -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_s]:
        # Checking if the user collides with a platform, so if it does, not allowing the user to sink down anymore;
        if not(mapRectHorizontalDetection(yellow)):
            if mapRectVerticalDetection(yellow):
                yellow.y += PLAYER_VELOCITY
        else:
            yellow.y += PLAYER_VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x < WIDTH - PLAYER_WIDTH:
        YELLOW_FACING = "right"
        yellow.x += PLAYER_VELOCITY

# Moves the red player
def move_player_red(keys_pressed, red):
    global RED_FACING
    if keys_pressed[pygame.K_UP] and red.y > 0:
        red.y -= JUMP_VELOCITY
    if keys_pressed[pygame.K_LEFT] and red.x > 0:
        RED_FACING = "left"
        red.x -= PLAYER_VELOCITY
    if keys_pressed[pygame.K_DOWN]:
        # Checking if the user collides with a platform, so if it does, not allowing the user to sink down anymore;
        if not(mapRectHorizontalDetection(red)):
            if mapRectVerticalDetection(red):
                red.y += PLAYER_VELOCITY
        else:
            red.y += PLAYER_VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x < WIDTH - PLAYER_WIDTH:
        RED_FACING = "right"
        red.x += PLAYER_VELOCITY

# This function is responsible for keeping the players from floating;
# Function takes playerToCheck as a parameter, the parameter is the desired player;
# The function then checks if the player is elligible for being lowered via a collision detection;
# If the player is eligible, the player gets lowered by the game gravity count;
def lowerPlayersByGravityF(playerToCheck):
    if not(mapRectHorizontalDetection(playerToCheck)):
        if mapRectVerticalDetection(playerToCheck):
                playerToCheck.y += GRAVITY
    else:
        playerToCheck.y += GRAVITY

# Takes the object of the player and the players name in a string form;
# Checks if the player is lower than the game height, if it is, the player gets respawned and looses one heart;
def checkIfPlayerDead(deadPlayer, deadPlayerSpeaker):
    global PLAYER_RED_HEALTH, PLAYER_YELLOW_HEALTH
    if deadPlayer.y + deadPlayer.height > HEIGHT:
        playLostHeartAUDIO(deadPlayerSpeaker)
        deadPlayer.x = CENTER_PLAYER_PLACEMENT_WIDTH
        deadPlayer.y = CENTER_PLAYER_PLACEMENT_HEIGHT
        if deadPlayerSpeaker == "red":
            PLAYER_RED_HEALTH-=1
        else:
            PLAYER_YELLOW_HEALTH-=1
        checkIfWinF()

# Called when a player is hit with a gun, post a collision detection return;
# Parameter is just a string value of the player that has been hit,
# Based off of who the hit player is, the hit player looses one per-round-health, which if gets to 0 causes the player to loose one heart;
def player_hit_with_gun(hitPlayer):
    global RED_PEROUND_HEALTH, YELLOW_PEROUND_HEALTH
    if hitPlayer == "red":
        RED_PEROUND_HEALTH-=1
    else:
        YELLOW_PEROUND_HEALTH-=1

# This function is called if a win is confirmed, Game freezes and the winner gets displayed on the screen; 
def actualWinF(whoWon):
    WIN.blit(pygame.font.SysFont('Comic Sans MS', 80).render(whoWon + " HAS WON THE GAME!", 1, RED), (200, 400))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

# Checks if the health of both players are 0, otherwise calls the actualWinF() with the username/display_name as the parameter; 
def checkIfWinF():
    if PLAYER_RED_HEALTH <= 0:
        actualWinF("PLAYER 1")
    if PLAYER_YELLOW_HEALTH <= 0:
        actualWinF("PLAYER 2")
        
# If a player looses all their per_round_health, this function is called with the players object in the parameters;
# Then the player is placed far low in the screen which causes the death of the player due to the other bottom-killzone functions;
def killPlayer(playerToKill):
    playerToKill.y = 2000

# Checks if all per_round_health of the desired player is over 0, if it isnt, the player gets killed;
def checkIfAllHeartsGone(playerToCheck, playerName):
    global RED_PEROUND_HEALTH, YELLOW_PEROUND_HEALTH, STANDARD_PER_ROUND_HEALTH
    if playerName == "red":
        if RED_PEROUND_HEALTH <= 0:
            killPlayer(playerToCheck)
            RED_PEROUND_HEALTH=STANDARD_PER_ROUND_HEALTH
    else:
        if YELLOW_PEROUND_HEALTH <= 0:
            killPlayer(playerToCheck)
            YELLOW_PEROUND_HEALTH=STANDARD_PER_ROUND_HEALTH

# This is used to display the health-bar with a valid color;
# username as a string is given to the function;
# based off of the name, the health is checked and the proper display color is returned;
def getValidHealthColorF(playerToCheck):
    if playerToCheck == "red":
        if RED_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//1.5:
            return GREEN
        elif RED_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//4:
            return ORANGE
        else:
            return RED
    else:
        if YELLOW_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//2:
            return GREEN
        elif YELLOW_PEROUND_HEALTH > STANDARD_PER_ROUND_HEALTH//4:
            return ORANGE
        else:
            return RED

# Rerenders the entire screen;
def reRenderScreenF(yellow, red, playerHealths, gameFPS, red_bullets, yellow_bullets):
    global RED_FACING, YELLOW_FACING, STANDARD_BULLET_COUNT, RED_IS_RELOADING, YELLOW_IS_RELOADING
    # Creating a few fonts that will be needed;
    comicFont = pygame.font.SysFont('Comic Sans MS', 60)
    fpsFont = pygame.font.SysFont('Arial', 30)
    is_reloading_font = pygame.font.SysFont("Comic Sans MS", 25)
    
    # Setting the background to the background-image;
    WIN.blit(BACKGROUND_IMAGE, (0,0))

    # Rendering the map;
    pygame.draw.rect(WIN, WHITE, LEFT_BOTTOM_RECT, 7)
    pygame.draw.rect(WIN, WHITE, RIGHT_BOTTOM_RECT, 7)
    pygame.draw.rect(WIN, WHITE, CENTER_BOTTOM_RECT, 7)

    # Rendering the hearts;
    player_healths_arr = ["", ""]
    for i in range(len(playerHealths)):
        for x in range(playerHealths[i]):
            player_healths_arr[i]+="♡"

    # PLAYER HEALTH/INFO TEXTS
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    WIN.blit(comicFont.render("PLAYER 1:", 1, (WHITE)), (20, 10))                                                     #//
    WIN.blit(comicFont.render(player_healths_arr[0], 1, (WHITE)), (20, 72))                                           #//
    pygame.draw.rect(WIN, getValidHealthColorF("yellow"), pygame.Rect(20, 150, 15*YELLOW_PEROUND_HEALTH, 40))         #//
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    WIN.blit(comicFont.render("PLAYER 2:", 1, (WHITE)), (1365, 10))                                                   #//
    WIN.blit(comicFont.render(player_healths_arr[1], 1, (WHITE)), (1365, 72))                                         #//
    pygame.draw.rect(WIN, getValidHealthColorF("red"), pygame.Rect(1365, 150, 15*RED_PEROUND_HEALTH, 40))             #//
    #////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    # AMMO COUNT
    WIN.blit(comicFont.render(f"{str(YELLOW_BULLET_COUNT)}/{str(STANDARD_BULLET_COUNT)}", 1, (WHITE)), (20, 200)) #Yellow
    WIN.blit(comicFont.render(f"{str(RED_BULLET_COUNT)}/{str(STANDARD_BULLET_COUNT)}", 1, (WHITE)), (1470, 200)) #Red
    
    # Rendering the fps
    WIN.blit(fpsFont.render("FPS: " + str(round(gameFPS, 0)), 1, (WHITE)), (750, 20))

    PLAYER_RED_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Photos", f"fighter_weed-red-{RED_FACING}.png")), (PLAYER_WIDTH, PlAYER_HEIGHT))
    PLAYER_YELLOW_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Photos", f"fighter_weed-yellow-{YELLOW_FACING}.png")), (PLAYER_WIDTH, PlAYER_HEIGHT))
    # Rendering the players;
    WIN.blit(PLAYER_YELLOW_IMAGE, (yellow.x, yellow.y))
    WIN.blit(PLAYER_RED_IMAGE, (red.x, red.y))

    # Rendering the bullets;
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, WHITE, bullet)

    pygame.display.update()


# Handling the bullets movements/collisions;
def handleBullets(color_bullets, bullet_type, target, hittargetname):
    x = 0
    for bullet in color_bullets:
        if bullet_type[x] == "right":
            bullet.x += BULLET_VELOCITY
        else:
            bullet.x -= BULLET_VELOCITY
        if bullet.colliderect(target):
            target.y -= GUN_KNOCKBACK_VERTICAL
            if bullet_type[x] == "right":
                target.x+=GUN_KNOCKBACK_HORIZONTAL
            else:
                target.x-=GUN_KNOCKBACK_HORIZONTAL
            color_bullets.remove(bullet)
            bullet_type.remove(bullet_type[x])
            player_hit_with_gun(hittargetname)
        x+=1


def play_gun_fire_audio():
    pygame.mixer.music.load(os.path.join("Audio", "gun_shot_sound_effect.mp3"))
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()

def play_reload_audio():
    pygame.mixer.music.load(os.path.join("Audio", "gun_reload.mp3"))
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()


def main():
    global RED_FACING, YELLOW_FACING, YELLOW_BULLET_COUNT, RED_BULLET_COUNT, RED_IS_RELOADING, YELLOW_IS_RELOADING
    isRunning = True

    yellow = pygame.Rect(CENTER_PLAYER_PLACEMENT_WIDTH, CENTER_PLAYER_PLACEMENT_HEIGHT, PLAYER_WIDTH, PlAYER_HEIGHT)
    red = pygame.Rect(CENTER_PLAYER_PLACEMENT_WIDTH, CENTER_PLAYER_PLACEMENT_HEIGHT, PLAYER_WIDTH, PlAYER_HEIGHT)

    yellow_bullets = []
    yellow_bullet_types = []
    red_bullets = []
    red_bullet_types = []

    gameClock = pygame.time.Clock()


    while isRunning:
        gameClock.tick(MAX_FPS)
        # Going through all the events and doing stuff based off of the inputs we get;
        for event in pygame.event.get():
            # Checking if the user wants to quit;
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # Firing
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_SPACE:
                    if YELLOW_BULLET_COUNT > 0:
                        YELLOW_BULLET_COUNT-=1
                        play_gun_fire_audio()
                        bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        yellow_bullet_types.append(YELLOW_FACING)
                # Reload handling, player1 = lshift | player2 = rshift;
                if event.key == pygame.K_LSHIFT:
                    if not(YELLOW_BULLET_COUNT > 0):
                        play_reload_audio()
                        YELLOW_BULLET_COUNT = STANDARD_BULLET_COUNT
                        YELLOW_IS_RELOADING = False
                        
                if event.key == pygame.K_RSHIFT:
                    if not(RED_BULLET_COUNT > 0):
                        play_reload_audio()
                        RED_BULLET_COUNT = STANDARD_BULLET_COUNT
                        RED_IS_RELOADING = False
                        
                if event.key == pygame.K_RCTRL or event.key == pygame.K_SLASH:
                    if RED_BULLET_COUNT > 0:
                        RED_BULLET_COUNT-=1
                        play_gun_fire_audio()
                        bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)
                        red_bullet_types.append(RED_FACING)

        # Handling the bullets
        handleBullets(yellow_bullets, yellow_bullet_types, red, "red")
        handleBullets(red_bullets, red_bullet_types, yellow, "yellow")

        # Collecting all movements;
        keys_pressed = pygame.key.get_pressed()
        move_player_yellow(keys_pressed, yellow) # Player-Yellow movements;
        move_player_red(keys_pressed, red) # Player-Red movements;

        # GRAVITY
        lowerPlayersByGravityF(yellow)
        lowerPlayersByGravityF(red)

        # Checking if any players lost all their hearts
        checkIfAllHeartsGone(red, "red")
        checkIfAllHeartsGone(yellow, "yellow")

        # Checking if any players are under the *DEATH-ZONE*
        checkIfPlayerDead(red, "red")
        checkIfPlayerDead(yellow, "yellow")

        # Calling the window update function as the last thing in the loop;
        reRenderScreenF(yellow, red, [PLAYER_YELLOW_HEALTH, PLAYER_RED_HEALTH], gameClock.get_fps(), red_bullets, yellow_bullets)


if __name__ == "__main__":
    main()
