import abc
import aiohttp
import asyncio
from typing import Optional, TypeVar, List, Dict
from logger import logger
from config import *


T = TypeVar('T')

class Exchange(abc.ABC):

    def __init__(self):
        self.coins = []
        self.session: Optional[aiohttp.ClientSession] = None

    async def get_tickers(self, retries: int=3, delay: int=1)-> List[str]:
        pass


class OKX(Exchange):
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            if not self.session.closed:
                await self.session.close()
            self.session = None

    async def get_tickers(self, retries: int=3, delay: int=1) -> List[str]:

        for attempt in range(retries):
            try:
                async with self.session.get(url=OKX_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

                    for i in range(len(data['data'])):
                        if data['data'][i]['instId'].endswith('USDT'):
                            self.coins.append(data['data'][i]['instId'].replace('-', ''))
            except Exception as e:
                if attempt == retries - 1:
                    logger.error(f"Ошибка при получении списка монет для OKX: {str(e)}", exc_info=True)
                logger.warning(f"Попытка {attempt + 1} не удалась для OKX, повторяем...")
                await asyncio.sleep(delay)
        return self.coins


class Binance(Exchange):
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            if not self.session.closed:
                await self.session.close()
            self.session = None

    async def get_tickers(self, retries: int=3, delay: int=1) -> List[str]:

        for attempt in range(retries):
            try:
                async with self.session.get(url=BINANCE_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

                    for i in range(len(data)):
                        if data[i]['symbol'].endswith('USDT'):
                            self.coins.append(data[i]['symbol'])
            except Exception as e:
                if attempt == retries - 1:
                    logger.error(f"Ошибка при получении списка монет для Binance: {str(e)}", exc_info=True)
                logger.warning(f"Попытка {attempt + 1} не удалась для Binance, повторяем...")
                await asyncio.sleep(delay)
        return self.coins


class Bybit(Exchange):
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            if not self.session.closed:
                await self.session.close()
            self.session = None

    async def get_tickers(self, retries: int=3, delay: int=1) -> List[str]:

        for attempt in range(retries):
            try:
                async with self.session.get(url=BYBIT_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

                    for i in range(len(data['result']['list'])):
                        if data['result']['list'][i]['symbol'].endswith('USDT'):
                            self.coins.append(data['result']['list'][i]['symbol'])
            except Exception as e:
                if attempt == retries - 1:
                    logger.error(f"Ошибка при получении списка монет для Binance: {str(e)}", exc_info=True)
                logger.warning(f"Попытка {attempt + 1} не удалась для Binance, повторяем...")
                await asyncio.sleep(delay)
        return self.coins

