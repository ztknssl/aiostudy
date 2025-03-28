import asyncio
import json
import aiohttp
from middleware import *
from config import *
from logger import logger
import sys
from typing import List, Dict

# Опционально для Windows
if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

storage= {}

@async_error_catcher
async def get_order_book(symbol: str) -> dict:
    async with storage['session'].get(URL, params=f"instId={symbol}-USDT") as response:
        data = await response.json()
        final_dict = dict()
        final_dict[f"{symbol}-USDT"] = {}
        final_dict[f"{symbol}-USDT"]["asks"] = data["data"][0]["askPx"]
        final_dict[f"{symbol}-USDT"]["bids"] = data["data"][0]["bidPx"]

        return final_dict

@async_error_catcher
async def fetch_all_order_books():
    tasks = []
    for ticker in TICKERS:
        await logger.info(f'Получаем словарь с тикерами и ценами для {ticker}')
        tasks.append(asyncio.create_task(get_order_book(ticker)))
    await asyncio.gather(*tasks)


@error_catcher
def write_to_json(data: List[Dict[str, Dict[str, str]]], filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@async_error_catcher
async def main():
    storage['session'] = aiohttp.ClientSession()

    async with storage['session'] as session:
        result = await fetch_all_order_books()

    write_to_json(result, FILENAME)


# Ожидался тип «Coroutine[Any, Any, _T]», вместо этого получен «Awaitable[None]»
# Пока не понял как решить
if __name__ == "__main__":
    asyncio.run(main())
