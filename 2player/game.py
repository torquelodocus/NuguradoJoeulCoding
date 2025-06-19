# Alex Kwong ask8kb
# Darrion Chandler djc3mu
# Winston Park wp6eh

import pygame
import gameboxnew
import random

"""
FEATURES OF THE GAME
Enemies- randomly spawned enemies and more spawn as time goes on
Collectibles- can get health pickups to heal player
Timer- tracks how long you stay alive
Health Bar- when health runs out, you lose
Two Players- two players can play
Shooting- shooting was difficult due to needing to keep track of facing direction. Ended up having to edit gamebox
          to include a projectile class that has a facing attribute.
Basic Enemy AI- created function to determine which player each enemy is closest to and moves that enemy to the closer
                player.
Collectible Text- when a health pickup is touched, text follows the player that picked it up saying they were healed.

"""


game_on = False  # is the game running
game_over = False  # did both players die and lose
win = pygame.display.set_mode((800, 600))
camera = gameboxnew.Camera(800, 600)  # the game window

# Enemies
enemies_list = []
spawn = []
enemy_velocity = 5
enemy_timer = 0
enemy_count = 0  # Tracks how many enemies are on screen at once
p1_takeDamage = True
p2_takeDamage = True
p1_player_damageTick = 0  # Tracks when the player can take damage again
p2_player_damageTick = 0
spawnrate = 200


def distance_from_player(p1_x, p2_x, p1_y, p2_y):
    """
    This function finds the closest player and moves enemies towards the closest player.
    :param p1_x: x pos of player1
    :param p2_x: x pos of player2
    :param p1_y: y pos of player1
    :param p2_y: y pos of player2
    :return: None
    """
    global enemies_list
    global p1_health
    global p2_health
    for enemy in enemies_list:
        p1_distance = abs(((p1_x - enemy.x) ** 2 + (p1_y - enemy.y) ** 2) ** (1 / 2))
        p2_distance = abs(((p2_x - enemy.x) ** 2 + (p2_y - enemy.y) ** 2) ** (1 / 2))
        if p1_health > 0 and p2_health > 0:
            if p1_distance < p2_distance:
                if enemy.x < p1.x:
                    enemy.x += 1
                    enemy.y += 1
                if enemy.x > p1.x:
                    enemy.x -= 1
                    enemy.y -= 1
            elif p2_distance < p1_distance:
                if enemy.x < p2.x:
                    enemy.x += 1
                    enemy.y += 1
                if enemy.x > p2.x:
                    enemy.x -= 1
                    enemy.y -= 1
            else:
                if enemy.x < p1.x:
                    enemy.x += 1
                    enemy.y += 1
                if enemy.x > p1.x:
                    enemy.x -= 1
                    enemy.y -= 1
        elif p1_health <= 0:
            if enemy.x < p2.x:
                enemy.x += 1
                enemy.y += 1
            if enemy.x > p2.x:
                enemy.x -= 1
                enemy.y -= 1
        else:
            if enemy.x < p1.x:
                enemy.x += 1
                enemy.y += 1
            if enemy.x > p1.x:
                enemy.x -= 1
                enemy.y -= 1


p1_width = 15  # p1 dimensions
p1_height = 60
p1_velocity = 15
p2_width = 15  # p1 dimensions
p2_height = 60
p2_velocity = 15
gravity = 1.5
p1_facing = 1  # 1 is right and -1 is left
p2_facing = 1
ground = gameboxnew.from_color(400, 500, "black", 600, 50)  # initializing terrain
platform1 = gameboxnew.from_color(125, 380, "black", 200, 20)
platform2 = gameboxnew.from_color(675, 380, "black", 200, 20)
platform3 = gameboxnew.from_color(400, 280, "black", 200, 25)
image = 'kirby_donkey_kong_reverse.png'
p1 = gameboxnew.from_image(150, 405, image)
p2 = gameboxnew.from_image(500, 405, "dedede.png")

# Health Bar
p1_health = 100
p2_health = 100
p1_healthbar_outline = gameboxnew.from_color(100, 30, "dark gray", 180, 30)
p2_healthbar_outline = gameboxnew.from_color(700, 30, "dark gray", 180, 30)

