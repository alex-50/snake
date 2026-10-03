"""
Точка входа в игру Snake.

Запускает главное меню. Игра инициализируется внутри класса Game.
"""

from game import Game

if __name__ == "__main__":
    game = Game()
    game.main_menu()
