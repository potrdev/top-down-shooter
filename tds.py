import pygame as pg
import random

#Settings
winx = 700
winy = 700

#PLAYER
class Player:
  def __init__(self):
    self.x = winx // 2
    self.y = winy // 2
    self.speed = 0.2
    
  def move(self, axis, dir):
    if axis == "x" and dir:
      self.x += self.speed
    elif axis == "x" and not dir:
      self.x -= self.speed
    elif axis == "y" and dir:
      self.y -= self.speed
    elif axis == "y" and not dir:
      self.y += self.speed
            

player = Player()

display = pg.display.set_mode((winx, winy))

game = True

while game:
  
  display.fill("White")
  
  #QUIT
  for event in pg.event.get():
    if event.type == pg.QUIT:
      game = False
   
  #INPUTS
  keys = pg.key.get_pressed()
  
  if keys[pg.K_w]:
    player.move("y", True)
  if keys[pg.K_s]:
    player.move("y", False)
  if keys[pg.K_a]:
    player.move("x", False)
  if keys[pg.K_d]:
    player.move("x", True)
  
  pg.draw.circle(display, "yellow", (player.x, player.y), 20)
  pg.display.update()