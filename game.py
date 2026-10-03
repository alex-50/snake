"""
Основной класс игры — оркестратор.

Отвечает за:
- инициализацию pygame и загрузку ресурсов;
- главное меню;
- игровой цикл (классический режим и гонка с ИИ);
- экран завершения игры с рекордами.

Игровые объекты (Snake, Apple, AIController) — в пакете objects.
UI-элементы (Button) — в пакете ui.
Работа с рекордами — в records.py.
"""

import glob
import os
import random
import sys
import time

import pygame

from objects import Snake, Apple, AIController
from ui import Button
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, FPS,
    GREEN, BLUE, RED,
    PLAYER_START_X, PLAYER_START_Y, AI_START_X, AI_START_Y,
    BUTTON_HEIGHT_LARGE, BUTTON_HEIGHT_SMALL,
    BUTTON_WIDTH_LARGE, BUTTON_WIDTH_MEDIUM, BUTTON_WIDTH_SMALL,
    MENU_BUTTON_TOP, MENU_BUTTON_MIDDLE, MENU_BUTTON_BOTTOM_MARGIN,
    THEMES,
)
from utils import FONTS_DIR, SOUNDS_DIR
from records import load_records, save_records


class Game:
    """
    Основной класс игры.

    Управляет окном, ресурсами, меню, игровым процессом
    и экраном рекордов.
    """

    def __init__(self):
        """Инициализирует pygame, окно, шрифт, звуки."""
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        self.sound_enabled = True
        self.dark_theme = True

        # Загрузка основного шрифта
        try:
            self.font = pygame.font.Font(
                os.path.join(FONTS_DIR, "PressStart2P.ttf"), 24
            )
        except FileNotFoundError:
            print(f"Шрифт не найден: {os.path.join(FONTS_DIR, 'PressStart2P.ttf')}")
            pygame.quit()
            sys.exit(1)

        # Инициализация микшера и загрузка списка мелодий
        pygame.mixer.init()
        self.music_files = glob.glob(os.path.join(SOUNDS_DIR, "*.mp3"))

        if not self.music_files:
            print(f"Звуки не найдены в {SOUNDS_DIR}")
            pygame.quit()
            sys.exit(1)

    # ============================================================
    # ВСПОМОГАТЕЛЬНОЕ
    # ============================================================

    def _quit(self):
        """Корректно завершает приложение (закрывает pygame и выходит)."""
        pygame.quit()
        sys.exit(0)

    def _theme(self):
        """
        Возвращает палитру текущей темы.

        Returns:
            Словарь с ключами background, grid, button, button_hover, text, text_accent.
        """
        return THEMES["dark" if self.dark_theme else "light"]

    def _draw_grid(self):
        """Рисует сетку на игровом поле (используется в меню и в игре)."""
        grid_color = self._theme()["grid"]
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)

    # ============================================================
    # МУЗЫКА
    # ============================================================

    def play_random_music(self):
        """Запускает случайную мелодию из папки sounds по кругу."""
        if self.sound_enabled and self.music_files:
            pygame.mixer.music.load(random.choice(self.music_files))
            pygame.mixer.music.play(-1)

    def toggle_sound(self):
        """Переключает звук: вкл/выкл (пауза/возобновление музыки)."""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def toggle_theme(self):
        """Переключает тёмную/светлую тему."""
        self.dark_theme = not self.dark_theme

    # ============================================================
    # МЕНЮ
    # ============================================================

    def _menu_buttons(self):
        """
        Создаёт кнопки для главного меню.

        Returns:
            Список объектов Button в порядке отрисовки.
        """
        theme = self._theme()
        button_color = theme["button"]
        hover_color = theme["button_hover"]

        classic = Button(
            x=SCREEN_WIDTH // 2 - BUTTON_WIDTH_LARGE // 2,
            y=MENU_BUTTON_TOP,
            width=BUTTON_WIDTH_LARGE, height=BUTTON_HEIGHT_LARGE,
            text="Классический режим", font_size=24,
            color=button_color, hover_color=hover_color,
        )
        race = Button(
            x=SCREEN_WIDTH // 2 - BUTTON_WIDTH_MEDIUM // 2,
            y=MENU_BUTTON_MIDDLE,
            width=BUTTON_WIDTH_MEDIUM, height=BUTTON_HEIGHT_LARGE,
            text="Гонка с ИИ", font_size=24,
            color=button_color, hover_color=hover_color,
        )
        sound = Button(
            x=0, y=SCREEN_HEIGHT - MENU_BUTTON_BOTTOM_MARGIN,
            width=BUTTON_WIDTH_SMALL, height=BUTTON_HEIGHT_SMALL,
            text="Звук: Вкл" if self.sound_enabled else "Звук: Выкл",
            font_size=14,
            color=button_color, hover_color=hover_color,
        )
        theme_btn = Button(
            x=0, y=SCREEN_HEIGHT - MENU_BUTTON_BOTTOM_MARGIN // 2,
            width=BUTTON_WIDTH_SMALL, height=BUTTON_HEIGHT_SMALL,
            text="Тема: Тёмная" if self.dark_theme else "Тема: Светлая",
            font_size=14,
            color=button_color, hover_color=hover_color,
        )
        return [classic, race, sound, theme_btn]

    def draw_menu(self):
        """
        Рисует главное меню.

        Returns:
            Список кнопок (для обработки кликов).
        """
        self.screen.fill(self._theme()["background"])
        self._draw_grid()

        buttons = self._menu_buttons()
        for button in buttons:
            button.draw(self.screen)
        return buttons

    def main_menu(self):
        """
        Главное меню игры.

        Запускает музыку и входит в цикл обработки кликов по кнопкам.
        Выход — только через закрытие окна.
        """
        self.play_random_music()

        while True:
            buttons = self.draw_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()

                for button in buttons:
                    if not button.is_clicked(event):
                        continue

                    if button.text == "Классический режим":
                        self.play_random_music()
                        self.game_loop("classic")
                    elif button.text == "Гонка с ИИ":
                        self.play_random_music()
                        self.game_loop("race")
                    elif button.text.startswith("Звук:"):
                        self.toggle_sound()
                    elif button.text.startswith("Тема:"):
                        self.toggle_theme()

    # ============================================================
    # ИГРОВОЙ ЦИКЛ
    # ============================================================

    def game_loop(self, mode):
        """
        Игровой цикл для выбранного режима.

        Args:
            mode: "classic" (один игрок) или "race" (гонка с ИИ).
        """
        # Змейка игрока: в режиме гонки — зелёная, в классике — случайный цвет
        player_color = GREEN if mode == "race" else [random.randint(0, 255) for _ in range(3)]
        player = Snake(player_color, PLAYER_START_X, PLAYER_START_Y)

        ai_snake = Snake(BLUE, AI_START_X, AI_START_Y) if mode == "race" else None
        apple = Apple()
        ai = AIController(ai_snake, apple, player) if mode == "race" else None

        score_player = 0
        score_ai = 0
        start_time = time.time()

        clock = pygame.time.Clock()
        running = True

        while running:
            # --- Обработка ввода ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                elif event.type == pygame.KEYDOWN:
                    key_map = {
                        pygame.K_UP: "UP",
                        pygame.K_DOWN: "DOWN",
                        pygame.K_LEFT: "LEFT",
                        pygame.K_RIGHT: "RIGHT",
                    }
                    if event.key in key_map:
                        player.turn(key_map[event.key])

            # --- Движение ---
            player.move()
            if mode == "race":
                ai.update_direction()
                ai_snake.move()

            self._wrap_around(player)

            # --- Съедание яблока ---
            if player.body[-1] == apple.position:
                apple.generate_new(player, ai_snake)
                score_player += 1
            else:
                player.body.pop(0)

            if mode == "race":
                if ai_snake.body[-1] == apple.position:
                    apple.generate_new(player, ai_snake)
                    score_ai += 1
                else:
                    ai_snake.body.pop(0)

            # --- Проверка столкновений ---
            if player.body[-1] in player.body[:-1]:
                running = False
            if mode == "race":
                if player.body[-1] in ai_snake.body or ai_snake.body[-1] in player.body:
                    running = False
                if ai_snake.body[-1] in ai_snake.body[:-1]:
                    running = False

            # --- Отрисовка ---
            self.screen.fill(self._theme()["background"])
            self._draw_grid()

            player.draw(self.screen)
            if mode == "race":
                ai_snake.draw(self.screen)

            # Яблоко
            pygame.draw.rect(
                self.screen, RED,
                pygame.Rect(apple.position[0], apple.position[1], CELL_SIZE, CELL_SIZE),
            )

            # Счёт
            text_color = self._theme()["text"]
            score_text = self.font.render(f"Змейка игрока: {score_player}", True, text_color)
            self.screen.blit(score_text, (10, 10))

            if mode == "race":
                ai_text = self.font.render(f"Змейка ИИ: {score_ai}", True, text_color)
                self.screen.blit(ai_text, (10, 50))

            # Время
            time_in_game = int(time.time() - start_time)
            time_text = self.font.render(f"Время: {time_in_game} сек", True, text_color)
            self.screen.blit(
                time_text,
                (SCREEN_WIDTH - time_text.get_width() - 10, 10),
            )

            pygame.display.flip()
            clock.tick(FPS)

        # Экран завершения игры
        self.show_game_over_screen(score_player, score_ai, mode, time_in_game)

    def _wrap_around(self, snake):
        """
        Телепортирует голову змейки через край экрана.

        Args:
            snake: объект Snake, у которого обновляется голова.
        """
        x, y = snake.body[-1]
        if x < 0:
            snake.body[-1] = (SCREEN_WIDTH - CELL_SIZE, y)
        elif x >= SCREEN_WIDTH:
            snake.body[-1] = (0, y)
        elif y < 0:
            snake.body[-1] = (x, SCREEN_HEIGHT - CELL_SIZE)
        elif y >= SCREEN_HEIGHT:
            snake.body[-1] = (x, 0)

    # ============================================================
    # ЭКРАН ПРОИГРЫША
    # ============================================================

    def show_game_over_screen(self, score_player, score_ai, mode, time_in_game):
        """
        Показывает экран проигрыша с рекордами.

        Обновляет и сохраняет рекорды, если они побиты. Ждёт нажатия
        кнопки «В меню».

        Args:
            score_player: очки игрока.
            score_ai: очки ИИ (0 в классическом режиме).
            mode: "classic" или "race".
            time_in_game: время игры в секундах.
        """
        # Загрузка рекордов и проверка новых
        records = load_records()
        mode_records = records[mode]
        best_score = mode_records["best_score"]
        best_time = mode_records["best_time"]

        new_score_record = score_player > best_score
        new_time_record = time_in_game > best_time

        if new_score_record:
            mode_records["best_score"] = score_player
        if new_time_record:
            mode_records["best_time"] = time_in_game
        save_records(records)

        theme = self._theme()
        button_color = theme["button"]
        hover_color = theme["button_hover"]

        while True:
            self.screen.fill(theme["background"])

            text_color = theme["text"]
            y = SCREEN_HEIGHT // 2 - 150

            def blit_centered(text, color=text_color):
                """Рисует текст по центру и сдвигает y вниз."""
                nonlocal y
                surface = self.font.render(text, True, color)
                x = SCREEN_WIDTH // 2 - surface.get_width() // 2
                self.screen.blit(surface, (x, y))
                y += 50

            blit_centered(f"Змейка игрока: {score_player}")
            if mode == "race":
                blit_centered(f"Змейка ИИ: {score_ai}")
            blit_centered(f"Время: {time_in_game} сек")
            blit_centered(f"Лучший результат: {best_score}")
            blit_centered(f"Лучшее время: {best_time} сек")
            if new_score_record:
                blit_centered("Новый рекорд по очкам!", RED)
            if new_time_record:
                blit_centered("Новый рекорд по времени!", RED)

            # Кнопка «В меню»
            menu_button = Button(
                x=SCREEN_WIDTH // 2 - BUTTON_WIDTH_SMALL // 2,
                y=y,
                width=BUTTON_WIDTH_SMALL, height=BUTTON_HEIGHT_SMALL,
                text="В меню", font_size=24,
                color=button_color, hover_color=hover_color,
            )
            menu_button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if menu_button.is_clicked(event):
                    return