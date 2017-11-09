# -*- coding: utf-8 -*-
# @Author     : Freedomly
# @Date       : 2017/11/9 19:44
# @Email      : Freedom.JLF@gmail.com
# @File       : scoreboard.py
# @Software   : PyCharm Community Edition
# @Description: scoreboard


import pygame
from pygame.sprite import Group

from ship import Ship


class Scoreboard():
    """
    显示得分信息的类
    """

    def __init__(self, ai_settings, screen, stats):
        """
        初始化显示得分涉及的属性
        :param ai_settings: 游戏设置
        :param screen: 目标屏幕
        :param stats: 游戏统计信息
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 36)

        # 准备包含分的图像
        self.prep_images()

    def prep_score(self):
        """
        将得分转换为一幅渲染的图像
        :return:
        """
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """
        将最高分转换为渲染的图像
        :return:
        """
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,
                                                 self.ai_settings.bg_color)
        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """
        将当前等级转换为渲染图像
        :return:
        """
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color,
                                            self.ai_settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """
        显示还余下多少飞船
        :return:
        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.image = pygame.image.load('images/ship_1.bmp')
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_images(self):
        """
        准备包含分的图像
        :return:
        """
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def show_score(self):
        """
        显示分数
        :return:
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船
        self.ships.draw(self.screen)
