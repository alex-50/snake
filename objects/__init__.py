"""
Пакет игровых объектов.

Реэкспортирует публичные классы для удобного импорта:
    from objects import Snake, Apple, AIController
"""

from .snake import Snake
from .apple import Apple
from .ai_controller import AIController

__all__ = ["Snake", "Apple", "AIController"]