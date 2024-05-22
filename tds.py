import pygame as pg
import random
import math

#Settings
winx = 700
winy = 700
FPS = 60

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
shootCooldown = 30
cooldownTimer = 0

#SHOOT
def shoot():
  newBullet = Bullet(player.x, player.y, pg.mouse.get_pos(), 15, 1)
  bullets.append(newBullet)

#SPAWNER
time = 0
spawnRate = 2

#GAME
display = pg.display.set_mode((winx, winy))
game = True

while game:
  display.fill("White")
  pg.time.Clock().tick(FPS)
  
  cooldownTimer += 1
  
  enteties = [enemies, bullets]
  
  #SPAWNER
  if time <= 60 * spawnRate:
    time += 1
  else:
    newEnemy = Enemy("Joze", "green", 3, randomSpawn(), randomSpawn(), 15, 0.005)
    enemies.append(newEnemy)
    time = 0
  
  #QUIT
  for event in pg.event.get():
    if event.type == pg.QUIT:
      game = False
  
  #INPUTS
  keys = pg.key.get_pressed()
  
  if keys[pg.K_w]:
    backgroundPos[1] += player.speed
    for e in enteties:
      for i in e:
        i.y += player.speed
  if keys[pg.K_s]:
    backgroundPos[1] -= player.speed
    for e in enteties:
      for i in e:
        i.y -= player.speed
  if keys[pg.K_a]:
    backgroundPos[0] += player.speed
    for e in enteties:
      for i in e:
        i.x += player.speed
  if keys[pg.K_d]:
    backgroundPos[0] -= player.speed
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
    pg.draw.circle(display, (0, abs(enemy.hp * 80), 0), (enemy.x, enemy.y), enemy.size) 
    
  #BULLETS
  for bullet in bullets:
    bullet.move()
    pg.draw.circle(display, "blue", (bullet.x, bullet.y), 10)
    #COLLISION
    for enemy in enemies:
      if enemy.x <= bullet.x and enemy.x + 45 >= bullet.x and enemy.y <= bullet.y and enemy.y + 45 >= bullet.y:
        bulletInList = bullets.index(bullet)
        enemyInList = enemies.index(enemy)
        
        if bullets[bulletInList]:
          bullets.pop(bulletInList)
        if enemies[enemyInList]:
          enemies[enemyInList].hp -= bullet.damage
          if enemies[enemyInList].hp <= 0:
            enemies.pop(enemyInList)
          
  
  pg.draw.circle(display, "yellow", (player.x, player.y), 25)
  pg.display.update()