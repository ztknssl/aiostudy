from loguru import logger


# Настройка логгера с асинхронной очередью для вывода в консоль и запись в лог-файл
logger.add("file.log", enqueue=True)