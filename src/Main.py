from pygame import *
from random import *
from math import *
# =======================================================================================================================
screen = display.set_mode((1200, 800))  # Sets screen length and width
# =======================================================================================================================
#colours
RED = (119, 0, 27)
GREEN = (39, 224, 114)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (190, 190, 190)
# =======================================================================================================================
clock = time.Clock()  # Creates clock variable for 60 frames per second
# =======================================================================================================================
#fonts
font.init()
font1 = font.SysFont("Copperplate Gothic Bold", 80)
font2 = font.SysFont("Copperplate Gothic Bold", 50)
font3 = font.SysFont("Copperplate Gothic Bold", 25)
# =======================================================================================================================
# default variables
textEnd = False
page = 0  # page of text at start of gam
didGoNext = False  # checking if the page has updated
ending = False  # checking if the game is done
finalDeaths = 0  # how many times you've died
click = True  #checking if you clicked
weaponGet = False  # checking if you picked up the next weapon
levelRestart = False  # checking if you restarted the level
gameRestart = False  # checking if you restarted the game
totalDeaths = 5  # how many lives you have
game = "start"  # setting the starting screen
textNum = 0  # index for text at start of game
gameTime = 0  # time taken to beat game
enemyList = []  # Creates a list for the enemies which is empty for use
global levelNum  # Variable levelNum is required for everything and therefore becomes a global
levelNum = 0  # Sets the default level number which is zero or the tutorial
waveTime = 0  # Sets a counter for how long its passed by since the level began
endTime = 100 #When the last wave will spawn
startTime = 100  # sets the time for how long it takes for the mobs to spawn
backgrounds = {image.load('screens/land1.png').convert(): image.load("screens/landmask1.png").convert(),  #Dictionary for the background and mask
               image.load('screens/land2.png').convert(): image.load("screens/landmask2.png").convert(),
              image.load('screens/land3.png').convert(): image.load("screens/landmask3.png").convert(),
               image.load('screens/land4.png').convert(): image.load("screens/landmask4.png").convert(),
               image.load('screens/land5.png').convert(): image.load("screens/landmask5.png").convert()}
portals = {image.load('screens/portal1.png'): (1150, 300),  #Dictionary of the portals and their spawn location
           image.load('screens/portal2.png'): (1075, 360),
           image.load('screens/portal3.png'): (1000, 610),
           image.load('screens/portal4.png'): (1085, 490)}
weapons = [image.load('attacks/sword.png'), image.load('attacks/bombs.png'), image.load('attacks/bow.png')]  # loading weapons
# =======================================================================================================================
class Object:  # Creates render class for player and enemy and allows every attribute from an enemy to be deleted if they die
    def render(self):
        """rendering object"""
        pass
# =======================================================================================================================
class Player(Object):  # Creates a class for the player
    def __init__(self, x,
                 y):  # Has parameters for its default x and y positions as well as its default direction the player is facing
        self.invincibility = False  # Makes a boolean for whether or not the player is invincible so they don't lose more than one health when they get hit
        self.iFrame = 0  # Creates a counter for how long the player is invincible (invincibility frame)
        self.x = x  # Changes the parameter x so that it can be changed in other functions
        self.y = y  # Changes the parameter y so that it can be changed in other functions
        self.face = "down"  # Changes the parameter face so that it can be changed in other functions
        self.moveTime = 0  # used for cycling between sprites
        self.moveList = 1  # used for deciding which sprite will be blit
        self.health = 5  # Player starts off with 3 health and if it reaches 0, player starts over
        self.weapon = "knife"  # default weapon
        self.projectile = []  # list of arrows
        self.bombRect = Rect(self.x - 70, self.y - 70, 140, 140)
        self.bombTime = 0  # when the bomb will blow up
        self.bombList = []  # list of bomb location
        self.bombSprite = image.load('attacks/bomb.png')
        self.explosionSprite = image.load("attacks/explosion.png")
        self.sprites = [[], [], [], [], []]  # Loads a sprite for the player
        self.stabRect = Rect(self.x - 20, self.y, 20, 40)  # Sets the default hurtbox for when the player is facing down, which is the default
        self.sFrame = 0  # Creates a counter for the frames the sword lingers (sword frame)
        self.knifeUp = image.load("player/mcku.png")  # loading images
        self.knifeDown = image.load("player/mckd.png")
        self.knifeRight = image.load("player/mckr.png")
        self.knifeLeft = image.load("player/mckl.png")
        self.swordUp = image.load("player/mcsu.png")
        self.swordDown = image.load("player/mcsd.png")
        self.swordRight = image.load("player/mcsr.png")
        self.swordLeft = image.load("player/mcsl.png")
        self.bombWalkUp = image.load("player/mcbmu.png")
        self.bombWalkDown = image.load("player/mcbmd.png")
        self.bombWalkRight = image.load("player/mcbmr.png")
        self.bombWalkLeft = image.load("player/mcbml.png")
        self.bowUp = image.load("player/mcbu.png")
        self.bowDown = image.load("player/mcbd.png")
        self.bowRight = image.load("player/mcbr.png")
        self.bowLeft = image.load("player/mcbl.png")
        self.hurtboxes = [Rect(self.x - 10, self.y - 4, 28, 1),
                          # Creates a hurtbox above, beside and below the player so collision is properly detected
                          Rect(self.x - 10, self.y - 4, 1, 36),
                          Rect(self.x - 10, self.y + 32, 28, 1),
                          Rect(self.x + 17, self.y - 4, 1, 36)]
        for sprite in range(1, 10):#Adds player walking sprites to a list for player to cycle through
            self.sprites[0].append(image.load("player/mcu%i.png" % sprite))
            self.sprites[1].append(image.load("player/mcd%i.png" % sprite))
        for sprite in range(1, 8):
            self.sprites[2].append(image.load("player/mcl%i.png" % sprite))
            self.sprites[3].append(image.load("player/mcr%i.png" % sprite))

# =======================================================================================================================
#player movemnt
    def movement(self):
        keys = key.get_pressed()  # Allows program to access keyboard
        mx, my = mouse.get_pos()
        try:#Player moves directions depending on which key is pressed unless blocked by wall
            if keys[K_w] == 1 or backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 3, self.y + 32)) == BLACK:  # If "W" key is pressed, moves player up and player faces up
                self.y -= 6
            if keys[K_s] == 1 or backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 3, self.y - 15)) == BLACK:  # If "S" key is pressed, moves player down and player faces down
                self.y += 6
            if keys[K_a] == 1 or backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 17, self.y + 10)) == BLACK:  # If "A" key is pressed, moves player left and player faces left
                self.x -= 6
            if keys[K_d] == 1 or backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x - 15, self.y + 10)) == BLACK:  # If "D" key is pressed, moves player right and player faces right
                self.x += 6
        except:
            pass
        if abs(self.x-mx)>abs(self.y-my):  # what direction the player is facing based off the mouse
            if self.x-mx>0:
                self.face = "left"
            if self.x-mx<0:
                self.face = "right"
        if abs(self.x-mx)<abs(self.y-my):
            if self.y-my>0:
                self.face = "up"
            if self.y-my<0:
                self.face = "down"

        if self.x < 2:  # pushes you into the screen if you get pushed out the map
            self.x += 2
        elif self.x > 1198:
            self.x -= 2
        elif self.y > 798:
            self.y -= 2
        elif self.y < 2:
            self.y += 2

        self.hurtboxes = [Rect(self.x - 10, self.y - 4, 28, 1),
                          Rect(self.x - 10, self.y - 4, 1, 36),
                          Rect(self.x - 10, self.y + 32, 28, 1),
                          Rect(self.x + 17, self.y - 4, 1, 36)]  # Updates the hurtboxes as players location moves

# =======================================================================================================================
#collision for player
    def collision(self, enemy):
        try:
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x - 5, self.y )) == BLACK: # make sure you dont get stuck in the wall
                self.x += 5
                self.y += 5
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 15, self.y )) == BLACK:
                self.x -= 5
                self.y += 5
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 15, self.y+20 )) == BLACK:
                self.x -= 5
                self.y -= 5
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x, self.y+20 )) == BLACK:
                self.x += 5
                self.y -= 5
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 3, self.y - 20)) != BLACK:
                if self.hurtboxes[0].colliderect(enemy.enemyHitBox) or self.hurtboxes[0].colliderect(
                        enemy.bossHitBox):  # If an enemy collides above the player, move the player down and turns the player invincible for a bit
                    if enemy.type == "slime" or enemy.type == "zombie" or enemy.type == "bomber":  # if you collide with certain mobs you take damage
                        self.invincibility = True
                    if self.y < 760 or enemy.Type != "mage" or enemy.Type != "bossMage" or enemy.type != "bossSkeleton":  # so you dont walk through the walls
                        self.y += 20
                        enemy.y -= 20
                    if self.y < 760 and enemy.Type == "mage" or enemy.Type == "bossMage" or enemy.type == "bossSkeleton":
                        self.y += 20
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x - 20, self.y + 10)) != BLACK:
                if self.hurtboxes[1].colliderect(enemy.enemyHitBox) or self.hurtboxes[1].colliderect(
                        enemy.bossHitBox):  # If an enemy collides to the left of the player, move the player right and turns the player invincible for a bit
                    if enemy.type == "slime" or enemy.type == "zombie"or enemy.type == "bomber":
                        self.invincibility = True
                    if self.x < 1180 or enemy.Type != "mage" or enemy.Type != "bossMage" or enemy.type != "bossSkeleton":
                        self.x += 20
                        enemy.x -= 20
                    if self.x < 1180 and enemy.Type == "mage" or enemy.Type == "bossMage" or enemy.type == "bossSkeleton":
                        self.x += 20
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 3, self.y + 42)) != BLACK:
                if self.hurtboxes[2].colliderect(enemy.enemyHitBox) or self.hurtboxes[2].colliderect(
                        enemy.bossHitBox):  # If an enemy collides beneath the player, move the player up and turns the player invincible for a bit
                    if enemy.type == "slime" or enemy.type == "zombie"or enemy.type == "bomber":
                        self.invincibility = True
                    if self.y > 20 or enemy.Type != "mage" or enemy.Type != "bossMage" or enemy.type != "bossSkeleton":
                        self.y -= 20
                        enemy.y += 20
                    if self.y > 20 and enemy.Type == "mage" or enemy.Type == "bossMage" or enemy.type == "bossSkeleton":
                        self.y -= 20
            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.x + 27, self.y + 10)) != BLACK:
                if self.hurtboxes[3].colliderect(enemy.enemyHitBox) or self.hurtboxes[3].colliderect(
                        enemy.bossHitBox):  # If an enemy collides to the right of the player, move the player left and turns the player invincible for a bit
                    if enemy.type == "slime" or enemy.type == "zombie" or enemy.type == "bomber":
                        self.invincibility = True
                    if self.x > 20 or enemy.Type != "mage" or enemy.Type != "bossMage" or enemy.type != "bossSkeleton":
                        self.x -= 20
                        enemy.x += 20
                    if self.x > 20 and enemy.Type == "mage" or enemy.Type == "bossMage" or enemy.type == "bossSkeleton":
                        self.x -= 20
        except:
            pass
        if self.invincibility:  # If the player is invincible adds to the counter for how long they are invincible for
            self.iFrame += 1
        if self.iFrame == 1:  # At the first frame of invincibility, the player loses one health
            self.health -= 1
        if self.iFrame == 80:  # If the player has reached 120 frames of invincibility, then reset the counter and make the player vulnerable again
            self.iFrame = 0
            self.invincibility = False
