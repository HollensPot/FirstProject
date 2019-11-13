# import sys
# import pygame
# from bullet import Bullet
# from alien import Alien
#
#
# def check_keydown_events(event, ai_settings, screen, ship, bullets):
#     if event.key == pygame.K_RIGHT:
#         ship.moving_right = True
#     elif event.key == pygame.K_LEFT:
#         ship.moving_left = True
#     elif event.key == pygame.K_SPACE:
#         fire_bullet(ai_settings, screen, ship, bullets)
#     elif event.key == pygame.K_q:
#         sys.exit()
#
#
# def fire_bullet(ai_settings, screen, ship, bullets):
#     if len(bullets) < ai_settings.bullets_allowed:
#         new_bullet = Bullet(ai_settings, screen, ship)
#         bullets.add(new_bullet)
#
#
# def check_keyup_events(event, ship):
#     if event.key == pygame.K_RIGHT:
#         ship.moving_right = False
#     elif event.key == pygame.K_LEFT:
#         ship.moving_left = False
#
#
# def check_events(ai_settings, screen, ship, bullets):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         elif event.type == pygame.KEYDOWN:
#             check_keydown_events(event, ai_settings, screen, ship, bullets)
#         elif event.type == pygame.KEYUP:
#             check_keyup_events(event, ship)
#
#
# def update_screen(ai_settings, screen, ship, aliens, bullets):
#     screen.fill(ai_settings.bg_color)
#     for bullet in bullets.sprites():
#         bullet.draw_bullet()
#     ship.blitme()
#     aliens.draw(screen)
#     pygame.display.flip()
#
#
# def update_bullets(aliens,bullets):
#     bullets.update()
#     for bullet in bullets.copy():
#         if bullet.rect.bottom <= 0:
#             bullets.remove(bullet)
#     collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
#     if len(aliens) == 0:
#         bullets.empty()
#         create_fleet(ai_settings, screen, ship, aliens)
#
#
# def get_number_aliens_x(ai_settings, alien_width):
#     available_space_x = ai_settings.screen_width - 2 * alien_width
#     number_aliens_x = int(available_space_x / (2 * alien_width))
#     return number_aliens_x
#
#
# def create_alien(ai_settings, screen, aliens, alien_number, row_number):
#     alien = Alien(ai_settings, screen)
#     alien_width = alien.rect.width
#     alien.x = alien_width + 2 * alien_width * alien_number
#     alien.rect.x = alien.x
#     alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
#     aliens.add(alien)
#
#
# def create_fleet(ai_settings, screen, ship, aliens):
#     alien = Alien(ai_settings, screen)
#     number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
#     number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
#     for row_number in range(number_rows):
#         for alien_number in range(number_aliens_x):
#             create_alien(ai_settings, screen, aliens, alien_number, row_number)
#
#
# def get_number_rows(ai_settings, ship_height, alien_height):
#     available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
#     number_rows = int(available_space_y / (2 * alien_height))
#     return number_rows
#
#
# def check_fleet_edges(ai_settings, aliens):
#     for alien in aliens.sprites():
#         if alien.check_edges():
#             change_fleet_direction(ai_settings, aliens)
#             break
#
#
# def change_fleet_direction(ai_settings, aliens):
#     for alien in aliens.sprites():
#         alien.rect.y += ai_settings.fleet_drop_speed
#     ai_settings.fleet_direction *= -1
#
#
# def update_aliens(ai_settings, aliens):
#     check_fleet_edges(ai_settings, aliens)
#     aliens.update()
#
#
#
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    # 监视键盘和鼠标事件
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # 关闭窗口退出
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置计分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''更新屏幕上的图片，并切换到新屏幕'''
    screen.fill(ai_settings.bg_color)  # 设置背景颜色
    ship.blitme()  # 绘制飞船
    aliens.draw(screen)
    # 循环子弹组里面的元素，进行绘制 为空时不执行
    for bullet in bullets.sprites():
        bullet.draw_bullet()  # 绘制子弹
    # 显示得分
    sb.show_score()
    # 如果游戏处于非活跃状态，就显示Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 显示最新屏幕，擦拭旧屏幕
    pygame.display.flip()
    # print('1')


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''更新子弹位置，删除子弹'''
    bullets.update()  # 子弹组每个成员执行self.update()操作
    for bullet in bullets.sprites():
        if bullet.rect.bottom <= 0:  # 子弹出界 删除
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应外星人和子弹的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人,加快游戏进度节奏
        bullets.empty()
        ai_settings.increase_speed()

        # 提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def update_ship(ship):
    ship.update()


def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一个子弹对象 加入到子弹组
    if len(bullets) < ai_settings.bullets_allowed:  # 子弹少于允许值时再生成
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_aliens(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当期行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_aliens(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的运动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕低端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """检查是否有外星人到达屏幕低端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    # 检查是否有外星人到达屏幕低端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高纪录"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