# Lists
platforms = [ground, platform1, platform2, platform3]
bullets = []
players = [p1, p2]

timer = 0
time = 0

p1_canshoot = 0
p2_canshoot = 0

# Collectibles

collect_health = gameboxnew.from_image(random.randint(200, 600), 0, "health.png")
timer_text = 0  # Tracker for how long the collectible text hangs in the air
timer_gen = 0  # Tacker for the length of time until a new collectible is generated
collect_exist = False  # Controls the spawn of a collectible
collect_touched = False  # Check to see if a collectible has been touched
touch = "none"
collect_list = []


def tick(keys):
    # we import some globals
    global game_on
    global game_over
    global p1_health
    global p2_health
    global p1_facing
    global p2_facing
    global p1_healthbar
    global image
    global timer
    global time
    global p1
    global p2
    global p1_canshoot
    global p2_canshoot
    global collect_health
    global collect_touched
    global collect_exist
    global timer_text
    global timer_gen
    global touch
    global enemy_timer
    global enemy_count
    global p1_takeDamage
    global p2_takeDamage
    global p1_player_damageTick
    global p2_player_damageTick
    global enemies_list
    global players
    global spawnrate
    global spawn
    global collect_list

    if timer % 10 == 0:  # controls spawn rate
        spawnrate -= 1
    if p1_health > 100:  # max health is 100
        p1_health = 100
    if p2_health > 100:
        p2_health = 100
    p1_canshoot += 1
    p2_canshoot += 1

    # THE HEALTH BARS
    p1_healthbar = gameboxnew.from_color(100 - (180 - ((p1_health) / 100) * 180) / 2, 30, "green",
                                         (p1_health / 100) * 180, 30)
    p2_healthbar = gameboxnew.from_color(700 - (180 - ((p2_health) / 100) * 180) / 2, 30, "green",
                                         (p2_health / 100) * 180, 30)

    if game_on == True and game_over == True:  # THE PLAYERS LOSE
        camera.clear("white")
        camera.draw(gameboxnew.from_text(400, 150, "You Lose", 200, "Black", bold=True))
        camera.draw(gameboxnew.from_text(400, 300, "You survived for " + str(time) + " seconds", 50, "Black"))
        camera.draw(gameboxnew.from_text(400, 450, "Press Space To Play Again", 50, "black"))
        if pygame.K_SPACE in keys:  # RESETTING VARIABLES FOR NEXT ROUND
            timer = 0
            time = 0
            p1_health = 100
            p2_health = 100
            p1.x = 150
            p1.y = 405
            p2.x = 500
            p2.y = 405
            enemies_list = []
            spawn = []
            collect_list = []
            players = [p1, p2]
            spawnrate = 200
            game_over = False
    if game_on == False:  # THIS IS THE TITLE SCREEN
        camera.draw(gameboxnew.from_text(400, 50, "BOOFIS AND FRIEND AGAINST THE WORLD", 40, "White", bold=True))
        camera.draw(gameboxnew.from_text(400, 150, "Instructions:", 40, "White", bold=True))
        camera.draw(gameboxnew.from_text(400, 200, '1. P1: Use keys WAD to move, "R" key to shoot', 40,
                                         "White", bold=False))
        camera.draw(gameboxnew.from_text(400, 250, '2. P2: Use keys IJL to move, "P" key to shoot', 40,
                                         "White", bold=False))
        camera.draw(gameboxnew.from_text(400, 300, "3. Shoot the enemies, don't die", 40, "White",
                                         bold=False))
        camera.draw(gameboxnew.from_text(400, 350, "4. Pick up items to power up", 40, "White", bold=False))
        camera.draw(gameboxnew.from_text(400, 425, "PRESS SPACE TO START", 80, "red", bold=False))
        camera.draw(gameboxnew.from_text(650, 525, "Alex Kwong (ask8kb)", 30, "White", bold=False))
        camera.draw(gameboxnew.from_text(650, 550, "Darrion Chandler (djc3mu)", 30, "White", bold=False))
        camera.draw(gameboxnew.from_text(650, 575, "Winston Park (wp6eh)", 30, "White", bold=False))
        if pygame.K_SPACE in keys:
            game_on = True

    if game_on == True and game_over == False:  # if game starts, have the players move
        if p1_health <= 0 and p2_health <= 0:
            game_over = True
        p1.move_speed()
        p2.move_speed()
        for enemy in enemies_list:
            enemy.move_speed()
        collect_health.move_speed()

        for thing in platforms:
            if collect_health.touches(thing):  # Collectible spawns above ground, stops it from falling
                collect_health.move_to_stop_overlapping(thing)

        if p1.y > 600:  # PLAYER DIES IF THEY FALL OFF
            p1_health = -10
            p1.x = 150
            p1.y = 405
        if p2.y > 600:
            p2_health = -10
            p2.x = 500
            p2.y = 405

        timer += 1  # TIMER INCREASES EVERY TICK
        if timer % 60 == 0:
            time += 1
        for thing in platforms:
            if pygame.K_w in keys and p1.bottom_touches(thing):  # players jump when spaced is pressed
                p1.yspeed -= 15
                p1.move_speed()
            if pygame.K_i in keys and p2.bottom_touches(thing):  # players jump when spaced is pressed
                p2.yspeed -= 15
                p2.move_speed()

            # MOVING
        if pygame.K_d in keys:  # moving p1 right
            p1.x += p1_velocity
            p1.move_speed()
            p1_facing = 1
        if pygame.K_l in keys:  # moving p2 right
            p2.x += p2_velocity
            p2.move_speed()
            p2_facing = 1
        if pygame.K_a in keys:  # moving p1 left
            p1.x -= p1_velocity
            p1.move_speed()
            p1_facing = -1
        if pygame.K_j in keys:  # moving p2 left
            p2.x -= p2_velocity
            p2.move_speed()
            p2_facing = -1

        for thing in platforms:
            if p1.touches(thing):  # stops the player1 from falling through the ground
                p1.move_to_stop_overlapping(thing)
            if p2.touches(thing):  # stops the player2 from falling through the ground
                p2.move_to_stop_overlapping(thing)

        for thing in platforms:  # ENEMY COLLISIONS
            for enemy in enemies_list:
                if enemy.bottom_touches(thing):
                    enemy.move_to_stop_overlapping(thing)
                    enemy.yspeed = 0

        p1.yspeed += gravity  # GRAVITY
        p2.yspeed += gravity
        collect_health.yspeed += gravity
        for enemy in enemies_list:
            enemy.yspeed += gravity

        # Health Bar Programming
        if pygame.K_t in keys:
            p1_health = (p1_health - 10)
        if pygame.K_y in keys:
            p2_health = (p2_health - 10)

        """Enemy Programming"""
        # Spawning
        enemy_timer += 1
        if spawnrate < 20:
            spawnrate = 100

        if enemy_timer % spawnrate == 0:
            spawn.append(1)
            for i in range(int((len(spawn))**(1/5))):
                enemies_list.append(gameboxnew.from_image(random.randint(200, 600), 100, "enemy.png"))



        # Enemy Damage/Collision
        for enemy in enemies_list:
            if enemy.y > 600:
                enemies_list.pop(enemies_list.index(enemy))
            if p1.touches(enemy):
                p1_takeDamage = False
                p1_player_damageTick += 1
            if p1_player_damageTick == 10 and p1_takeDamage == False:
                p1_health -= 10
                p1_player_damageTick = 0
                p1_takeDamage = True

            if p2.touches(enemy):
                p2_takeDamage = False
                p2_player_damageTick += 1
            if p2_player_damageTick == 10 and p2_takeDamage == False:
                p2_health -= 10
                p2_player_damageTick = 0
                p2_takeDamage = True

        # Movement/Targetting
        distance_from_player(p1.x, p2.x, p1.y, p2.y)

        # Bullet Programming
        for bullet in bullets:
            for thing in platforms:
                if bullet.touches(thing):
                    bullets.pop(bullets.index(bullet))
        for bullet in bullets:
            if 800 > bullet.x > 0:
                bullet.x += bullet.xspeed
            else:
                bullets.pop(bullets.index(bullet))
        if p1_health > 0:
            if pygame.K_r in keys and p1_canshoot > 15:
                bullets.append(gameboxnew.from_projectile(p1.x, p1.y, "black", 10, 10, p1_facing))
                p1_canshoot = 0
        if p2_health > 0 and p2_canshoot > 15:
            if pygame.K_p in keys:
                bullets.append(gameboxnew.from_projectile(p2.x, p2.y, "black", 10, 10, p2_facing))
                p2_canshoot = 0

        for bullet in bullets:
            for enemy in enemies_list:
                if bullet.touches(enemy):
                    enemies_list.pop(enemies_list.index(enemy))
                    try:
                        bullets.pop(bullets.index(bullet))
                    except:
                        None
                    enemy_count -= 1

        # ------------------------- DRAWING------------------------
        camera.clear("white")
        camera.draw(gameboxnew.from_image(400, 300, "background.png"))
        # COLLECTIBLES
        timer_gen += 1
        if timer_gen % 200 == 0:
            collect_health.x = random.randint(100, 700)
            collect_health.y = 0
            collect_list.append(collect_health)

        for collectible in collect_list:
            if p1.touches(collectible):
                touch = "p1"
                collect_touched = True
                collect_list.pop(collect_list.index(collectible))
                if collectible == collect_health:
                    p1_health += 10
            if p2.touches(collectible):
                touch = "p2"
                collect_touched = True
                collect_list.pop(collect_list.index(collectible))
                if collectible == collect_health:
                    p2_health += 10
        if collect_touched == True:
            if touch == "p1":
                camera.draw(gameboxnew.from_text(p1.x, p1.y - 50, "Healed!", 40, "red"))
            if touch == "p2":
                camera.draw(gameboxnew.from_text(p2.x, p2.y - 50, "Healed!", 40, "red"))
            timer_text += 1
        if timer_text == 50:
            collect_touched = False
            timer_text = 0

        # DRAWING BULLETS
        for bullet in bullets:
            bullet.x += 20 * bullet.facing
            bullet.move_speed()
            camera.draw(bullet)

        for thing in platforms:
            camera.draw(thing)  # drawing the ground
        for collectible in collect_list:
            camera.draw(collectible)
        camera.draw(p1_healthbar_outline)
        camera.draw(p1_healthbar)
        camera.draw(p2_healthbar_outline)
        camera.draw(p2_healthbar)
        for enemy in enemies_list:
            camera.draw(enemy)
        if p1_health <= 0:
            try:
                players.pop(players.index(p1))
            except:
                None
        if p2_health <= 0:
            try:
                players.pop(players.index(p2))
            except:
                None
        for player in players:
            camera.draw(player)
        camera.draw(gameboxnew.from_text(400, 50, str(time), 100, "black"))
    camera.display()


