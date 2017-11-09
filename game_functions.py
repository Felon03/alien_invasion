# -*- coding: utf-8 -*-
# @Author     : Freedomly
# @Date       : 2017/11/6 20:26
# @Email      : Freedom.JLF@gmail.com
# @File       : game_functions.py
# @Software   : PyCharm Community Edition
# @Description: functions of running Alien Invasion

import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, stats, sb, ship,
                         aliens, bullets):
    """
    响应按键
    :param event: 按键事件
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        # 创建一颗子弹，并将其加入到编组bullets中
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_ESCAPE:
        exit_game(stats)


def check_keyup_events(event, ship):
    """
    响应松开
    :param event: 按键事件
    :param ship: 飞船对象
    :return:
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(ai_settings, screen, ship, bullets):
    """
    如果没有达到子弹数量上限，就发射一颗子弹
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param ship: 飞船对象
    :param bullets: 子弹对象
    :return:
    """
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    开始游戏
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    # 重置游戏设置
    ai_settings.initialize_dynamic_settings()

    # 隐藏光标
    pygame.mouse.set_visible(False)

    # 重置游戏信息
    stats.reset_stats()
    stats.game_active = True

    # 重置记分牌图像
    sb.prep_images()

    # 清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人，并让飞船居中
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """
    在玩家单机Play按钮时开始游戏
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param play_button: 开始按钮
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :param mouse_x: 鼠标指针x坐标位置
    :param mouse_y: 鼠标指针y坐标位置
    :return:
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets):
    """
    响应按键和鼠标事件
    :return:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game(stats)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship,
                                 aliens, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """
    更新屏幕上的图像，并切换到新屏幕
    :param ai_settings: 设置属性
    :param screen: 目标屏幕
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :param play_button: 开始按钮对象
    :return:
    """
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    更新子弹的位置
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    # 更新子弹位置
    bullets.update()

    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """
    检查是否有子弹击中了外星人
    如果是这样，就删除相应的子弹和外星人 两个True表示删除发生碰撞的子弹和外星人
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        # 确保每消灭一个外星人都记分
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
        # stats.score += ai_settings.alien_points
        # sb.prep_score()

    if len(aliens) == 0:
        # 删除现有的子弹, 加快游戏节奏，并新建一群外星人
        start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    相应被外星人撞到的飞船
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    # print(stats.ships_left)
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    检查是否有外星人到达了屏幕底端
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    更新外星人位置
    :param ai_settings: 游戏设置
    :param screen: 屏幕对象
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # print("Ship hit!!!")
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, screen, stats, ship, aliens,
                        bullets)


def check_fleet_edges(ai_settings, aliens):
    """
    有外星人到达边缘时采取相应措施
    :param ai_settings: 游戏设置
    :param aliens: 外星人对象
    :return:
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """
    将整群外星人下移，并改变他们的方向
    :param ai_settings: 游戏设置
    :param aliens: 外星人对象
    :return:
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_number_aliens_x(ai_settings, alien_width):
    """
    计算每行可容纳多少个外星人
    :param ai_settings: 游戏设置
    :param alien_width: 外星人图片的宽度
    :return:
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """
    计算屏幕可容纳多少外星人
    :param ai_settings: 游戏设置
    :param ship_height: 飞船的高度
    :param alien_height: 外星人的高度
    :return: 课容纳外星人的行数
    """
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - (2 * ship_height))
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    创建一个外星人并将其放在当前行
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param aliens: 外星人对象
    :param alien_number: 外星人编号
    :param row_number: 外星人行号
    :return:
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """
    创建外星人群
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :return:
    """
    # 创建一个外星人，并计算一行可容纳都少个外星人
    # 外星人的间距为外星人的宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建第多行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建第一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_high_score(stats, sb):
    """
    检查是否诞生了新的最高分
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :return:
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def exit_game(stats):
    """
    推出游戏
    :param stats: 游戏统计信息
    :return:
    """
    with open('score/high_score.txt', 'w') as f:
        f.write(str(stats.high_score))
    sys.exit()


def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    删除现有的子弹, 加快游戏节奏，并新建一群外星人
    :param ai_settings: 游戏设置
    :param screen: 目标屏幕
    :param stats: 游戏统计信息
    :param sb: 记分牌
    :param ship: 飞船对象
    :param aliens: 外星人对象
    :param bullets: 子弹对象
    :return:
    """
    bullets.empty()
    ai_settings.increase_speed()

    # 提高等级
    stats.level += 1
    sb.prep_level()

    create_fleet(ai_settings, screen, ship, aliens)
