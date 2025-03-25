import time
import random
import pygame
from settings import *


class Snake:
    def __init__(self, color, x, y):
        self.color = color
        self.dark_color = (color[0] // 2, color[1] // 2, color[2] // 2)
        self.head_color = HEAD_COLOR
        self.body = [(x, y), (x + 20, y), (x + 40, y)]
        self.direction = "RIGHT"

    def move(self):
        head = self.body[-1]
        if self.direction == "UP":
            new_head = (head[0], head[1] - 20)
        elif self.direction == "DOWN":
            new_head = (head[0], head[1] + 20)
        elif self.direction == "LEFT":
            new_head = (head[0] - 20, head[1])
        elif self.direction == "RIGHT":
            new_head = (head[0] + 20, head[1])
        self.body.append(new_head)

    def turn(self, direction):
        if (
                (self.direction == "UP" and direction != "DOWN") or
                (self.direction == "DOWN" and direction != "UP") or
                (self.direction == "LEFT" and direction != "RIGHT") or
                (self.direction == "RIGHT" and direction != "LEFT")
        ):
            self.direction = direction

    def draw(self, screen):
        """
        Отрисовка змейки
        """

        for i, pos in enumerate(self.body):
            color = self.head_color if i == len(self.body) - 1 else \
                self.color if i % 2 == 0 else self.dark_color
            pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], 20, 20))


class Apple:
    """
    Класс-яблоко
    """

    def __init__(self):
        self.position = (
            random.randint(0, SCREEN_WIDTH // 20 - 1) * 20,
            random.randint(0, SCREEN_HEIGHT // 20 - 1) * 20
        )

    def generate_new(self, snake1, snake2):
        while True:
            new_position = (
                random.randint(0, SCREEN_WIDTH // 20 - 1) * 20,
                random.randint(0, SCREEN_HEIGHT // 20 - 1) * 20
            )
            if new_position not in snake1.body and (not snake2 or new_position not in snake2.body):
                self.position = new_position
                break


class AIController:
    """
    Класс контроллера AI змейки
    """

    def __init__(self, snake, apple, other_snake):
        self.snake = snake
        self.apple = apple
        self.other_snake = other_snake

    def get_new_head(self, direction):
        """
        Возвращает новую позицию головы змейки при движении в заданном направлении
        """

        head = self.snake.body[-1]
        if direction == "UP":
            return (head[0], head[1] - 20)
        elif direction == "DOWN":
            return (head[0], head[1] + 20)
        elif direction == "LEFT":
            return (head[0] - 20, head[1])
        elif direction == "RIGHT":
            return (head[0] + 20, head[1])

    def is_safe(self, new_head):
        """
        Проверка на безопасность движения в новую позицию
        """

        # Проверка на столкновение с собой
        if new_head in self.snake.body[:-1]:
            return False
        # Проверка на столкновение с другой змейкой (если есть)
        if self.other_snake and new_head in self.other_snake.body:
            return False
        return True

    def get_safe_directions(self):
        """
        Список безопасных направлений для движения
        """

        safe_directions = []
        for direction in ["UP", "DOWN", "LEFT", "RIGHT"]:
            new_head = self.get_new_head(direction)
            if self.is_safe(new_head):
                safe_directions.append(direction)
        return safe_directions

    def get_direction_towards_apple(self):
        """
        Определяем направление, которое приблизит змейку к яблоку
        """

        head = self.snake.body[-1]
        dx = self.apple.position[0] - head[0]
        dy = self.apple.position[1] - head[1]

        preferred_directions = []
        if dx > 0:
            preferred_directions.append("RIGHT")
        elif dx < 0:
            preferred_directions.append("LEFT")
        if dy > 0:
            preferred_directions.append("DOWN")
        elif dy < 0:
            preferred_directions.append("UP")

        return preferred_directions

    def update_direction(self):
        """
        Обновление направления змейки
        """

        safe_directions = self.get_safe_directions()
        if not safe_directions:
            # Выбиреам случайное направление, когда больше некуда безопасно двигаться
            self.snake.turn(random.choice(["UP", "DOWN", "LEFT", "RIGHT"]))
            return

        preferred_directions = self.get_direction_towards_apple()

        for direction in preferred_directions:
            # Направление, которое безопасно и ближе к яблоку
            if direction in safe_directions:
                self.snake.turn(direction)
                return

        self.snake.turn(random.choice(safe_directions))
