from models import *
import asyncio
import sys



# Опционально для Windows
if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    async with OKX('okx') as okx:
        okx_prices = await okx.get_prices()
        print(okx_prices)

    async with Binance('binance') as binance:
        binance_prices = await binance.get_prices()
        print(binance_prices)

    async with Bybit('bybit') as bybit:
        bybit_prices = await bybit.get_prices()
        print(bybit_prices)


    final = len(set(okx_prices).intersection(set(binance_prices)).intersection(set(bybit_prices)))
    print(final)


asyncio.run(main())
