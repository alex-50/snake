import os
import json
import random
import hashlib
from gameObjects import *


class Button:
    """
    Вспомогательный класс для отрисовки и обработки кнопок
    """

    def __init__(self, x, y, width, height, text, font_size, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font("fonts/PressStart2P.ttf", font_size)

    def draw(self, screen):
        """
        Отрисовка кнопки
        """

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)  # Hover-режим
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, (60, 60, 60))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """
        Проверка на нажатие
        """

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)

        return False


class Game:
    """
    Основной класс игры
    """

    def __init__(self):
        pygame.init()

        # Константы цветов

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake")

        self.sound_enabled = True  # Звук
        self.dark_theme = True  # Тема

        # Загрузка шрифта
        try:
            self.font = pygame.font.Font("fonts/PressStart2P.ttf", 24)
        except FileNotFoundError:
            pygame.quit()

        pygame.mixer.init()

        # Загрузка путей до мелодий
        self.music_files = [os.path.join("sounds", sound) for sound in os.listdir("sounds")]

        if not self.music_files:
            pygame.quit()

    def load_records(self):
        """
        Для сохранения рекордов я решил воспользоваться контрольной суммой, которая считается для прошлого рекорда.
        Если хеш не совпадает (т.е. рекорд поменяли вручную), то мы обнуляем все рекорды.
        Мне кажется это надёжнее, чем хранить рекорды в открытую в .db, хотя для пущей надёжности можно было бы
        совместить эти методы, но я думаю это уже слишком избыточно
        """

        try:
            with open("records.json", mode="r", encoding="utf-8") as records_file:
                content = records_file.read().split("\n")
                json_data = "\n".join(content[:-1])
                hash_value = content[-1]

                # Проверяем хеш
                if hashlib.sha256(json_data.encode()).hexdigest() == hash_value:
                    return json.loads(json_data)
                else:
                    return {
                        "classic": {"best_score": 0, "best_time": 0},
                        "race": {"best_score": 0, "best_time": 0}
                    }
        except FileNotFoundError:
            return {
                "classic": {"best_score": 0, "best_time": 0},
                "race": {"best_score": 0, "best_time": 0}
            }

    def save_records(self, records):
        """
        Сохраняет рекорды и считает к ним хеш.
        """

        json_data = json.dumps(records, indent=2)
        hash_value = hashlib.sha256(json_data.encode()).hexdigest()

        with open("records.json", mode="w", encoding="utf-8") as records_file:
            records_file.write(json_data + "\n" + hash_value)

    def play_random_music(self):
        """
        Выбираем случайную мелодию и воспроизводит её.
        """

        if self.sound_enabled and self.music_files:
            current_music = random.choice(self.music_files)
            pygame.mixer.music.load(current_music)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        """
        Останавливает музыку.
        """

        pygame.mixer.music.stop()

    def draw_menu(self):
        """
        Отрисовка меню
        """

        self.screen.fill(BACKGROUND_DARK if self.dark_theme else BACKGROUND_LIGHT)
        button_color = BUTTON_DARK if self.dark_theme else BUTTON_LIGHT
        button_color_hover = BUTTON_HOVER_DARK if self.dark_theme else BUTTON_HOVER_LIGHT
        lines_color = MAP_LINES_DARK if self.dark_theme else MAP_LINES_LIGHT

        # Рисуем игровое поле на фоне меню
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.line(self.screen, lines_color, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.line(self.screen, lines_color, (0, y), (SCREEN_WIDTH, y), 1)

        # Большие кнопки
        classic_button = Button(
            x=SCREEN_WIDTH // 2 - 225, y=150,
            width=450, height=100,
            text="Классический режим", font_size=24,
            color=button_color, hover_color=button_color_hover
        )

        race_button = Button(
            x=SCREEN_WIDTH // 2 - 150, y=300,
            width=300, height=100,
            text="Гонка с ИИ", font_size=24,
            color=button_color, hover_color=button_color_hover
        )

        # Маленькие кнопки (в левом нижнем углу)
        sound_button = Button(
            x=0, y=SCREEN_HEIGHT - 100,
            width=200, height=50,
            text="Звук: Вкл" if self.sound_enabled else "Звук: Выкл", font_size=14,
            color=button_color, hover_color=button_color_hover
        )

        theme_button = Button(
            x=0, y=SCREEN_HEIGHT - 50,
            width=200, height=50,
            text="Тема: Тёмная" if self.dark_theme else "Тема: Светлая", font_size=14,
            color=button_color, hover_color=button_color_hover
        )

        buttons = [classic_button, race_button, sound_button, theme_button]

        for button in buttons:
            button.draw(self.screen)

        return buttons

    def main_menu(self):

        # Cлучайная мелодия из папки sounds
        self.play_random_music()

        while True:
            buttons = self.draw_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                for button in buttons:
                    if button.is_clicked(event):
                        if button.text == "Классический режим":
                            self.play_random_music()
                            self.game_loop("classic")
                        elif button.text == "Гонка с ИИ":
                            self.play_random_music()
                            self.game_loop("race")
                        elif button.text.startswith("Звук:"):
                            self.sound_enabled = not self.sound_enabled
                            if self.sound_enabled:
                                pygame.mixer.music.unpause()
                            else:
                                pygame.mixer.music.pause()
                        elif button.text.startswith("Тема:"):
                            self.dark_theme = not self.dark_theme

    def game_loop(self, mode):

        snake1 = Snake(GREEN if mode == "race" else ([random.randint(0, 255) for _ in range(3)]), 200, 200)
        snake2 = Snake(BLUE, 400, 200) if mode == "race" else None
        apple = Apple()
        ai_controller = AIController(snake2, apple, snake1) if mode == "race" else None
        score1 = 0
        score2 = 0

        # Время начала игры
        start_time = time.time()

        lines_color = MAP_LINES_DARK if self.dark_theme else MAP_LINES_LIGHT
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake1.direction != "DOWN":
                        snake1.turn("UP")
                    elif event.key == pygame.K_DOWN and snake1.direction != "UP":
                        snake1.turn("DOWN")
                    elif event.key == pygame.K_LEFT and snake1.direction != "RIGHT":
                        snake1.turn("LEFT")
                    elif event.key == pygame.K_RIGHT and snake1.direction != "LEFT":
                        snake1.turn("RIGHT")

            snake1.move()
            if mode == "race":
                ai_controller.update_direction()
                snake2.move()

            # Проверка столкновения со стенами для змейки игрока
            if snake1.body[-1][0] < 0:
                snake1.body[-1] = (SCREEN_WIDTH - 20, snake1.body[-1][1])
            elif snake1.body[-1][0] >= SCREEN_WIDTH:
                snake1.body[-1] = (0, snake1.body[-1][1])
            elif snake1.body[-1][1] < 0:
                snake1.body[-1] = (snake1.body[-1][0], SCREEN_HEIGHT - 20)
            elif snake1.body[-1][1] >= SCREEN_HEIGHT:
                snake1.body[-1] = (snake1.body[-1][0], 0)

            # Змейка игрока съедает яблоко
            if snake1.body[-1] == apple.position:
                apple.generate_new(snake1, snake2)
                score1 += 1
            else:
                snake1.body.pop(0)

            # То же самое для ИИ-змейки, если ИИ-режим
            if mode == "race" and snake2.body[-1] == apple.position:
                apple.generate_new(snake1, snake2)
                score2 += 1
            elif mode == "race":
                snake2.body.pop(0)

            # Проверка столкновения с хвостом
            if snake1.body[-1] in snake1.body[:-1] or (mode == "race" and snake1.body[-1] in snake2.body):
                running = False

            # Проверка столкновения с хвостом для ИИ-змейки
            if mode == "race" and (snake2.body[-1] in snake2.body[:-1] or snake2.body[-1] in snake1.body):
                running = False

            # Далее отрисовка игры

            # Бэкграунд
            self.screen.fill(INDIGO if self.dark_theme else LINEN)

            # Сетка
            for x in range(0, SCREEN_WIDTH, 20):
                pygame.draw.line(self.screen, lines_color, (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, 20):
                pygame.draw.line(self.screen, lines_color, (0, y), (SCREEN_WIDTH, y), 1)

            # Отрисовка змеек и яблока
            snake1.draw(self.screen)
            if mode == "race":
                snake2.draw(self.screen)
            pygame.draw.rect(self.screen, RED, pygame.Rect(apple.position[0], apple.position[1], 20, 20))

            # Отображение счёта
            text_color = WHITE if self.dark_theme else DARK_GREEN
            text1 = self.font.render(f"Змейка игрока: {score1}", True, text_color)
            self.screen.blit(text1, (10, 10))
            if mode == "race":
                text2 = self.font.render(f"Змейка ИИ: {score2}", True, text_color)
                self.screen.blit(text2, (10, 50))

            # Отображаем время - сколько игрок уже продержался
            time_in_game = int(time.time() - start_time)
            time_text = self.font.render(f"Время: {time_in_game} сек", True, text_color)
            self.screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 10, 10))

            pygame.display.flip()
            clock.tick(12)  # Оптимальное обновление кадров для змейки по моим наблюдениям

        # Экран завершения игры
        self.show_game_over_screen(score1, score2, mode, time_in_game)

    def show_game_over_screen(self, score1, score2, mode, time_in_game):
        """
        Отображает экран завершения игры с рекордами
        """
        # Текущие рекорды
        records = self.load_records()
        mode_records = records[mode]
        best_score = mode_records["best_score"]
        best_time = mode_records["best_time"]

        # Проверяем новый рекорд
        new_score_record = score1 > best_score
        new_time_record = time_in_game > best_time

        # Обновляем, если нужно
        if new_score_record:
            mode_records["best_score"] = score1
        if new_time_record:
            mode_records["best_time"] = time_in_game

        # Сохраняем обновленные рекорды
        self.save_records(records)

        button_color = BUTTON_DARK if self.dark_theme else BUTTON_LIGHT
        button_color_hover = BUTTON_HOVER_DARK if self.dark_theme else BUTTON_HOVER_LIGHT

        while True:
            self.screen.fill(BACKGROUND_DARK if self.dark_theme else BACKGROUND_LIGHT)

            # Счёт
            text_color = PINK if not self.dark_theme else WHITE
            snake_player_text = self.font.render(f"Змейка игрока: {score1}", True, text_color)
            snake_ai_text = self.font.render(
                f"Змейка ИИ: {score2}", True, text_color
            ) if mode == "race" else None

            # Время
            time_text = self.font.render(f"Время: {time_in_game} сек", True, text_color)

            # Рекорды
            best_score_text = self.font.render(f"Лучший результат: {best_score}", True, text_color)
            best_time_text = self.font.render(f"Лучшее время: {best_time} сек", True, text_color)

            y_offset = -150  # Для распределения текста в окне

            self.screen.blit(
                snake_player_text,
                (SCREEN_WIDTH // 2 - snake_player_text.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset)
            )

            y_offset += 50

            if snake_ai_text:
                self.screen.blit(
                    snake_ai_text,
                    (SCREEN_WIDTH // 2 - snake_ai_text.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset)
                )

                y_offset += 50

            self.screen.blit(
                time_text,
                (SCREEN_WIDTH // 2 - time_text.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset)
            )

            y_offset += 50

            self.screen.blit(
                best_score_text,
                (SCREEN_WIDTH // 2 - best_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset)
            )

            y_offset += 50

            self.screen.blit(
                best_time_text,
                (SCREEN_WIDTH // 2 - best_time_text.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset)
            )

            y_offset += 50

            # Отображаем сообщения о новых рекордах
            if new_score_record:
                new_score_text = self.font.render("Новый рекорд по очкам!", True, RED)
                self.screen.blit(
                    new_score_text,
                    (SCREEN_WIDTH // 2 - new_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset)
                )
                y_offset += 50
            if new_time_record:
                new_time_text = self.font.render("Новый рекорд по времени!", True, RED)
                self.screen.blit(
                    new_time_text,
                    (SCREEN_WIDTH // 2 - new_time_text.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset)
                )
                y_offset += 50

            # Кнопка "В меню"
            menu_button = Button(
                x=SCREEN_WIDTH // 2 - 100, y=SCREEN_HEIGHT // 2 + y_offset,
                width=200, height=50,
                text="В меню", font_size=24,
                color=button_color, hover_color=button_color_hover
            )
            menu_button.draw(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if menu_button.is_clicked(event):
                    return
