# -*- coding: utf-8 -*-
# @Author     : Freedomly
# @Date       : 2017/11/9 18:20
# @Email      : Freedom.JLF@gmail.com
# @File       : button.py
# @Software   : PyCharm Community Edition
# @Description: button class


import pygame.font


class Button():
    """
    按钮类
    """

    def __init__(self, ai_settings, screen, msg):
        """
        初始化按钮属性
        :param ai_settings: 游戏设置
        :param screen: 屏幕对象
        :param msg: 要显示的信息
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的rect对象，并使其剧中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """
        将msg渲染为图像，并使其在按钮上居中
        :param msg: 要在按钮上显示的信息
        :return:
        """
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """
        绘制一个用颜色填充的按钮，再绘制文本
        :return:
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
