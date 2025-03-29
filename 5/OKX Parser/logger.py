from loguru import logger
from config import LOGS


# Настройка логгера с асинхронной очередью для вывода в консоль и запись в лог-файл
logger.add(LOGS, enqueue=True)