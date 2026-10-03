"""
AI-контроллер для управления змейкой в режиме «Гонка с ИИ».

Простой жадный алгоритм:
1. Ищет безопасные направления (не столкновение с собой/врагом).
2. Предпочитает то, что приближает к яблоку.
3. Если безопасных нет — случайное направление.
"""

import random

from settings import CELL_SIZE, DIRECTIONS, DIRECTION_DELTAS


class AIController:
    """
    Управляет AI-змейкой.

    Атрибуты:
        snake: змейка, которой управляем.
        apple: цель (яблоко).
        other_snake: змейка игрока (для проверки столкновений).
    """

    def __init__(self, snake, apple, other_snake):
        """
        Args:
            snake: управляемая змейка (AI).
            apple: объект Apple.
            other_snake: змейка игрока.
        """
        self.snake = snake
        self.apple = apple
        self.other_snake = other_snake

    def _new_head(self, direction):
        """
        Возвращает позицию головы при движении в заданном направлении.

        Args:
            direction: одно из DIRECTIONS.

        Returns:
            (x, y) — координаты новой головы.
        """
        dx, dy = DIRECTION_DELTAS[direction]
        head_x, head_y = self.snake.body[-1]
        return (head_x + dx, head_y + dy)

    def _is_safe(self, position):
        """
        Проверяет, безопасна ли клетка для хода.

        Клетка небезопасна, если занята телом своей змейки
        (кроме хвоста — он уйдёт при движении) или телом врага.

        Args:
            position: координаты клетки.

        Returns:
            True, если в клетку можно двигаться.
        """
        # Столкновение со своим телом (кроме последнего сегмента — хвоста)
        if position in self.snake.body[:-1]:
            return False
        # Столкновение с врагом
        if self.other_snake and position in self.other_snake.body:
            return False
        return True

    def _safe_directions(self):
        """
        Возвращает список безопасных направлений.

        Returns:
            Список направлений из DIRECTIONS, ведущих в свободную клетку.
        """
        return [d for d in DIRECTIONS if self._is_safe(self._new_head(d))]

    def _directions_towards_apple(self):
        """
        Возвращает направления, приближающие змейку к яблоку.

        Сначала — по горизонтали (если есть смещение), затем по вертикали.
        Используется как приоритет при выборе хода.

        Returns:
            Список предпочтительных направлений.
        """
        head_x, head_y = self.snake.body[-1]
        dx = self.apple.position[0] - head_x
        dy = self.apple.position[1] - head_y

        preferred = []
        if dx > 0:
            preferred.append("RIGHT")
        elif dx < 0:
            preferred.append("LEFT")
        if dy > 0:
            preferred.append("DOWN")
        elif dy < 0:
            preferred.append("UP")
        return preferred

    def update_direction(self):
        """
        Обновляет направление змейки перед ходом.

        Логика:
        1. Если нет безопасных направлений — поворот случайный (обречены).
        2. Иначе — первое безопасное направление из предпочтительных.
        3. Если ни одно из предпочтительных не безопасно — случайное безопасное.
        """
        safe = self._safe_directions()

        if not safe:
            self.snake.turn(random.choice(DIRECTIONS))
            return

        for direction in self._directions_towards_apple():
            if direction in safe:
                self.snake.turn(direction)
                return

        self.snake.turn(random.choice(safe))
