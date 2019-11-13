# import pygame
# from pygame.sprite import Sprite
#
#
# class Bullet(Sprite):
#     def __init__(self, ai_settings, screen, ship):
#         super(Bullet, self).__init__()
#         self.screen = screen
#         self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
#         self.rect.centerx = ship.rect.centerx
#         self.rect.top = ship.rect.top
#         self.y = float(self.rect.y)
#         self.color = ai_settings.bullet_color
#         self.speed_factor = ai_settings.bullet_speed_factor
#
#     def update(self):
#         self.y -= self.speed_factor
#         self.rect.y = self.y
#
#     def draw_bullet(self):
#         pygame.draw.rect(self.screen, self.color, self.rect)
import pygame
from pygame.sprite import Sprite
import time

class Bullet(Sprite):
  '''飞船子弹进行管理'''

  def __init__(self,ai_settings,screen,ship):
    super(Bullet,self).__init__()
    self.screen = screen

    # 创建子弹矩形初始位置（0,0,3,15）分别对应lef，top，宽，高
    self.rect = pygame.Rect(0,0,
    ai_settings.bullet_width, ai_settings.bullet_height)

    self.rect.centerx = ship.rect.centerx # 设置中心点x轴坐标跟飞船一致
    self.rect.top = ship.rect.top     # 设置y轴坐标顶部跟飞船一致

    # 设置成小数进行计算
    self.top = float(self.rect.top)

    self.color = ai_settings.bullet_color
    self.speed_factor = ai_settings.bullet_speed_factor

  def update(self):
    self.top -=self.speed_factor
    self.rect.top = self.top
    print(self.rect.top)

  def draw_bullet(self):
    pygame.draw.rect(self.screen,self.color,self.rect)