# =======================================================================================================================
#Knife weapon
    def knife(self):
        mb = mouse.get_pressed()  # Allows program to access mouse buttons
        if mb[
            0] == 1 and self.sFrame < 15:  # If left click is pressed and the sword is out for less than 15 frames use sword
            self.sFrame += 1  # Adds to the counter so you can't walk around with the sword always out
            if self.face == "up":  # If player is facing up, change the hitbox to be above
                self.stabRect = Rect(self.x - 15, self.y - 40, 40, 30)
                screen.blit(self.knifeUp, (self.x - 20, self.y - 45))
            elif self.face == "right":  # If player is facing right, change the hitbox to be to the right
                self.stabRect = Rect(self.x + 20, self.y - 10, 30, 40)
                screen.blit(self.knifeRight, (self.x - 12.5, self.y - 12.5))
            elif self.face == "down":  # If player is facing down, change the hitbox to be below
                self.stabRect = Rect(self.x - 15, self.y + 30, 40, 30)
                screen.blit(self.knifeDown, (self.x - 20, self.y - 25))
            elif self.face == "left":  # If player is facing left, change the hitbox to be to the left
                self.stabRect = Rect(self.x - 40, self.y - 10, 30, 40)
                screen.blit(self.knifeLeft, (self.x - 35, self.y - 12.5))
        if mb[0] == 0:
            self.sFrame = 0  # If the player lets go of left click the sword can be used again by resetting the counter
# =======================================================================================================================
#Sword weapon similar to knife
    def sword(self):
        mb = mouse.get_pressed()  # Allows program to access mouse buttons
        if mb[
            0] == 1 and self.sFrame < 15:  # If left click is pressed and the sword is out for less than 15 frames use sword
            self.sFrame += 1  # Adds to the counter so you can't walk around with the sword always out
            if self.face == "up":  # If player is facing up, change the hitbox to be above
                self.stabRect = Rect(self.x - 15, self.y - 70, 40, 60)
                screen.blit(self.swordUp, (self.x - 10, self.y - 35))
            elif self.face == "right":  # If player is facing right, change the hitbox to be to the right
                self.stabRect = Rect(self.x + 20, self.y - 10, 60, 40)
                screen.blit(self.swordRight, (self.x - 12.5, self.y - 12.5))
            elif self.face == "down":  # If player is facing down, change the hitbox to be below
                self.stabRect = Rect(self.x - 15, self.y + 35, 40, 60)
                screen.blit(self.swordDown, (self.x - 20, self.y - 15))
            elif self.face == "left":  # If player is facing left, change the hitbox to be to the left
                self.stabRect = Rect(self.x - 70, self.y - 10, 60, 40)
                screen.blit(self.swordLeft, (self.x - 45, self.y - 12.5))
        if mb[0] == 0:
            self.sFrame = 0  # If the player lets go of left click the sword can be used again by resetting the counter
# =======================================================================================================================
# bomb weapon
    def bomb(self):
        if mb[0] == 1:  # drop the bomb when you left click
            if self.bombTime < 15:#Holds a bomb for 25
                self.bombTime += 1
            if self.bombTime == 15:
                if self.face == "up":  # checking where your facing, and throwing the boss in that location
                    self.bombList.append(Rect(self.x, self.y-50, 20, 20))
                elif self.face == "down":
                    self.bombList.append(Rect(self.x, self.y+50, 20, 20))
                elif self.face == "right":
                    self.bombList.append(Rect(self.x+50, self.y, 20, 20))
                elif self.face == "left":
                    self.bombList.append(Rect(self.x-50, self.y, 20, 20))
                screen.blit(self.bombSprite, (self.bombList[0][0],self.bombList[0][1]))
        if mb[0] == 0 and self.bombTime >= 15 and self.bombTime <= 20:# if you let go of the left click, let the bomb explode
            self.bombTime += 1
            self.bombRect = Rect(self.bombList[0][0] - 70, self.bombList[0][1] - 70, 140, 140)
            screen.blit(self.explosionSprite, (self.bombList[0][0]-90, self.bombList[0][1]-90))
        if self.bombTime == 20:#Removes the bomb if explodes and resets time
            self.bombTime = 0
            self.bombList.clear()
        if self.bombTime > 0 and self.bombTime < 15:
            if self.face == "up":  # If player is facing up, change the hitbox to be above
                screen.blit(self.bombWalkUp, (self.x - 12.5, self.y - 15))
            if self.face == "right":  # If player is facing right, change the hitbox to be to the right
                screen.blit(self.bombWalkRight, (self.x - 12.5, self.y - 12.5))
            if self.face == "down":  # If player is facing down, change the hitbox to be below
                screen.blit(self.bombWalkDown, (self.x - 12.5, self.y - 12.5))
            if self.face == "left":  # If player is facing left, change the hitbox to be to the left
                screen.blit(self.bombWalkLeft, (self.x - 28, self.y - 12.5))
# =======================================================================================================================

# bow weapon
    def bow(self, arrows):
        global click
        mx, my = mouse.get_pos()
        if not click:  # if you click, shoot one bullet
            click = True
            ang = atan2(my - self.y, mx - self.x)
            projectileX, projectileY = cos(ang) * 7, sin(ang) * 7  # horizontal component
            arrows.append([self.x, self.y, projectileX, projectileY])

        for arrow in self.projectile[:]:  # arrows[:] is a COPY of the arrows list
            arrow[0] += arrow[2]
            arrow[1] += arrow[3]
            if arrow[0] > 1200 or arrow[0] < 0 or arrow[1] > 800 or arrow[1] < 0:  # off-screen
                self.projectile.remove(arrow)

        if mb[0] == 1:
            if self.face == "up":  # If player is facing up, change the hitbox to be above
                screen.blit(self.bowUp, (self.x - 12.5, self.y - 12.5))
            if self.face == "right":  # If player is facing right, change the hitbox to be to the right
                screen.blit(self.bowRight, (self.x - 12.5, self.y - 12.5))
            if self.face == "down":  # If player is facing down, change the hitbox to be below
                screen.blit(self.bowDown, (self.x - 12.5, self.y - 12.5))
            if self.face == "left":  # If player is facing left, change the hitbox to be to the left
                screen.blit(self.bowLeft, (self.x - 12.5, self.y - 12.5))

