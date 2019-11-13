# import sys
# import pygame
# from pygame.sprite import Group
# from settings import Settings
# from ship import Ship
# from alien import Alien
# import game_functions as gf
#
#
# def run_game():
#     pygame.init()
#     ai_settings = Settings()
#     screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
#     pygame.display.set_caption("Alien Invasion")
#     ship = Ship(ai_settings, screen)
#     bullets = Group()
#     aliens = Group()
#     gf.create_fleet(ai_settings, screen, ship, aliens)
#
#     while True:
#         gf.check_events(ai_settings, screen, ship, bullets)
#         ship.update()
#         gf.update_bullets(aliens, bullets)
#         gf.update_aliens(ai_settings, aliens)
#         gf.update_screen(ai_settings, screen, ship, aliens, bullets)
# run_game()
import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from pygame.sprite import Group
import game_functions as gf
from scoreboard import Scoreboard


def run_game():
    pygame.init()  # 初始化背景设置
    ai_settings = Settings()  # 全局设置

    screen = pygame.display.set_mode(  # 创建screen显示窗口
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption('Alien Invasion')  # 标题
    # 新建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例,并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建飞船
    ship = Ship(ai_settings, screen)
    # 创建子弹编组
    bullets = Group()

    # 创建一个外星人
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 开始游戏主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            # 移动飞船
            gf.update_ship(ship)
            # 更新子弹位置
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            # 更新外星人
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        # 更新屏幕
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()