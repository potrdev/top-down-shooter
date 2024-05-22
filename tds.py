import pygame as pg
import random
import math
import time as t

#Settings
winx = 700
winy = 700
FPS = 240

pg.init()
pg.font.init()

font = pg.font.SysFont("mont.ttf", 90)

#IMAGES
bulletImage = pg.image.load("bullet.png")
enemyImage = pg.image.load("enemy.png")
playerImage = pg.image.load("player.png")

#FUNCTIONS
def randomSpawn():
  if random.randint(1,2) == 1:
    return random.randint(-200, -50)
  else:
    return random.randint(700, 900)

#PLAYER
class Player:
  def __init__(self):
    self.x = winx // 2
    self.y = winy // 2
    self.speed = 3
    self.hp = 3
    self.image = pg.transform.scale(playerImage, (60,60))
  
  def draw(self, display):
    # CHATGPT
    mouse_x, mouse_y = pg.mouse.get_pos()
    rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
    rotated_image = pg.transform.rotate(self.image, angle)
    new_rect = rotated_image.get_rect(center=self.image.get_rect(topleft=(self.x - 20, self.y - 5)).center)
    display.blit(rotated_image, new_rect.topleft)
  
class Enemy:
  def __init__(self, name, color, hp, x, y, size, speed):
    self.name = name
    self.color = color
    self.hp = hp
    self.x = x
    self.y = y
    self.size = size
    self.speed = speed
    self.hp = hp
    self.image = pg.transform.scale(enemyImage, (35,35))

  
  def chase(self, player):
    self.x += (player.x - self.x) * self.speed
    self.y += (player.y - self.y) * self.speed
    
class Bullet:
  def __init__(self, x, y, mousePos, speed, damage):
        self.x = x
        self.y = y
        self.mousePos = mousePos
        self.speed = speed
        self.damage = damage
        self.image = pg.transform.scale(bulletImage, (24, 24))

        direction_x = mousePos[0] - x
        direction_y = mousePos[1] - y

        magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
        self.dir_x = direction_x / magnitude
        self.dir_y = direction_y / magnitude
        
  def move(self):
      # Move the bullet in the direction of the mouse position
      self.x += self.dir_x * self.speed
      self.y += self.dir_y * self.speed
    
            

player = Player()

enemies = []

bullets = []
shootCooldown = 15
cooldownTimer = 0

#SHOOT
def shoot():
  newBullet = Bullet(player.x, player.y, pg.mouse.get_pos(), 15, 1)
  bullets.append(newBullet)

#SPAWNER
time = 0.5
spawnRate = 1

#GAME
display = pg.display.set_mode((winx, winy))
game = True

#COLORS
playerColor = "#57476e"
bulletColor = "#8a77a6"

#HP
normalEnemyHp = 4

while game:
  display.fill("#958ba3")
  
  cooldownTimer += 1
  
  enteties = [enemies, bullets]
  
  if player.hp <= 0:
    loseText = font.render("You died!", True, "white", None)
    display.blit(pg.transform.scale(loseText, (220, 50)), (winx // 2 - 70, winy // 2 - 20))
    pg.display.update()
    t.sleep(4)
    game = False
  
  #SPAWNER
  if time <= 60 * spawnRate:
    time += 1
  else:
    newEnemy = Enemy("Joze", "green", 3, randomSpawn(), randomSpawn(), 15, 0.010)
    enemies.append(newEnemy)
    time = 0
  
  #QUIT
  for event in pg.event.get():
    if event.type == pg.QUIT:
      game = False
  
  #INPUTS
  keys = pg.key.get_pressed()
  
  #UI
  hpText = font.render(f"{player.hp}", True, "WHITE", None)
  display.blit(hpText, (100, 25))
  
  heart = pg.image.load("heart.png")
  heart = heart.convert_alpha()
  display.blit(pg.transform.scale(heart, (80, 80)), (10,10))
  
  if keys[pg.K_w]:
    for e in enteties:
      for i in e:
        i.y += player.speed
  if keys[pg.K_s]:
    for e in enteties:
      for i in e:
        i.y -= player.speed
  if keys[pg.K_a]:
    for e in enteties:
      for i in e:
        i.x += player.speed
  if keys[pg.K_d]:
    for e in enteties:
      for i in e:
        i.x -= player.speed
  if keys[pg.K_SPACE]:
    if cooldownTimer >= shootCooldown:
      shoot()
      cooldownTimer = 0
  
  #ENEMIES
  for enemy in enemies:
    enemy.chase(player)
    display.blit(enemy.image, (enemy.x, enemy.y))
    pg.draw.rect(display, "#5d4d73", (enemy.x - 17, enemy.y - 20, (normalEnemyHp * 18),16))
    pg.draw.rect(display, "#7e6b99", (enemy.x - 10, enemy.y - 15, (enemy.hp * 19),8))
    #pg.draw.circle(display, (0, abs(enemy.hp * 80), 0), (enemy.x, enemy.y), enemy.size) 
    
  #BULLETS
  for bullet in bullets:
    bullet.move()
    #pg.draw.circle(display, bulletColor, (bullet.x, bullet.y), 10)
    #COLLISION
    display.blit(bullet.image, (bullet.x, bullet.y))
    for enemy in enemies:
      if enemy.x <= bullet.x and enemy.x + 45 >= bullet.x and enemy.y <= bullet.y and enemy.y + 45 >= bullet.y:
        bulletInList = bullets.index(bullet)
        enemyInList = enemies.index(enemy)
        
        if bullets.count(bullets[bulletInList]) >= 1:
          bullets[bulletInList].x += 1000
          bullets.pop(bulletInList)
        if enemies.count(enemies[enemyInList]) >= 1:
          enemies[enemyInList].hp -= bullet.damage
          if enemies[enemyInList].hp <= 0:
            enemies.pop(enemyInList)
  
  for enemy in enemies:
    if enemy.x >= player.x - 40 and enemy.x <= player.x + 40 and enemy.y >= player.y - 40 and enemy.y <= player.y + 40:
        player.hp -= 1
        enemy.x += 1000
        enemies.pop(enemies.index(enemy))    
  
  player.draw(display)
  #pg.draw.circle(display, playerColor, (player.x, player.y), 25)
  pg.time.Clock().tick(FPS)
  pg.display.update()