ticks_per_second = 60  # 60 ticks per second

gameboxnew.timer_loop(ticks_per_second, tick)  # runs game

# CHECKPOINT 2
"""
Movement controls work using wad and ijl for player one and player two. Added a basic health bar for player one
that decreases when you press/hold space. Used sprites for the two players. Added a title screen. Two players can
play simultaneously. Player one can kind of shoot projectiles by pressing R but it does not fully work. Enemies, timer,
collectibles, and multiple levels have not been added into the game yet
"""

# CHECKPOINT 1
"""
 Group of 3 so need 6 optional features.

 Platform shooter game where 2 people work together to kill enemies. When all the enemies are killed, you move to the
 next level. levels will be generated until players die or run out of time. Subsequent levels will spawn harder
 enemies. Items will be spawned and can be collected by players to make them stronger.


Required Features:
    User Input- players will use keyboard to move and shoot
    Graphics- characters and enemies will have sprites
    Start Screen- start screen with names and instructions
    Small Enough Window- game resolution will be 800x600

 6 Options:
    Enemies- randomly spawned enemies that get stronger as level increases
    Collectibles- powerups that players can collect to make them stronger (time boost or heal)
    Timer- the score
    Health Bar- when health runs out, you lose
    Two Players- two players can play
    shooting
"""
