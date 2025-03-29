import aiohttp
import asyncio
from logger import logger
from config import *
from typing import Dict, List, Optional
import json
import time
import sys

# Опционально для Windows
if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Попытался сделать всё через контекстный менеджер как в стриме с Романом и заодно
# реализовать логику для биржи в одной сессии, так как в лекциях говорилось, что
# не рекомендуется создавать несколько сессий для одного приложения
class AsyncOKXParser:
    """ Класс AsyncOKXParser представляет из себя контекстный менеджер для работы в единой сессии """
    def __init__(self):
        #
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            if not self.session.closed:
                await self.session.close()
            # Не уверен, что в python это так работает, но если просто закрыть сессию,
            # то по идее ссылка на неё останется и gc её не соберёт, поэтому явно
            # сделал её None. Думаю, хуже не будет)
            self.session = None

    async def get_order_book(self, symbol: str) -> Dict:
        """Получает ордербук для конкретной монеты"""
        params = {
            "instId": f"{symbol}-USDT",
            "sz": 5 # Глубину можно указать любую
        }

        try:
            async with self.session.get(URL, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                return {
                    "symbol": symbol,
                    "data": data["data"][0] if data["data"] else None
                }
        except Exception as e:
            logger.error(f"Ошибка при получении ордербука для {symbol}: {str(e)}", exc_info=True)
            return {
                "symbol": symbol,
                "error": str(e)
            }

    async def fetch_all_order_books(self, symbols: List[str]) -> List[Dict]:
        """Получаем ордербуки для всех монет"""

        # По идее здесь должна быть реализована другая логика с одновременной записью
        # в файл для каждого полученного ответа, иначе асинхронная save_to_json по сути
        # дожидается полного списка и работает синхронно, но в таком случае будет много циклов
        # записи, что не есть хорошо, по-моему. Если можно, напишите после проверки, какой вариант
        # предпочтительнее

        # Обработку ошибок опустил, так как она реализована в get_order_book
        tasks = [self.get_order_book(symbol) for symbol in symbols]
        return await asyncio.gather(*tasks, return_exceptions=True)



async def save_to_json(data: List[Dict], filename: str) -> None:
    """Сохранение в JSON"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


async def main():
    start = time.time()

    async with AsyncOKXParser() as parser:
        logger.info("Начинаем получение ордербуков...")
        order_books = await parser.fetch_all_order_books(TICKERS)
        await save_to_json(order_books, FILENAME)

    full_time = time.time() - start
    logger.info(f"Готово! Результаты сохранены в {FILENAME}")
    logger.info(f"Время выполнения: {full_time:.2f} секунд")


if __name__ == "__main__":
    asyncio.run(main())

