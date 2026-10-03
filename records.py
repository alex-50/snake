"""
Работа с рекордами: загрузка и сохранение.

Файл рекордов подписывается SHA-256 контрольной суммой. Если хеш
не совпадает (файл отредактировали вручную) — рекорды обнуляются.
"""

import hashlib
import json

from utils import RECORDS_PATH

# Значения по умолчанию для обеих игровых мод
DEFAULT_RECORDS = {
    "classic": {"best_score": 0, "best_time": 0},
    "race": {"best_score": 0, "best_time": 0},
}


def load_records():
    """
    Загружает рекорды из файла.

    Если файл отсутствует или хеш не совпадает — возвращает
    копию DEFAULT_RECORDS.

    Returns:
        Словарь с рекордами для режимов "classic" и "race".
    """
    try:
        with open(RECORDS_PATH, mode="r", encoding="utf-8") as f:
            content = f.read().split("\n")
            json_data = "\n".join(content[:-1])
            stored_hash = content[-1]

            if hashlib.sha256(json_data.encode()).hexdigest() == stored_hash:
                return json.loads(json_data)
    except FileNotFoundError:
        pass

    # Возвращаем копию, чтобы вызывающий код мог безопасно мутировать
    return {mode: dict(values) for mode, values in DEFAULT_RECORDS.items()}


def save_records(records):
    """
    Сохраняет рекорды в файл с подписью SHA-256.

    Args:
        records: словарь с рекордами.
    """
    json_data = json.dumps(records, indent=2)
    hash_value = hashlib.sha256(json_data.encode()).hexdigest()

    with open(RECORDS_PATH, mode="w", encoding="utf-8") as f:
        f.write(json_data + "\n" + hash_value)
