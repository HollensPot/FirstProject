# import pygame
#
#
# class Ship:
#     def __init__(self, ai_settings, screen):
#         self.screen = screen
#         self.ai_setting = ai_settings
#         self.image1 = pygame.image.load('images/ship.bmp')
#         # 对飞船进行缩小
#         self.image = pygame.transform.scale(self.image1, (50, 70))
#         self.rect = self.image.get_rect()
#         self.screen_rect = screen.get_rect()
#         self.rect.centerx = self.screen_rect.centerx
#         self.rect.bottom = self.screen_rect.bottom
#         self.center = float(self.rect.centerx)
#         self.moving_right = False
#         self.moving_left = False
#
#     def update(self):
#         if self.moving_right and self.rect.right < self.screen_rect.right:
#             self.center += self.ai_setting.ship_speed_factor
#         if self.moving_left and self.rect.left > 0:
#             self.center -= self.ai_setting.ship_speed_factor
#         self.rect.centerx = self.center
#
#     def blitme(self):
#         self.screen.blit(self.image, self.rect)
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
  '''飞船所有信息'''

  def __init__(self,ai_settings,screen):
    """初始化飞船，并设置其起始位置"""
    super(Ship,self).__init__()
    self.screen=screen
    self.ai_settings = ai_settings

    # 加载飞船图片、获取外接矩形
    self.image = pygame.image.load(self.ai_settings.ship_image_path)  # 加载图片
    self.image = pygame.transform.smoothscale(self.image,(40,60))
    self.rect = self.image.get_rect()  # 获取图片外接矩形
    self.screen_rect = screen.get_rect()    #获取屏幕外接矩形

    # 将每搜新飞船放到并木底部中心
    self.rect.centerx = self.screen_rect.centerx
    self.rect.bottom = self.screen_rect.bottom
    # 设置成浮点类型
    self.center = float(self.rect.centerx)   # self.rect.centerx设置不了浮点数 只能另设置一个变量进行运算

    # 移动标志
    self.moving_right = False
    self.moving_left = False

  def blitme(self):
    '''在指定位置绘制飞船'''
    self.screen.blit(self.image,self.rect)

  def update(self):
    # 向右移动飞船
    if self.moving_right and self.rect.right < self.screen_rect.right:
      self.center +=self.ai_settings.ship_speed_factor
    # 向左移动飞船
    if self.moving_left and self.rect.left > self.screen_rect.left:
      self.center -= self.ai_settings.ship_speed_factor

    self.rect.centerx = self.center

  def center_ship(self):
    """让飞船在屏幕上居中"""
    self.center = self.screen_rect.centerx