# =======================================================================================================================
#blitting the players sprites
    def render(self):
        #If sprites from other functions aren't blitting, blit the normal walking animation by cycling through a list with timer as an index
        if self.weapon == "knife" or self.weapon == "sword":
            if self.sFrame == 0 or self.sFrame == 15:
                screen.blit(self.sprites[self.moveList][self.moveTime // 3],
                            (self.x - 12.5, self.y - 12.5))  # Blits the sprite at the player's location
        if self.weapon == "bombs":
            if self.bombTime == 0 or self.bombTime >= 15:
                screen.blit(self.sprites[self.moveList][self.moveTime // 3],
                            (self.x - 12.5, self.y - 12.5))  # Blits the sprite at the player's location
        if self.weapon == "bow":
            if mb[0] == 0:
                screen.blit(self.sprites[self.moveList][self.moveTime // 3],
                            (self.x - 12.5, self.y - 12.5))  # Blits the sprite at the player's location
        keys = key.get_pressed()

        if self.face == "up":  # Chooses which list of sprites to cycle through and when to reset
            self.moveList = 0
            self.moveTime += 1
            if self.moveTime // 3 > 8:
                self.moveTime = 0


        if self.face == "down":
            self.moveList = 1
            self.moveTime += 1
            if self.moveTime // 3 > 8:
                self.moveTime = 0


        if self.face == "left":
            self.moveList = 2
            self.moveTime += 1
            if self.moveTime // 3 > 6:
                self.moveTime = 0


        if self.face == "right":
            self.moveList = 3
            self.moveTime += 1
            if self.moveTime // 3 > 6:
                self.moveTime = 0

        if keys[K_w] == 0 and keys[K_a] == 0 and keys[K_s] == 0 and keys[K_d] == 0:#Becomes idle if nothing is pressed
            self.moveTime = 0

        for arrow in self.projectile:#Renders the arrows
            draw.rect(screen, GREY, (arrow[0], arrow[1], 6, 6))
# =======================================================================================================================
class Enemies(Object):  # Creates a class for the enemies
    def __init__(self, enemyX, enemyY,
                 enemyType):  # Has parameters for its default x and y positions as well as the type of enemy it is
        self.type = enemyType  # Does actions based off of what type of enemy it is
        self.x, self.y = enemyX, enemyY  # Changes the parameter x so that it can be changed in other functions
        self.moveTime = 0
        self.invincibility = False  # when the boss cant get hit
        self.iFrame = 0  # invincibility for the boss
        self.health = 160  # health for the bosses
        self.face = "down"  # default enemy face
        self.sprite = [[] for list in range(10)]  # a list of all the mobs sprites
        self.randPosx, self.randPosy = randint(0, 1200), randint(0, 800)  # random location
        self.projectile = []  # list for the enemy arrows
        self.enemyHitBox = Rect(0, 0, 0, 0) # the default enemy hitbox
        self.bossHitBox = Rect(0, 0, 0, 0)  # the default boss hitbox
        self.enemySprites = ["zomb", "bzomb", "bzombs", "bomb", "bbomb", "skel", "bmage"]  # used for rendering images
        self.magicX, self.magicY = enemyX, enemyY  # location of fire balls
        self.magic = Rect(self.magicX - 8, self.magicY - 8, 16, 16)  # the fireball
        self.broken = False  # if the boss is moving
        # =======================================================================================================================
        if enemyType == "slime":
            self.slimeTime = 0  # a counter for the slime
            self.slimeSpeed = randint(1, 3)  # the slimes speed
            self.slimeRand = randint(50, 150)  # a random timer

        if enemyType == "zombie":
            self.locationList = []  # used for if mob is stuck
            self.pos1 = 0
            self.pos2 = 1
            self.zombieTime = 0  # a counter for the zombie
            self.zombieStuck = 0
            self.zombieSpeed = randint(10, 35)  # zombies speed
            self.zombieRand = randint(50, 600)  # a random timer

        if enemyType == "bossZombie":
            self.bossZombieTime = 0  # a counter for the zombie
            self.bossZombieSpeed = randint(1, 3)  # zombies speed
            self.bossZombieRand = randint(50, 600)  # a random timer

        if enemyType == "bomber":
            self.bomberTime = 0  # a counter for the bomber

        if enemyType == "bossBomber":
            self.bomberTime = 0  # a counter for the bomber
            self.bomberCounter = 1.0#Changes Boss Bomber's size

        if enemyType == 'skeleton':
            self.shootTime = randint(100, 300)  # how often they shoot
            self.skeletonTime = 0  # a counter for the skeleton
            self.skeletonSpeed = randint(1, 2)  # the skeletons speed
            self.skeletonRand = randint(100, 600)  # a random timer
            self.projectileX, projectileY = 0, 0#X and Y of arrows

        if enemyType == 'bossSkeleton':
            self.headX, self.headY = enemyX, enemyY
            self.skeletonHealths = [40, 80, 120]
            self.shootTime = 45  # how often they shoot
            self.skeletonTime = 0  # a counter for the skeleton
            self.skeletonSpeed = randint(1, 3)  # the skeletons speed
            self.skeletonRand = randint(50, 600)  # a random timer
            self.projectileX, projectileY = 0, 0#X and Y of arrows

        if enemyType == "mage":
            self.mageRand = randint(100, 400)  # random time for mage
            self.mageTime = 1  # timer for mage
            self.fireballSprite = image.load("attacks/fireball.png")

        if enemyType == "bossMage":
            self.attackSurface = Surface((1200,800))#Where boss attacks
            self.idle = False#Changes which sprites to blit
            self.attackMove = randint(0,4)#Chooses which attack to use
            self.attackTime = 0#How long the attack lasts for
            self.attackCounter = 0#Vulnerable or not
            self.laserX, self.laserY = randint(0, 1200), randint(0, 800)#Where lasers initially start
            self.lasers = []#Lasers that attack
            self.laserVSprite = image.load("attacks/laservertical.png")
            self.laserHSprite = image.load("attacks/laserhorizontal.png")
            self.hexagons = []#Hexagons that attack
            self.hexagonSprite = image.load("attacks/hexagon.png")
            self.cloneX, self.cloneY = randint(0, 1200), randint(0, 800)#Where to teleport
            self.clones = [[],[],[],[]]#Rects for the clones
            self.cloneRand = randint(0,4)#Chooses which clone the Boss Mage becomes
            self.cloneCounter = 0#Goes through a while loop adding the clone locations to a list and increases the counter if it doesn't teleport to a mask and breaks if there are 4 clones
            self.cloneFail = False#False and if attacks the wrong clone, becomes coordinates to spawn a mage
            self.squares = []#Squares that attack
            self.squareX, self.squareY = self.x-35, self.y-35#Squares top left
            self.squareSize = 70#Size of square
            self.squareSprite = image.load("attacks/square.png")
            self.orbs = []#Orbs that attack
            self.orbList = [(randint(0, 1200), -35), (-35, randint(0, 800)), (randint(0, 1200), 835), (1235, randint(0, 800))]#Where the orbs can begin and end
            self.orbSprite = image.load("attacks/orb.png")

        for sprite in range(1, 4):#Adds sprites for all the enemies to a nested list
            self.sprite[0].append(image.load("enemies/slime%i.png" % sprite))
        for sprite in range(1, 3):
            self.sprite[1].append(image.load("enemies/mage%i.png" % sprite))
        for sprite in range(1, 8):
            self.sprite[2].append(image.load("enemies/bskel%i.png" % sprite))
        for enemy in self.enemySprites:
            for sprite in range(1, 9):
                self.sprite[self.enemySprites.index(enemy) + 3].append(image.load("enemies/%s%i.png" % (enemy, sprite)))
        self.explosionSprite = image.load("attacks/explosion.png")
        for sprite in range(9, 13):
            self.sprite[7].append(image.load("enemies/bbomb%i.png" % sprite))
# =======================================================================================================================
    def render(self):
        self.moveTime += 1#Cycles through counter for sprites
        if self.moveTime // 5 > 2:
            self.moveTime = 0
        global walking
        def walking(enemyNum):  # animates the enemy sprites if odd blits one if even blits other depending on direction
            if self.face == "down":
                if self.moveTime // 5 % 5 == 1:
                    screen.blit(self.sprite[enemyNum][0],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                else:
                    screen.blit(self.sprite[enemyNum][1],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
            if self.face == "left":
                if self.moveTime // 5 % 5 == 1:
                    screen.blit(self.sprite[enemyNum][2],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                else:
                    screen.blit(self.sprite[enemyNum][3],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
            if self.face == "right":
                if self.moveTime // 5 % 5 == 1:
                    screen.blit(self.sprite[enemyNum][4],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                else:
                    screen.blit(self.sprite[enemyNum][5],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
            if self.face == "up":
                if self.moveTime // 5 % 5 == 1:
                    screen.blit(self.sprite[enemyNum][6],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                else:
                    screen.blit(self.sprite[enemyNum][7],
                                (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y

        if self.type == "slime":
            screen.blit(self.sprite[0][self.moveTime // 5],
                        (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
        if self.type == "mage":
            if self.moveTime // 5 % 5 == 1:
                screen.blit(self.sprite[1][0], (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
            else:
                screen.blit(self.sprite[1][1], (self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
        if self.type == "zombie":
            walking(3)
        if self.type == "bossZombie":
            if self.bossZombieTime > 80 and self.bossZombieTime < 160:
                walking(5)
            else:
                walking(4)
        if self.type == "bomber":
            walking(6)
        if self.type == "skeleton":
            walking(8)
        for arrow in self.projectile:#Draws the skeleton's arrows
            draw.rect(screen, GREY, (arrow[0], arrow[1], 6, 6))
# =======================================================================================================================
# checking if the enemy gets hit
    def collision(self, player):
        mb = mouse.get_pressed()
        if self.type == "mage":
            for hurtbox in player.hurtboxes:  # If the player touches a mage's fireball. gets hurt
                if self.magic.colliderect(hurtbox):
                    player.invincibility = True
        if self.broken == False:#Doesn't work on broken boss skeleton and returns True on normal enemies to delete them
            if player.stabRect.colliderect(self.enemyHitBox) and mb[0] == 1 and player.sFrame < 15:  # bomb collision for sword and knife 8 for knife and 10 for sword if boss
                return True
            if player.weapon == "knife" and player.stabRect.colliderect(self.bossHitBox) and mb[0] == 1 and player.sFrame < 15:
                self.invincibility = True
                if self.iFrame == 1:  # At the first frame of invincibility, the player loses one health
                    self.health -= 8
            if player.weapon == "sword" and player.stabRect.colliderect(self.bossHitBox) and mb[0] == 1 and player.sFrame < 15:
                self.invincibility = True
                if self.iFrame == 1:  # At the first frame of invincibility, the player loses one health
                    self.health -= 10
            if player.weapon == "bombs" and mb[0] == 0 and player.bombTime > 15 and player.bombTime <= 20:#bomb collision and deals 5 if boss
                if player.bombRect.colliderect(self.enemyHitBox):
                    return True
                if player.bombRect.colliderect(self.bossHitBox):
                    self.invincibility = True
                    if self.iFrame == 1:  # At the first frame of invincibility, the player loses one health
                        self.health -= 5
            for arrow in player.projectile[:]:  #checks if the players arrows hit the enemy, removes the arrow if hits the enemy and deals 2 if boss
                arrowRect = Rect(arrow[0], arrow[1], 6, 6)
                if player.weapon == "bow":
                    if arrowRect.colliderect(self.enemyHitBox):
                        player.projectile.remove(arrow)
                        return True
                    if arrowRect.colliderect(self.bossHitBox):
                        self.invincibility = True
                        if self.iFrame == 1:  # At the first frame of invincibility, the player loses one health
                            self.health -= 2
                            player.projectile.remove(arrow)

        if self.invincibility:  # If the player is invincible adds to the counter for how long they are invincible for
            self.iFrame += 1
        if self.iFrame == 40:  # If the player has reached 40 frames of invincibility, then reset the counter and make the player vulnerable again
            self.iFrame = 0
            self.invincibility = False

        for enemy in enemyList:#Checks collision with other enemies so they don't overlap
            if self.x != enemy.x and self.y != enemy.y:
                if self.enemyHitBox.colliderect(enemy.enemyHitBox):
                    if self.x > enemy.x:
                        self.x += 5
                    elif self.x < enemy.x:
                        self.x -= 5
                    if self.y > enemy.y:
                        self.y += 5
                    elif self.y < enemy.y:
                        self.y -= 5
# =======================================================================================================================
#the function that lets the enemys follow the player
    def ai(self, player, dist):
        def follow(destx, desty, speed, collide):  # basic following if not touching mask also changes direction
            if self.x <= 20:
                self.x += 1
            if self.x >= 1180:
                self.x -= 1
            if self.y <= 20:
                self.y += 1
            if self.y >= 780:
                self.y -= 1
            try:
                if desty > self.y:
                    self.y += speed
                    self.face = "down"
                    if backgrounds[list(backgrounds.keys())[levelNum]].get_at(collide[1]) == BLACK:
                        self.y -= speed
                if desty < self.y:
                    self.y -= speed
                    self.face = "up"
                    if backgrounds[list(backgrounds.keys())[levelNum]].get_at(collide[3]) == BLACK:
                        self.y += speed
                if destx < self.x - 16.5:  # checking collision with mask
                    self.x -= speed
                    self.face = "left"
                    if backgrounds[list(backgrounds.keys())[levelNum]].get_at(collide[2]) == BLACK:
                        self.x += speed
                if destx > self.x + (collide[0][0]-collide[2][0]-16.5):
                    self.x += speed
                    self.face = "right"
                    if backgrounds[list(backgrounds.keys())[levelNum]].get_at(collide[0]) == BLACK:
                        self.x -= speed
            except:
                pass
# =======================================================================================================================
        if self.type == "bossZombie" or self.type == "bossBomber" or self.type == "bossSkeleton" or self.type == "bossMage":
            draw.rect(screen, RED, (370, 10, 400, 25))  # red health bar under green for bosses
            draw.rect(screen, GREEN, (370, 10, self.health * 2.5, 25))
        else:
            collideList = [(self.x+17,self.y),(self.x,self.y+24),(self.x-17,self.y),(self.x,self.y-24)]#Makes a list of points so enemy doesn't walk through mask
# =======================================================================================================================
#enemy slime
        if self.type == "slime":
            if self.slimeTime == 0:
                follow(self.randPosx, self.randPosy, self.slimeSpeed, collideList)  # sending the slime to a random location
            self.slimeTime += 1
            if self.slimeTime > self.slimeRand:  # if the random time is reached move to a new random location
                follow(self.randPosx, self.randPosy, self.slimeSpeed, collideList)
                if self.slimeTime > self.slimeRand + 50:  # making a new random location
                    self.slimeTime = 1
                    self.randPosy = randint(10, 550)
                    self.randPosx = randint(0, 800)
            self.enemyHitBox = Rect(self.x - 13, self.y - 19, 23, 35)

# =======================================================================================================================
#enemy zombie
        if self.type == "zombie":
            self.zombieStuck += 1
            self.zombieTime += 1
            if self.zombieStuck % 100 == 0:  # checking if the zombie hasnt moved in 100 frames
                self.locationList.append((self.x,self.y))
                if len(self.locationList) >= 2:
                    self.zombieStuck = 0
                    if self.zombieStuck < 100:
                        if self.locationList[self.pos1] == self.locationList[self.pos2]:  # if the zombie is stuck, move him
                            if player.x > 600:
                                self.x -= 10
                                follow(self.x-200,self.y,self.zombieSpeed//10,collideList)
                            if player.x < 600:
                                self.x += 10
                                follow(self.x+200,self.y,self.zombieSpeed//10,collideList)
                            if player.y < 400:
                                self.y += 10
                                follow(self.x,self.y+200,self.zombieSpeed//10, collideList)
                            if player.y > 400:
                                self.y -= 10
                                follow(self.x,self.y-200,self.zombieSpeed//10, collideList)
                    self.pos1 += 1
                    self.pos2 += 1
            if self.zombieTime < self.zombieRand:  # follow the player
                follow(player.x, player.y, (self.zombieSpeed // 10), collideList)
            if self.zombieTime > self.zombieRand:  # if a random time is reached track a random location for a little bit
                follow(player.x + self.randPosx, player.y + self.randPosy, (self.zombieSpeed // 10),collideList)
                if self.zombieTime > self.zombieRand + 20:
                    self.zombieTime = 0
            self.enemyHitBox = Rect(self.x - 12, self.y - 12, 25, 34)
# =======================================================================================================================
#enemy skeleton
        if self.type == "skeleton":
            self.skeletonTime += 1
            if self.skeletonTime > self.skeletonRand:  # if a random time is reached, follow a random location
                follow(self.randPosx, self.randPosy + 50, self.skeletonSpeed, collideList)
                if self.skeletonTime > self.skeletonRand + 70:  # making a new random location
                    self.randPosy = randint(0, 600)
                    self.randPosx = randint(0, 800)
                    self.skeletonTime = 0
            else:
                if dist > 300:  # if the skeleton is 300 pixels away from the player, track the player
                    follow(player.x, player.y, self.skeletonSpeed, collideList)
                if dist < 320:  # if the skeleton is less then 320 pixels stay away
                    if player.x > 600:
                        follow(self.x - 200, self.y, self.skeletonSpeed, collideList)
                    if player.x < 600:
                        follow(self.x + 200, self.y, self.skeletonSpeed, collideList)
                    if player.y < 400:
                        follow(self.x, self.y + 200, self.skeletonSpeed, collideList)
                    if player.y > 400:
                        follow(self.x, self.y - 200, self.skeletonSpeed, collideList)
            enemy.enemyShoot(enemy.projectile)
            self.enemyHitBox = Rect(self.x - 10, self.y - 15, 23, 40)
# =======================================================================================================================
#enemy bomber
        if self.type == "bomber":
            if self.enemyHitBox == Rect(self.x - 50, self.y - 50, 100,
                                        100) and self.bomberTime > 60:  # removing the bomber after he blows up
                enemyList.remove(enemy)
                objects.remove(enemy)
            if dist < 150:  # if the bomber is within 100 piles
                self.bomberTime += 1
                follow(self.x, self.y, 0, collideList)
                if self.bomberTime == 60:  # if he has been next to the player for more then 60 frames, he will explode
                    screen.blit(self.explosionSprite, (self.x - 100, self.y - 100))
                    self.enemyHitBox = Rect(self.x - 50, self.y - 50, 100, 100)
                    self.bomberTime += 1
            elif dist > 150:  # if the bomber is 50 pixles away, follow player
                follow(player.x, player.y, 4, collideList)
            if self.bomberTime < 60:  # changing the hitbox size
                self.enemyHitBox = Rect(self.x - 7, self.y - 5, 23, 35)
            elif self.bomberTime > 60:
                self.enemyHitBox = Rect(self.x - 50, self.y - 50, 100, 100)
# =======================================================================================================================
#enemy mage
        if self.type == "mage":
            self.mageTime += 1
            try:
                if self.mageTime % self.mageRand == 0:  # teleport at random times
                    while True:
                        mageX, mageY = randint(0, 1200), randint(0, 800)
                        if backgrounds[list(backgrounds.keys())[levelNum]].get_at((mageX, mageY)) != BLACK:
                            self.x, self.y = mageX, mageY
                            break
            except:
                pass
            for magic in player.hurtboxes:  # shoot every time you get hit
                if self.magic.colliderect(magic):
                    self.magicX, self.magicY = self.x, self.y
            if self.mageTime % randint(100,150) == 0:
                self.magicX, self.magicY = self.x, self.y
                self.mageTime = 0
            else:
                if player.x > self.magicX:  # tracking bullets
                    self.magicX += 2
                if player.y > self.magicY:
                    self.magicY += 2
                if player.x < self.magicX:
                    self.magicX -= 2
                if player.y < self.magicY:
                    self.magicY -= 2
            self.magic = Rect(self.magicX - 8, self.magicY - 8, 16, 16)
            self.enemyHitBox = Rect(self.x - 10, self.y - 10, 25, 40)
            screen.blit(self.fireballSprite, (self.magicX - 8, self.magicY - 8))
# =======================================================================================================================
# boss zombie
        if self.type == "bossZombie":
            self.bossZombieTime += 1
            collideList = [(self.x+75,self.y+25),(self.x+25,self.y+75),(self.x-25,self.y+25),(self.x+25,self.y-25)]
            if self.bossZombieTime < self.bossZombieRand:  # follow the player
                follow(player.x, player.y, 1, collideList)
            if self.bossZombieTime > self.bossZombieRand:  # if a random time is reached track a random location for a little bit
                follow(player.x + self.randPosx, player.y + self.randPosy, 1, collideList)
                if self.bossZombieTime > self.bossZombieRand:
                    self.bossZombieTime = 0
            if self.bossZombieTime > 80 and self.bossZombieTime < 160:
                if self.face == "up":  # If player is facing up, change the hitbox to be above
                    swordRect = Rect(self.x + 32, self.y-60, 45, 120)
                if self.face == "right":  # If player is facing right, change the hitbox to be to the right
                    swordRect = Rect(self.x+32, self.y+16, 120, 45)
                if self.face == "down":  # If player is facing down, change the hitbox to be below
                    swordRect = Rect(self.x - 16, self.y, 45, 120)
                if self.face == "left":  # If player is facing left, change the hitbox to be to the left
                    swordRect = Rect(self.x - 60, self.y+16, 120, 45)
                for hurtbox in player.hurtboxes:
                    if swordRect.colliderect(hurtbox):
                        player.invincibility = True
            if self.bossZombieTime == 160:
                self.bossZombieTime = 0
            self.bossHitBox = Rect(self.x-12.5, self.y-12.5, 107.5, 107.5)
# =======================================================================================================================
# boss zombie
        if self.type == "bossBomber":
            bomberCoord = 20#Top left of hitbox
            bomberSize = 116#Length and width of hitbox
            bomberX, bomberY = int(self.x + (50 * self.bomberCounter) - 12.5), int(self.y + (50 * self.bomberCounter) - 12.5)#The middle of the hitbox
            bombDist = int(sqrt(abs(player.x - bomberX) ** 2 + abs(player.y - bomberY) ** 2))#The distance between the player and the Boss Bomber
            bomberCoord = int(bomberCoord * self.bomberCounter)#Scales bomberCoord
            bomberSize = int(bomberSize * self.bomberCounter)#Scales bomberSize
            collideList = [(bomberX + bomberSize//2, bomberY), (bomberX, bomberY + bomberSize//2), (bomberX - bomberSize//2, bomberY), (bomberX, bomberY - bomberSize//2)]#For collision with mask
            for hurtbox in player.hurtboxes:#Hurts the player if Boss Bomber touches player
                if self.bossHitBox.colliderect(hurtbox):
                    player.invincibility = True
            if bombDist <= bomberSize:  # if the bomber is within 100 piles
                self.bomberTime += 1
                follow(self.x, self.y, 2, collideList)
                if self.face == "down":  # If player is facing up, change the hitbox to be above
                    screen.blit(self.sprite[7][8],(self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                if self.face == "left":  # If player is facing right, change the hitbox to be to the right
                    screen.blit(self.sprite[7][9],(self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                if self.face == "right":  # If player is facing down, change the hitbox to be below
                    screen.blit(self.sprite[7][10],(self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                if self.face == "up":  # If player is facing left, change the hitbox to be to the left
                    screen.blit(self.sprite[7][11],(self.x - 16.5, self.y - 23.5))  # Blits the enemy sprite to its x and y
                if self.bomberTime == 60:  # if he has been next to the player for more then 60 frames, he will explode
                    screen.blit(self.explosionSprite, (bomberX - 90, bomberY - 90))
                    self.bossHitBox = Rect(self.x - bomberCoord, self.y - bomberCoord, bomberSize, bomberSize)
                    if bomberSize < 275:#Sets a limit to size, also increases size every time a certain distance is met
                        self.bomberCounter += 0.1
            else:  # if the bomber is 50 pixels away, follow player and blits the images
                walking(7)
                follow(player.x, player.y, 4, collideList)
            if self.bomberTime > 70:#Resets timer
                self.bomberTime = 0
            self.bossHitBox = Rect(self.x - bomberCoord, self.y - bomberCoord, bomberSize, bomberSize)
            for sprite in range(12):#Scales images with size
                self.sprite[7][sprite] = transform.scale(self.sprite[7][sprite],(bomberSize,bomberSize))
# =======================================================================================================================
        if self.type == "bossSkeleton":
            self.skeletonTime += 1
            skeletonX, skeletonY = randint(0, 1200), randint(0, 800)
            if self.broken == False:#Displays a set of sprites if Boss Skeleton isn't broken
                if self.x - 16.5 > player.x:
                    screen.blit(self.sprite[2][1],(self.x - 16.5, self.y - 23.5))
                elif self.x + 63.5 < player.x:
                    screen.blit(self.sprite[2][2],(self.x - 16.5, self.y - 23.5))
                else:
                    screen.blit(self.sprite[2][0], (self.x - 16.5, self.y - 23.5))
                enemy.enemyShoot(enemy.projectile)
            if self.health in self.skeletonHealths and self.broken == False:#Becomes broken if health is divisible by 40
                self.skeletonTime = 0
                self.broken = True
                self.skeletonHealths.pop()
            if self.broken == True:#Moves to a location on the map while broken as a head displaying certain sprites
                try:
                    if self.skeletonTime == 0:
                        self.projectile = []
                        while True:
                            self.skeletonX, self.skeletonY = randint(0, 1200), randint(0, 800)
                            if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.skeletonX, self.skeletonY)) != BLACK:
                                self.x, self.y = skeletonX, skeletonY
                                break
                except:
                    pass
                self.skeletonTime += 1
                if self.skeletonTime >= 1:
                    if self.x - 16.5 > self.headX:  # tracking bullets
                        screen.blit(self.sprite[2][6], (self.headX, self.headY))
                    elif self.x + 63.5 < self.headX:
                        screen.blit(self.sprite[2][5], (self.headX, self.headY))
                    else:
                        screen.blit(self.sprite[2][4], (self.headX, self.headY))
                    if self.x > self.headX:  # tracking bullets
                        self.headX += 1
                    elif self.x < self.headX:
                        self.headX -= 1
                    elif self.y < self.headY:
                        self.headY -= 1
                    elif self.y > self.headY:
                        self.headY += 1
                    screen.blit(self.sprite[2][3], (self.x - 16.5, self.y - 23.5))
                if self.headX == self.x and self.headY == self.y and self.skeletonTime > 0:#Reforms if head reaches body
                    self.broken = False
            self.bossHitBox = Rect(self.x - 16.5, self.y - 23.5, 81, 111)
# =======================================================================================================================
#final boss
        if self.type == "bossMage":
            self.attackSurface.fill(BLACK)#Makes the screen which the enemy attacks in default to black
            self.cloneFail = False#Makes it so that mages don't spawn when attacking all clones
            self.attackTime += 1#Adds to a timer which is when each attack happens and how long they last for
            if self.attackMove != 2:#If bossMage isn't using clone attack, the teleports to a place unreachable on odd turns and a random place on even turns
                if self.attackCounter % 2 == 1:
                        self.x, self.y = 589, 35
                        if self.attackTime == 2:
                            self.squareX, self.squareY = self.x - 35, self.y - 35
                if self.attackCounter % 2 == 0:
                    try:
                        if self.attackTime == 2:
                            while True:
                                mageX, mageY = randint(0, 1200), randint(0, 800)
                                if backgrounds[list(backgrounds.keys())[levelNum]].get_at((mageX, mageY)) != BLACK:
                                    self.x, self.y = mageX, mageY
                                    self.squareX, self.squareY = self.x - 35, self.y - 35
                                    break
                    except:
                        pass
            self.bossHitBox = Rect(self.x - 16.5, self.y - 23.5, 60, 64)#Updates hitbox location
            if self.idle == True:#Enemy becomes idle after attacking for player to punish and displays different sprites whether idle or not
                if self.x - 16.5 > player.x:
                    screen.blit(self.sprite[9][2], (self.x - 16.5, self.y - 23.5))
                elif self.x + 43.5 < player.x:
                    screen.blit(self.sprite[9][4], (self.x - 16.5, self.y - 23.5))
                else:
                    if self.y < player.y:
                        screen.blit(self.sprite[9][0], (self.x - 16.5, self.y - 23.5))
                    if self.y > player.y:
                        screen.blit(self.sprite[9][6], (self.x - 16.5, self.y - 23.5))
            if self.idle == False:
                if self.x - 16.5 > player.x:
                    screen.blit(self.sprite[9][3], (self.x - 16.5, self.y - 23.5))
                elif self.x + 43.5 < player.x:
                    screen.blit(self.sprite[9][5], (self.x - 16.5, self.y - 23.5))
                else:
                    if self.y < player.y:
                        screen.blit(self.sprite[9][1], (self.x - 16.5, self.y - 23.5))
                    if self.y > player.y:
                        screen.blit(self.sprite[9][7], (self.x - 16.5, self.y - 23.5))
            if self.attackTime == 1:#Add to counter of where bossMage teleports when everytime counter resets
                self.attackCounter += 1
            if self.attackMove == 0:#Laser attack
                if self.attackTime < 80:#Attacks on 20, 40, 60
                    if player.x > self.laserX:#Lasers follow player
                        self.laserX += 3
                    if player.y > self.laserY:
                        self.laserY += 3
                    if player.x < self.laserX:
                        self.laserX -= 3
                    if player.y < self.laserY:
                        self.laserY -= 3
                    if self.attackTime % 20 == 0:
                        self.lasers.append(((self.laserX, 0), (self.laserX, 800)))#Laser from top of the screen to bottom of the screen based on X of laser
                        self.lasers.append(((0, self.laserY), (1200, self.laserY)))#Laser from left side of the screen to the right side of the screen based on Y of laser
                    for laser in self.lasers:
                        draw.line(self.attackSurface, GREEN, laser[0], laser[1],10)#Draws lasers
                        if laser[0][1] == 0 and laser[1][1] == 800:#Blits vertical sprite
                            screen.blit(self.laserVSprite, (laser[0][0]-4, laser[0][1]))
                        elif laser[0][0] == 0 and laser[1][0] == 1200:#Blits horizontal sprite
                            screen.blit(self.laserHSprite, (laser[0][0], laser[0][1]-4))
                if self.attackTime == 80:#Stops lasers and idles
                    self.idle = True
                    self.lasers.clear()
                    self.laserX, self.laserY = randint(0, 1200), randint(0, 800)
                if self.attackTime == 180:#Resets everything
                    self.idle = False
                    self.attackTime = 0
                    self.attackMove = randint(0,4)
            if self.attackMove == 1:#Hexagon attack
                if self.attackTime < 50:#Attacks at 10, 20, 30, 40 at random locations with random sizes
                    if self.attackTime % 10 == 0:
                        self.hexagons.append((randint(0, 1200), randint(0, 800),randint(50,200)))
                    for hexagon in self.hexagons:
                        hexagonSprite = transform.scale(self.hexagonSprite,(hexagon[2]*2, hexagon[2]*2))#Sprite scales with size
                        draw.polygon(self.attackSurface, GREEN, [(hexagon[0] + hexagon[2] * cos(2 * pi * side / 6), hexagon[1] + hexagon[2] * sin(2 * pi * side / 6))#Does calculations for the hexagon and draws the hexagons
                            for side in range(6)], hexagon[2]//3)
                        screen.blit((hexagonSprite), (hexagon[0] - hexagon[2], hexagon[1] - hexagon[2]))#Blits sprite
                if self.attackTime == 50:#Stops hexagons and idles
                    self.idle = True
                    self.hexagons.clear()
                if self.attackTime == 150:#Resets everything
                    self.idle = False
                    self.attackTime = 0
                    self.attackMove = randint(0,4)
            if self.attackMove == 2:#Clone attack
                if self.attackTime < 1000:#Adds current location as well as 3 other random locations to a list as rects
                    try:
                        if self.attackTime == 1:
                            self.cloneRand = randint(0, 3)
                            self.clones[0].append((self.x - 16.5, self.y - 23.5, 60, 64))
                            while True:
                                self.cloneX, self.cloneY = randint(0, 1200), randint(0, 800)
                                if backgrounds[list(backgrounds.keys())[levelNum]].get_at((self.cloneX, self.cloneY)) != BLACK:
                                    self.clones[self.cloneCounter].append((self.cloneX, self.cloneY, 60, 64))
                                    self.cloneCounter += 1
                                if self.cloneCounter == 4:
                                    break
                            self.x, self.y = self.clones[self.cloneRand][0][0] + 16.5, self.clones[self.cloneRand][0][1] + 23.5#Updates location and hitbox as one of the locations in the list
                            self.bossHitBox = self.clones[self.cloneRand][0]
                    except:
                        pass
                    try:
                        if self.attackTime > 0:
                            for clone in self.clones:#Detects collision with clones and player weapons, killing the clone and ending the attack, if it's a fake then changes variable cloneFail so a mage can be spawned in the while loop
                                if player.stabRect.colliderect(Rect(clone[0])) and player.sFrame > 0 and player.sFrame < 15:
                                    self.attackTime = 1000
                                    if Rect(clone[0]) != self.bossHitBox:
                                        self.cloneFail = (self.clones[self.clones.index(clone)][0][0], self.clones[self.clones.index(clone)][0][1])
                                        del self.clones[self.clones.index(clone)]
                                if player.bombRect.colliderect(Rect(clone[0])) and mb[0] == 0 and player.bombTime >= 25 and player.bombTime <= 30:
                                    self.attackTime = 1000
                                    if Rect(clone[0]) != self.bossHitBox:
                                        self.cloneFail = (self.clones[self.clones.index(clone)][0][0], self.clones[self.clones.index(clone)][0][1])
                                        del self.clones[self.clones.index(clone)]
                                for arrow in player.projectile[:]:
                                    arrowHitBox = Rect(arrow[0], arrow[1], 6, 6)
                                    if arrowHitBox.colliderect(Rect(clone[0])):
                                        player.projectile.remove(arrow)
                                        self.attackTime = 1000
                                        if Rect(clone[0]) != self.bossHitBox:
                                            self.cloneFail = (self.clones[self.clones.index(clone)][0][0], self.clones[self.clones.index(clone)][0][1])
                                            del self.clones[self.clones.index(clone)]
                                else:#Blits images for other clones to trick the player, even if one of them is the real one
                                    if len(self.clones) > 3:
                                        if self.clones[self.clones.index(clone)][0][0] - 16.5 > player.x:
                                            screen.blit(self.sprite[9][3], (self.clones[self.clones.index(clone)][0][0], self.clones[self.clones.index(clone)][0][1]))
                                        elif self.clones[self.clones.index(clone)][0][0] + 43.5 < player.x:
                                            screen.blit(self.sprite[9][5], (self.clones[self.clones.index(clone)][0][0], self.clones[self.clones.index(clone)][0][1]))
                                        else:
                                            if self.clones[self.clones.index(clone)][0][1] < player.y:
                                                screen.blit(self.sprite[9][1], (self.clones[self.clones.index(clone)][0][0], self.clones[self.clones.index(clone)][0][1]))
                                            if self.clones[self.clones.index(clone)][0][1] > player.y:
                                                screen.blit(self.sprite[9][7], (self.clones[self.clones.index(clone)][0][0], self.clones[self.clones.index(clone)][0][1]))
                    except:
                        pass
                if self.attackTime == 1000:#Resets clones and becomes idle
                    self.idle = True
                    self.clones = [[], [], [], []]
                    self.cloneCounter = 0
                    self.squareX, self.squareY = self.x - 35, self.y - 35
                if self.attackTime == 1050:#Resets everything
                    self.idle = False
                    self.attackTime = 0
                    self.attackMove = randint(0,4)

            if self.attackMove == 3:#Square attack
                if self.attackTime > 2 and self.attackTime < 80:#Attacks 20, 40, 60 around the bossMage
                    if self.attackTime % 20 == 0:#Adds to the list of squares and makes the size bigger for each square
                        self.squares.append((self.squareX, self.squareY, self.squareSize))  # vertical line
                        self.squareX -= 150
                        self.squareY -= 150
                        self.squareSize += 300
                    for square in self.squares:#Blits the square and scales and draws the squares
                        squareSprite = transform.scale(self.squareSprite,(square[2], square[2]))
                        screen.blit((squareSprite), (square[0], square[1]))
                        draw.rect(self.attackSurface, GREEN, (square[0]+square[2]//11, square[1]+square[2]//11, square[2]-square[2]//6, square[2]-square[2]//6), square[2]//6)
                if self.attackTime == 80:#Resets the squares and idles
                    self.idle = True
                    self.squares.clear()
                    self.squareX, self.squareY = self.x - 35, self.y - 35
                    self.squareSize = 70
                if self.attackTime == 180:#Resets everything
                    self.idle = False
                    self.attackTime = 0
                    self.attackMove = randint(0,4)

            if self.attackMove == 4:#Orb attack
                if self.attackTime < 500:#Attacks every 10 until 490
                    if self.attackTime % 10 == 0:
                        orbRand1 = randint(0, 3)#Adds a random location from one side of the screen and a random location from a different side of the screen then resets the orbList so different locations each time
                        self.orbList.append(self.orbList.pop(orbRand1))
                        orbRand2 = randint(0, 2)
                        self.orbs.append([self.orbList[3][0], self.orbList[3][1], self.orbList[orbRand2][0], self.orbList[orbRand2][1]])
                        self.orbList = [(randint(0, 1200), -35), (-35, randint(0, 800)), (randint(0, 1200), 835),
                                        (1235, randint(0, 800))]
                    for orb in self.orbs:#Orbs move across the screen and draws and blits the orbs
                        if orb[0] > orb[2]:
                            orb[2] += 5
                        if orb[1] > orb[3]:
                            orb[3] += 5
                        if orb[0] < orb[2]:
                            orb[2] -= 5
                        if orb[1] < orb[3]:
                            orb[3] -= 5
                        draw.circle(self.attackSurface, GREEN, (orb[2], orb[3]), 25)
                        screen.blit(self.orbSprite, (orb[2] - 25, orb[3] - 25))
                if self.attackTime == 500:#Resets orbs and idles
                    self.idle = True
                    self.orbs.clear()
                if self.attackTime == 600:#Resets everything
                    self.idle = False
                    self.attackTime = 0
                    self.attackMove = randint(0,4)
# =======================================================================================================================
#same as players bullets except coming from the skeleton and tracking the player
    def enemyShoot(self, arrows):
        if self.skeletonTime % self.shootTime == 0:
            ang = atan2(player.y - self.y, player.x - self.x)
            self.projectileX, self.projectileY = cos(ang) * 5.5, sin(ang) * 5.5  # horizontal component
            arrows.append([self.x, self.y, self.projectileX, self.projectileY])

        for arrow in self.projectile[:]:  # arrows[:] is a COPY of the arrows list
            arrow[0] += arrow[2]
            arrow[1] += arrow[3]
            if arrow[0] > 1200 or arrow[0] < 0 or arrow[1] > 800 or arrow[1] < 0:  # off-screen
                self.projectile.remove(arrow)
# =======================================================================================================================
# music function
def music():
    if gameTime == 1:#Title music upon starting the game
        return "music/titlemusic.mp3"
    if game == "game":
        keys = key.get_pressed()
        if levelNum == 0 and keys[K_e] == 1 and textEnd == False and textNum == 1:  # Music on first page of tutorial level
            return "music/tutorialendmusic.mp3"
        if waveTime == 1:
            if levelNum == 1:  # Music at the beginning of each level
                return "music/level1music.mp3"
            if levelNum == 2:
                return "music/level2music.mp3"
            if levelNum == 3:
                return "music/level3music.mp3"
            if levelNum == 4:
                return "music/finalmusic1.mp3"
        if waveTime == endTime:
            if levelNum > 0 and levelNum < 4:
                return "music/bossmusic.mp3"
        if levelNum == 4 and keys[K_e] == 1 and textEnd == False:#Music on 3rd and 6th page of final level
            if textNum == 3:
                return "music/finalmusic2.mp3"
            if textNum == 6:
                return "music/tutorialendmusic.mp3"
# =======================================================================================================================
# enemy spawn function
def enemySpawn():  # Creates a function for the enemies spawning
    def wave(time, number, type):
        if waveTime == time:# Spawns if waveTime is equal to time to only spawn once
            for enemy in range(number):
                if levelNum == 1:
                    spawn = randint(0, 4)
                    if spawn == 0:  # setting locations for where the enemies will spawn on random
                        spawnX, spawnY = randint(410, 660), 770
                    elif spawn == 1:
                        spawnX, spawnY = randint(580, 850), 20
                    elif spawn == 2:
                        spawnX, spawnY = randint(833, 1000), 770
                    elif spawn == 3:
                        spawnX, spawnY = randint(25, 240), 20
                    else:
                        spawnX, spawnY = 1180, randint(390, 445)
                elif levelNum == 2:
                    spawn = randint(0, 2)
                    if spawn == 0:
                        spawnX, spawnY = 20, randint(20, 280)
                    elif spawn == 1:
                        spawnX, spawnY = randint(50, 775), 770
                    else:
                        spawnX, spawnY = randint(660, 870), 20
                elif levelNum == 3:
                    spawn = randint(0, 2)
                    if spawn == 0:
                        spawnX, spawnY = 80, randint(100, 350)
                    elif spawn == 1:
                        spawnX, spawnY = randint(860, 1120), 20
                    else:
                        spawnX, spawnY = randint(1050, 1120), 565
                elif levelNum == 4:
                    spawn = randint(0, 1)
                    if spawn == 0:
                        spawnX, spawnY = randint(955, 1055), 195
                    else :
                        spawnX, spawnY = randint(125, 1055), 770
                enemies = Enemies(spawnX, spawnY, type)  # creating the enemies
                enemyList.append(enemies)  # adding it to the list
                objects.append(enemies)

# =======================================================================================================================
#decides when, how many, and what mob to spawn
    if levelNum == 0:
        if waveTime == 100:
            tutorialEnemy = Enemies(800,400, "slime")
            enemyList.append(tutorialEnemy)
            objects.append(tutorialEnemy)
    if levelNum == 1:
        wave(100, 1, "slime")
        wave(300, 4, "slime")
        wave(500, 2, "zombie")
        wave(700, 2, "zombie")
        wave(1000, 4, "zombie")
        wave(1400, 2, "bomber")
        wave(1600, 3, "zombie")
        wave(1900, 5, "slime")
        wave(2500, 3, "zombie")
        wave(2900, 2, "bomber")
        wave(3100, 1, "bossZombie")
    if levelNum == 2:
        wave(100, 4, "slime")
        wave(300, 1, "bomber")
        wave(400, 3, "skeleton")
        wave(700, 2, "zombie")
        wave(800, 2, "bomber")
        wave(1400, 2, "bomber")
        wave(1600, 3, "zombie")
        wave(1900, 5, "slime")
        wave(2500, 2, "skeleton")
        wave(2900, 1, "bossBomber")
    if levelNum == 3:
        wave(100, 4, "zombie")
        wave(300, 1, "slime")
        wave(400, 2, "skeleton")
        wave(600, 1, "mage")
        wave(700, 2, "zombie")
        wave(800, 1, "skeleton")
        wave(1100, 3, "zombie")
        wave(1500, 2, "bomber")
        wave(2000, 5, "slime")
        wave(2100, 2, "bomber")
        wave(2200, 1, "skeleton")
        wave(2700, 1, "bossSkeleton")
    if levelNum == 4:
        wave(100, 1, "mage")
        wave(300, 2, "skeleton")
        wave(500, 3, "bomber")
        wave(700, 4, "zombie")
        wave(1000, 5, "slime")
        if textNum == 4:
            finalBoss = Enemies(589, 35, "bossMage")
            enemyList.append(finalBoss)
            objects.append(finalBoss)

# =======================================================================================================================
running = True  # Creates a boolean for the program running in general
player = Player(600,400)  # Instantiates the player class and its default location (centre of the screen) and its default direction
objects = [player]  # Creates a list of objects for use and at default contains the player object
while running:  # while running loop
    init()  # initialize music
    mb = mouse.get_pressed()  # get mouse button
    for evt in event.get():
        if evt.type == QUIT:
            running = False
        elif evt.type == MOUSEBUTTONDOWN:
            if evt.button == 1:
                click = False  # checking if you click once
        if evt.type == KEYDOWN:
            if textEnd == False:
                keys = key.get_pressed()  # checking for keyboard
                if keys[K_e] == 1:
                    textNum += 1
    mx, my = mouse.get_pos()  # mouse position
    if gameTime < 3:
        gameTime += 1
    if music() != None:  # plays the music forever until music function does not return None again
        mixer.music.load(music())
        mixer.music.play(-1)
# =======================================================================================================================
#All the rectangles used
    startRect = Rect(205, 400, 305, 100)
    controlRect = Rect(230, 560, 255, 70)
    nextRect = Rect(1050, 700, 100, 70)
    restartGame = Rect(340, 610, 550, 100)
    endhealth = Rect(330, 480, 570, 100)
    timeRect = Rect(330, 350, 570, 100)
    backRect = Rect(1050, 700, 100, 70)
    unPause = Rect(450, 320, 250, 100)
    controlRect2 = Rect(465, 460, 215, 50)
    restartLevel = Rect(430, 550, 290, 50)
    restartGame2 = Rect(430, 630, 290, 50)
    textRect = Rect(300, 680, 550, 50)
    textRect2 = Rect(350, 680, 410, 50)
# =======================================================================================================================
#restarting the level makes certain variables default
    if levelRestart == True:
        game = "game"
        if levelNum == 0:
            textEnd = False
        else:
            textEnd = True
        textNum = 0
        player.x = 600
        player.y = 400
        waveTime = 0
        startTime = 100
        gameTime = 1
        enemyList = []
        objects = [player]
        player.health = 5
        weaponGet = False
        levelRestart = False
# =======================================================================================================================
# re starts the game and sends you to the title screen makes certain variables default
    if gameRestart == True:
        page = 0
        player.weapon = "knife"
        levelNum = 0
        player.x = 600
        player.y = 400
        waveTime = 0
        startTime = 100
        gameTime = 0
        enemyList = []
        objects = [player]
        game = "start"
        textNum = 0
        textEnd = False
        gameRestart = False
# =======================================================================================================================
    if game == "start":  # opening screen
        col1 = BLACK
        col2 = BLACK  # loading all the images and text
        if startRect.collidepoint(mx,my):
            col1 = WHITE
        if controlRect.collidepoint(mx,my):
            col2 = WHITE
        screen.blit(image.load("screens/titlescreen.png").convert(),(0,0))
        draw.rect(screen, RED, startRect)
        draw.rect(screen, col1, startRect,5)
        draw.rect(screen, RED, controlRect)
        draw.rect(screen, col2, controlRect, 5)
        text = ["START","CONTROLS"]
        word1 = font1.render(text[0], True, col1)
        word2 = font2.render(text[1], True, col2)
        screen.blit(word1, (265, 425))
        screen.blit(word2, (255, 580))
        if mb[0] == 1 and startRect.collidepoint(mx,my):  # takes you to the loading screen
            game = "loading"
        elif mb[0] == 1 and controlRect.collidepoint(mx, my):  # takes you to the control screen
            game = "controls"
# =======================================================================================================================
# ending game screen
    elif game == "end":
        col4 = BLACK  # loading all the text and images
        col1 = BLACK
        col2 = BLACK
        end = image.load("screens/end.png").convert()
        draw.rect(screen, BLACK, (0, 0, 1200, 800))
        text = ["CONGRATULATIONS", "THE END", "TOTAL DEATHS: %i" %finalDeaths, "TOTAL TIME: %s" %(gameTime-3), "RESTART GAME"]
        word1 = font1.render(text[0], True, WHITE)
        word2 = font1.render(text[1], True, BLACK)
        word3 = font1.render(text[2], True, BLACK)
        word4 = font1.render(text[3], True, BLACK)
        word5 = font1.render(text[4], True, col4)
        screen.blit(word1, (300, 20))
        fountain = image.load("screens/fountain.png").convert()
        screen.blit(fountain,(410,200))
        draw.rect(screen, RED, nextRect)
        screen.blit(image.load("screens/next1.png"), (1050, 710))
        if nextRect.collidepoint(mx,my):
            screen.blit(image.load("screens/next2.png"),(1050,710))
            draw.rect(screen,WHITE,nextRect,5)
        if not click and nextRect.collidepoint(mx, my):  #  taking you to the next screen
            click = True
            ending = True
        if ending == True:
            screen.blit(end,(0,-100))
            draw.rect(screen, RED, restartGame)  # re starting the game
            draw.rect(screen, RED, endhealth)    # how many times u died
            draw.rect(screen, RED, timeRect)     # how long it took you to beat the game
            if restartGame.collidepoint(mx, my):
                col4 = WHITE
            if endhealth.collidepoint(mx, my):
                col1 = WHITE
            if timeRect.collidepoint(mx, my):
                col2 = WHITE
            draw.rect(screen, col4, restartGame, 5)
            draw.rect(screen, col1, endhealth, 5)
            draw.rect(screen, col2, timeRect, 5)
            screen.blit(word2,(400,20))
            screen.blit(word3, (360, 510))
            screen.blit(word5, (390, 640))
            screen.blit(word4, (360, 380))
        if mb[0] == 1 and restartGame.collidepoint(mx, my):
            gameRestart = True
# =======================================================================================================================
# text before game
    elif game == "loading":
        try:
            screen.fill(BLACK)  # getting the text
            draw.rect(screen, RED, nextRect)
            text = ["                       LONG LONG AGO........",
                    "                 IN A LAND FAR FAR AWAY......",
                    "   WAS A FOUNTAIN OF ULTIMATE POWER",
                    "AND A GREAT WARRIOR NAMED LAFANDA",
                    "             IS ON A JOURNEY TO OBTAIN IT",
                    "                       AND ITS UP TO YOU",
                    "           TO HELP HIM ACHIEVE HIS GOAL!"]
            word = font1.render(text[page], True, WHITE)
            screen.blit(word, (0, 400))
        except:
            pass
        screen.blit(image.load("screens/next1.png"),(1050,710))
        if nextRect.collidepoint(mx,my):
            screen.blit(image.load("screens/next2.png"),(1050,710))
            draw.rect(screen,WHITE,nextRect,5)
        if evt.type == MOUSEBUTTONDOWN and nextRect.collidepoint(mx,my):
            if (didGoNext == False):  # making sure you don't go through multiple pages at once
                page += 1
            didGoNext = True
            if page == 7:  # once all the text is done, start the game
                game = "game"
        if evt.type == MOUSEBUTTONUP and nextRect.collidepoint(mx,my):
            didGoNext = False
 # =======================================================================================================================
#control screen
    elif game == "controls":
        col = BLACK  # loading all the images and text
        screen.blit(image.load("screens/controls.png").convert(),(0,0))
        back = image.load("screens/back1.png")
        back2 = image.load("screens/back2.png")
        draw.rect(screen, RED, backRect)
        screen.blit(image.load("screens/back1.png"), (1050, 710))
        if backRect.collidepoint(mx, my):  # takes u to the start
            col = WHITE
            screen.blit(image.load("screens/back2.png"),(1050, 710))
        draw.rect(screen, col, backRect, 5)
        if mb[0] == 1 and backRect.collidepoint(mx, my):
            game = "start"

# =======================================================================================================================
# pause screen
    elif game == "pause":
        col1 = BLACK
        col2 = BLACK
        col3 = BLACK
        col4 = BLACK
        screen.blit(image.load("screens/titlescreenblur.png"),(0,0)) #
        draw.rect(screen, RED, unPause)
        draw.rect(screen, RED, controlRect2)
        draw.rect(screen, RED, restartLevel)
        draw.rect(screen, RED, restartGame2)
        if unPause.collidepoint(mx,my):
            col1 = WHITE
        elif controlRect2.collidepoint(mx,my):
            col2 = WHITE
        elif restartLevel.collidepoint(mx,my):
            col3 = WHITE
        elif restartGame2.collidepoint(mx,my):
            col4 = WHITE
        draw.rect(screen,col2,controlRect2,5)
        draw.rect(screen, col1, unPause, 5)
        draw.rect(screen, col3, restartLevel, 5)
        draw.rect(screen, col4, restartGame2, 5)
        text = ["PLAY", "CONTROLS", " RESTART LEVEL", "RESTART GAME"]
        word1 = font1.render(text[0], True, col1)
        word2 = font2.render(text[1], True, col2)
        word3 = font2.render(text[2], True, col3)
        word4 = font2.render(text[3], True, col4)
        screen.blit(word1, (498, 350))
        screen.blit(word2, (470, 470))
        screen.blit(word3, (427, 560))
        screen.blit(word4, (435, 640))
        if mb[0] == 1 and unPause.collidepoint(mx, my):
            game = "game"
        elif mb[0] == 1 and controlRect2.collidepoint(mx, my):
            game = "controls2"
        elif mb[0] == 1 and restartLevel.collidepoint(mx, my):
            levelRestart = True
        elif mb[0] == 1 and restartGame2.collidepoint(mx, my):
            gameRestart = True
# =======================================================================================================================
#control menu from pause screen (same as previous pause screen except the back button takes you to the pause screen)
    elif game == "controls2":
        col = BLACK
        screen.blit(image.load("screens/controls.png"),(0,0))  # loading all the images and back button
        back = image.load("screens/back1.png")
        back2 = image.load("screens/back2.png")
        draw.rect(screen, RED, backRect)
        screen.blit(image.load("screens/back1.png"), (1050, 710))
        if backRect.collidepoint(mx, my):  # highlighting
            col = WHITE
            screen.blit(image.load("screens/back2.png"),(1050, 710))
        draw.rect(screen, col, backRect, 5)
        if mb[0] == 1 and backRect.collidepoint(mx, my):
            game = "pause"  # take u to the previous screen
# =======================================================================================================================
    elif game == "game":  # if the game is being played
#timers
        if levelNum == 1:#When the last wave spawns for each level
            endTime = 3100
        if levelNum == 2:
            endTime = 2900
        if levelNum == 3:
            endTime = 2700
        if levelNum == 4:
            endTime = 1000
        if textEnd == True:
            gameTime += 1
            waveTime += 1  # Adds 1 to time every time it goes through the while Running loop if the player is done reading
# =======================================================================================================================
        if weaponGet == True:
            if levelNum == 1:
                player.weapon = "sword"
            if levelNum == 2:
                player.weapon = "bombs"
            if levelNum == 3:
                player.weapon = "bow"
# =======================================================================================================================
        screen.blit(list(backgrounds.keys())[levelNum], (0,0))  # blitting the background
# =======================================================================================================================
#pausing game
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            game = "pause"
# =======================================================================================================================
        if levelNum <4:
            portalRect = Rect(portals[list(portals.keys())[levelNum]][0], portals[list(portals.keys())[levelNum]][1], 52, 100)  # where the portals will spawn
            weaponRect = Rect(585, 402, 31, 35)  # The rect that the player needs to touch if the player wants the weapon
# =======================================================================================================================
# iterating through all the enemies
        for enemy in enemyList:
            if enemy.health == 0:  # remove the mob if it has no health
                enemyList.remove(enemy)
                objects.remove(enemy)
            dist = sqrt(abs(player.x - enemy.x) ** 2 + abs(player.y - enemy.y) ** 2)  # calculating the distance between the player and enemy
            player.collision(enemy)  # checks for collsion
            enemy.ai(player, dist)   # lets the enemies follow the player
            if enemy.collision(player):  # If anything from player touches the enemy while a mouse button is clicked, removes the enemy by removing the object
                try:
                    enemyList.remove(enemy)
                    objects.remove(enemy)
                except:
                    pass

            for arrow in enemy.projectile[:]:  # checks if the enemies arrows hit the player and if it does, hurts the player and removes the arrow
                try:
                    enemyArrowRect = Rect(arrow[0], arrow[1], 6, 6)
                    for hurtbox in player.hurtboxes:
                        if enemyArrowRect.colliderect(hurtbox):
                            enemy.projectile.remove(arrow)
                            player.invincibility = True
                except:
                    pass

            if enemy.type == "bossMage":
                if enemy.attackSurface.get_at((player.x, player.y)) == GREEN:#If the player touches an attack the Boss Mage uses, gets hurt
                    player.invincibility = True
                if enemy.cloneFail != False:#Spawns the fake mage if player hits the wrong one
                    player.sFrame = 15
                    fakeMage = Enemies(enemy.cloneFail[0], enemy.cloneFail[1], "mage")
                    enemyList.append(fakeMage)
                    objects.append(fakeMage)
# =======================================================================================================================
#if all mobs are dead
        if len(enemyList) == 0:
            if startTime <= 100 and levelNum > 0 and levelNum < 4:
                screen.blit(list(portals.keys())[levelNum-1], (600,400))

            if waveTime > endTime and levelNum < 4:
                try:
                    screen.blit(list(portals.keys())[levelNum], portals[list(portals.keys())[levelNum]])  # spawns the portal
                    textEnd = False
                except:
                    pass
                if not weaponGet and levelNum > 0:  # checking if you picked up the weapon or not, if not blits the weapon, displays info
                    screen.blit(weapons[levelNum-1],(585, 402))
                    if levelNum == 1:
                        text = ["     SWORD: press E for details",
                                "               Damage: STRONG -->",
                                "                Speed: MEDIUM -->",
                                "           Range: CLOSE RANGE -->",
                                "                     WARNING: -->",
                                "you can not return to previous weapons -->",
                                "       walk on weapon to collect ",
                                " "]
                    elif levelNum == 2:
                        text = ["     BOMBS: press E for details",
                                "                Damage: MEDIUM -->",
                                "                   Speed: SLOW -->",
                                "               Range: MID RANGE -->",
                                "                       WARNING: -->",
                                "you can not return to previous weapons -->",
                                "       walk on weapon to collect ",
                                " "]
                    elif levelNum == 3:
                        text = ["      BOW: press E for details",
                                "                   Damage: LOW -->",
                                "                    Speed: FAST -->",
                                "              Range: LONG RANGE -->",
                                "                       WARNING: -->",
                                "you can not return to previous weapons -->",
                                "       walk on weapon to collect ",
                                " "]
                    if textNum > 7:
                        textNum = 7
                    if textNum < 7:
                        draw.rect(screen, RED, textRect2)
                        draw.rect(screen, BLACK, textRect2, 5)
                        word = font3.render(text[textNum], True, WHITE)
                        screen.blit(word, (400, 700))
                for hurtbox in player.hurtboxes:
                    if waveTime > endTime:
                        if hurtbox.colliderect(portalRect):  # If player touches portal, goes to next level resets position
                            player.x = 600
                            player.y = 400
                            weaponGet = False
                            textEnd = True
                            levelNum += 1
                            player.health = 5
                            waveTime = 0
                            startTime = 0
                            textNum = 0
                            player.projectile = []
                        if hurtbox.colliderect(weaponRect):
                            weaponGet = True
            if levelNum == 4 and waveTime > endTime:#Displays the text if last wave has and no enemies on the screen or when the Boss Mage is defeated, also blits the image
                text = ["       Boss Mage: So you've finally arrived.",
                        "Boss Mage: You think you are deserving of unlimited power?",
                        "Boss Mage: Well, the power of the fountain is mine!",
                        "Boss Mage: And I will use its power to obliterate you!",
                        " ",
                        "                       Boss Mage: NOOOO!",
                        "           Boss Mage: HOW COULD THIS BE!?",
                        "Boss Mage: THE POWER WAS SUPPOSED TO ONLY BE MINE!",
                        "                       Boss Mage: CURSES!",
                        "    Unlimited power awaits beyond the door",
                        " "]
                if textNum < 4 or textNum >= 5 and textNum < 10:
                    draw.rect(screen, RED, textRect)
                    draw.rect(screen, BLACK, textRect, 5)
                    word = font3.render(text[textNum], True, WHITE)
                    screen.blit(word, (320, 700))
                if textNum < 5:
                    screen.blit(image.load("enemies/bmage1.png"), (572.5, 11.5))
                    textEnd = False
                    if textNum == 4:
                        textEnd = True
                    if textNum >= 4:
                        textNum = 4
                if textNum >= 5:
                    screen.blit(image.load("enemies/bmage9.png"), (600, 400))
                    textEnd = False
                if textNum >= 10:#Opens the door when the Boss Mage is done talking and player can end it to complete the game
                    textNum = 10
                    draw.rect(screen, BLACK, (564, 206, 76, 50))
                    if player.x >= 554 and player.x <= 649 and player.y >= 256 and player.y <= 287:
                        game = "end"
        if player.weapon == "knife":#Calls player function depending on which weapon it is
            player.knife()
        if player.weapon == "sword":
            player.sword()
        if player.weapon == "bombs":
            player.bomb()
        if player.weapon == "bow":
            player.bow(player.projectile)
        if waveTime == startTime:  # If 100 frames have passed by, begin spawning the enemies
            enemySpawn()
            startTime += 100
# =======================================================================================================================
#text that says when the game will commence
        if levelNum == 0:
            text = ["         Before you begin, press E to continue",
                    "                            Use WASD to move",
                    "                       Use left click to attack",
                    "                            Aim with the cursor",
                    "  Show what you've learned by beating this slime",
                    " "]
            if textNum < 5:
                draw.rect(screen, RED, textRect)
                draw.rect(screen, BLACK, textRect, 5)
                word = font3.render(text[textNum], True, WHITE)
                screen.blit(word, (400, 700))
            if textNum == 5:
                textEnd = True
        if levelNum == 4:
            if textNum == 4 and len(enemyList) > 0:#Sets up text page when Boss Mage spawns
                textNum = 5
            if textNum == 5 and len(enemyList) == 0:#Displays the 5th text page if Boss Mage is killed
                textEnd = False
    #=======================================================================================================================
# health stuff
        text = ["%s" %(gameTime-3),"X%i" % totalDeaths]  # loading all the text and images
        word = font2.render(text[0], True, BLACK)
        word2 = font2.render(text[1], True, BLACK)
        screen.blit(word,(0,760))
        screen.blit(image.load("screens/lives.png"),(1080,0))
        screen.blit(word2, (1145,10))
        for i in range(player.health):  # blitting the players health
            screen.blit(image.load("screens/heart.png"),(0+i*60,0))
        if player.health == 0:  # if the player looses all 3 hearts restart the level
            levelRestart = True
            totalDeaths -= 1
            finalDeaths += 1
            textNum = 0
        if totalDeaths == 0:
            levelNum = 0
            gameRestart = True
            totalDeaths = 5
            textNum = 0
# =======================================================================================================================
        for object in objects:  # For all the objects, it renders them on to the screen
            object.render()
        player.movement()  # Calls the player movement function so the player can move
# =======================================================================================================================
    display.flip()  # Puts stuff on screen
    clock.tick(60)  # Makes the program run at 60 frames per second
quit()
