from models import *
import asyncio
import sys



# Опционально для Windows
if sys.platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@logger.catch()
async def main():
    async with OKX('okx') as okx:
        okx_prices = await okx.get_prices()
        print(len(okx_prices))

    async with Binance('binance') as binance:
        binance_prices = await binance.get_prices()
        print(len(binance_prices))

    async with Bybit('bybit') as bybit:
        bybit_prices = await bybit.get_prices()
        print(len(bybit_prices))


    await update_coins_dicts(okx, binance, bybit)
    print(len(okx.coins))
    print(len(binance.coins))
    print(len(bybit.coins))


asyncio.run(main())
