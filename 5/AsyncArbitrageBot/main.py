from models import *
import asyncio
import sys



# Опционально для Windows
if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    async with OKX() as okx:
        okx_tickers = await okx.get_tickers()
        print(len(okx_tickers))

    async with Binance() as binance:
        binance_tickers = await binance.get_tickers()
        print(len(binance_tickers))

    async with Bybit() as bybit:
        bybit_tickers = await bybit.get_tickers()
        print(len(bybit_tickers))

    final = len(set(okx_tickers).intersection(set(binance_tickers)).intersection(set(bybit_tickers)))
    print(final)


asyncio.run(main())
