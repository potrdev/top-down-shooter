import pygame as pg
import random

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
  
  def chase(self, player):
    self.x += (player.x - self.x) * self.speed
    self.y += (player.y - self.y) * self.speed
            

player = Player()

enemies = []

#SPAWNER
time = 0
spawnRate = 2

#GAME
display = pg.display.set_mode((winx, winy))
game = True

while game:
  display.fill("White")
  pg.time.Clock().tick(FPS)
  
  
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
    for e in enemies:
      e.y += player.speed
  if keys[pg.K_s]:
    for e in enemies:
      e.y -= player.speed
  if keys[pg.K_a]:
    for e in enemies:
      e.x += player.speed
  if keys[pg.K_d]:
    for e in enemies:
      e.x -= player.speed
  
  #ENEMIES
  for enemy in enemies:
    enemy.chase(player)
    pg.draw.circle(display, enemy.color, (enemy.x, enemy.y), enemy.size)
  
  pg.draw.circle(display, "yellow", (player.x, player.y), 25)
  pg.display.update()