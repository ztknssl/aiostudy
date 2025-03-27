import asyncio

import aiohttp
from middleware import async_error_catcher
from config import *
from logger import logger
import sys

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
        tasks.append(asyncio.create_task(get_order_book(ticker)))
    results = await asyncio.gather(*tasks)
    return results

@async_error_catcher
async def main():
    storage['session'] = aiohttp.ClientSession()

    async with storage['session'] as session:
        result = await fetch_all_order_books()

    print(result)


asyncio.run(main())