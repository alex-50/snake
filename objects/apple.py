"""
Яблоко — цель для змеек. Появляется в случайной свободной клетке.
"""

import random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE


class Apple:
    """
    Яблоко на игровом поле.

    Позиция всегда выровнена по сетке (кратна CELL_SIZE).
    """

    def __init__(self):
        """Создаёт яблоко в случайной клетке."""
        self.position = self._random_position()

    @staticmethod
    def _random_position():
        """
        Возвращает случайную клетку на игровом поле.

        Returns:
            (x, y) — координаты клетки, выровненные по сетке.
        """
        cols = SCREEN_WIDTH // CELL_SIZE
        rows = SCREEN_HEIGHT // CELL_SIZE
        return (
            random.randrange(cols) * CELL_SIZE,
            random.randrange(rows) * CELL_SIZE,
        )

    def generate_new(self, snake1, snake2=None):
        """
        Перемещает яблоко в случайную свободную клетку.

        Ищет позицию, не занятую ни одной из змеек.

        Args:
            snake1: обязательная змейка (игрок).
            snake2: вторая змейка (ИИ) или None.
        """
        while True:
            pos = self._random_position()
            if pos not in snake1.body and (snake2 is None or pos not in snake2.body):
                self.position = pos
                return
