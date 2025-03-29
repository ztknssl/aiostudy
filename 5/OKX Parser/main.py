""" Вариант с использованием декоратора для отлова исключений """
# Такой вариант мне уже разонравился, но оставлю, раз уж сделал)
# Основная версия домашки в AsyncOKXParser.py

import asyncio
import json
from middleware import *
from config import *
import sys
from typing import List, Dict

# Опционально для Windows
if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

""" Создаем хранилище для сессии и прочих сущностей приложения """
storage= {}

""" Функция для получения словаря с ценами для каждого тикера """
@async_error_catcher
async def get_order_book(symbol: str) -> dict:
    async with storage['session'].get(URL, params={"instId": f"{symbol}-USDT"}) as response:
        response.raise_for_status()
        data = await response.json()

        if "data" not in data or not data["data"]:
            return {f"{symbol}-USDT": {"asks": None, "bids": None}}

        return {
            f"{symbol}-USDT": {
                "asks": data["data"][0]["asks"],
                "bids": data["data"][0]["bids"]
            }
        }

""" Функция для получения итогового списка для записи в файл """
@async_error_catcher
async def fetch_all_order_books() -> list:
    tasks = [asyncio.create_task(get_order_book(ticker)) for ticker in TICKERS]
    return await asyncio.gather(*tasks)

""" Функция записи в json-файл. Синхронная, так как данные пишутся в самом конце программы
    один раз и нет никаких добавлений в файл по ходу их получения
 """
@error_catcher
def write_to_json(data: List[Dict[str, Dict[str, List[str]]]], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@async_error_catcher
async def main():
    async with aiohttp.ClientSession() as session:
        storage['session'] = session
        result = await fetch_all_order_books()
    write_to_json(result, FILENAME)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as err:
        print(f"Critical error: {err}")
