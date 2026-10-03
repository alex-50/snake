"""
Утилиты для работы с путями к ресурсам.

Работает и при запуске из скрипта, и после сборки в .exe через PyInstaller.
"""

import os
import sys


def get_base_dir() -> str:
    """
    Возвращает базовую директорию приложения.

    - Из скрипта: папка, где лежит utils.py (корень проекта).
    - Из .exe (PyInstaller): папка, где лежит сам .exe.
    """
    if getattr(sys, "frozen", False):
        # Запущено из .exe — берём папку с исполняемым файлом
        return os.path.dirname(sys.executable)
    # Обычный запуск из скрипта — папка с этим файлом
    return os.path.dirname(os.path.abspath(__file__))


# Базовые пути для ресурсов (рассчитываются один раз при импорте)
BASE_DIR = get_base_dir()
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
RECORDS_PATH = os.path.join(BASE_DIR, "records.json")