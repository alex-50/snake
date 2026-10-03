"""
Змейка игрока или ИИ: тело, движение, повороты, отрисовка.
"""

import pygame

from settings import CELL_SIZE, HEAD_COLOR, OPPOSITE, DIRECTION_DELTAS


class Snake:
    """
    Змейка — управляемая сущность (игрок или ИИ).

    Тело хранится как список координат сегментов (кортежи (x, y)).
    Последний элемент списка — голова. Первый — хвост.
    """

    def __init__(self, color, x, y):
        """
        Создаёт змейку с начальной длиной 3 сегмента.

        Args:
            color: базовый цвет змейки (кортеж RGB).
            x, y: координаты начальной головы (остальные сегменты — влево).
        """
        self.color = color
        # Более тёмный оттенок для чередования сегментов
        self.dark_color = (color[0] // 2, color[1] // 2, color[2] // 2)
        self.head_color = HEAD_COLOR
        self.body = [
            (x, y),
            (x + CELL_SIZE, y),
            (x + 2 * CELL_SIZE, y),
        ]
        self.direction = "RIGHT"

    def move(self):
        """
        Двигает змейку на одну клетку в текущем направлении.

        Добавляет новую голову в конец body. Удаление хвоста —
        ответственность вызывающего кода (в game_loop), потому что
        при съедании яблока хвост не удаляется (змейка растёт).
        """
        dx, dy = DIRECTION_DELTAS[self.direction]
        head_x, head_y = self.body[-1]
        self.body.append((head_x + dx, head_y + dy))

    def turn(self, direction):
        """
        Поворачивает змейку, если направление не противоположно текущему.

        Args:
            direction: одно из "UP", "DOWN", "LEFT", "RIGHT".
        """
        if direction != OPPOSITE[self.direction]:
            self.direction = direction

    def draw(self, screen):
        """
        Отрисовывает змейку сегментами.

        Голова — HEAD_COLOR, чётные сегменты — основной цвет,
        нечётные — затемнённый.
        """
        for i, pos in enumerate(self.body):
            if i == len(self.body) - 1:
                color = self.head_color
            elif i % 2 == 0:
                color = self.color
            else:
                color = self.dark_color

            pygame.draw.rect(
                screen, color,
                pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE),
            )
