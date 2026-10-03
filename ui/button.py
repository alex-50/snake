"""
Кнопка для меню и экранов игры.
"""

import os
import pygame

from utils import FONTS_DIR


class Button:
    """
    Кликабельная кнопка с текстом и hover-эффектом.

    Атрибуты:
        rect: прямоугольник кнопки (pygame.Rect).
        text: подпись на кнопке.
        color: базовый цвет.
        hover_color: цвет при наведении курсора.
        font: шрифт для отрисовки текста.
    """

    def __init__(self, x, y, width, height, text, font_size, color, hover_color):
        """
        Создаёт кнопку.

        Args:
            x, y: координаты верхнего левого угла.
            width, height: размеры кнопки.
            text: подпись.
            font_size: размер шрифта.
            color: базовый цвет фона.
            hover_color: цвет фона при наведении.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(
            os.path.join(FONTS_DIR, "PressStart2P.ttf"), font_size
        )

    def draw(self, screen):
        """
        Рисует кнопку на экране.

        Меняет цвет фона при наведении курсора.
        """
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(self.text, True, (60, 60, 60))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """
        Проверяет, кликнули ли по кнопке.

        Returns:
            True, если событие — левый клик мыши по области кнопки.
        """
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )