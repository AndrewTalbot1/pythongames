import math
import pygame
import random

from pygame import mixer



# Initalize the pygame
pygame.init()

screen = pygame.display.set_mode((800,600))

#Background image
background = pygame.image.load("background.png")

#Background music
#mixer.music.load("background.wav")
#mixer.music.play(-1)

#Title and Icon
# ICON <div>Icons made by <a href="https://www.flaticon.com/authors/pixel-buddha" title="Pixel Buddha">Pixel Buddha</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Space Ship Player
#<div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
playerImg = pygame.image.load('player.png')
playerX = 370 # X = left and right
playerY = 480 # y = up and down
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('death.png'))
    enemyX.append(random.randint(0, 735)) # X = left and right
    enemyY.append(random.randint(50, 150)) # y = up and down
    enemyX_change.append(30)
    enemyY_change.append(40)


# Bullet
# Ready - can't see bullet
# Fire - bullet is moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0  # X = left and right
bulletY = 480 # y = up and down
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"


# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render("Score :" +str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg,(x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet (x, y):
    global bullet_state
    bullet_state = "fire"
    # Fire from top of ship
    screen.blit(bulletImg,(x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:

    # Red, Green, Blue
    screen.fill((0, 0, 0))
    #Background image
    screen.blit(background, (0, 0))
    
    # Moving the player left to right
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        # Keystroke    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                
                playerX_change = -20
            if event.key == pygame.K_RIGHT:
                playerX_change = 20
                

            # BULLET
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    pygame.mixer.music.load('laser.wav')
                    pygame.mixer.music.play()
                    #bullet_Sound = mixer.Sound('laser.wav')
                    #bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    
                 
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                #print("Release")
                playerX_change = 0

    playerX += playerX_change

    #Game Borders Player
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Game Borders Enemy
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break



        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0: 
            enemyX_change[i] = 10
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -10 
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            #explosionSound = mixer.Sound("explosion.wav")
            #explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            #Respawn a new enemy
            enemyX[i] = random.randint(0, 800) 
            enemyY[i] = random.randint(50, 150)
    #Bullet Movement
        enemy(enemyX[i], enemyY[i], i)
    if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

 

    
    


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()



