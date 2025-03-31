import abc
import aiohttp
import asyncio
from typing import Optional, TypeVar, List, Dict
from logger import logger
from config import *


T = TypeVar('T')

class Exchange(abc.ABC):

    def __init__(self, name):
        self.__name = name
        self.coins = {}
        self.__session: Optional[aiohttp.ClientSession] = None

    async def get_prices(self, retries: int=3, delay: int=1)-> Dict[str, List[str]]:
        pass


class OKX(Exchange):
    def __init__(self, name):
        super().__init__(name)
        self.__name = name

    async def __aenter__(self):
        self.__session = aiohttp.ClientSession()
        return self

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    async def __aexit__(self, exc_type, exc, tb):
        if self.__session:
            if not self.__session.closed:
                await self.__session.close()
            self.session = None

    async def get_prices(self, retries: int=3, delay: int=1) -> Dict[str, List[str]]:

        for attempt in range(retries):
            try:
                async with self.__session.get(url=OKX_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

                    for i in range(len(data['data'])):
                        if data['data'][i]['instId'].endswith('USDT'):
                            ask = data['data'][i]['askPx']
                            bid = data['data'][i]['bidPx']
                            self.coins[(data['data'][i]['instId'].replace('-', ''))] = [bid, ask]
            except Exception as e:
                if attempt == retries - 1:
                    logger.error(f"Ошибка при получении данных для {self.name.upper()}: {str(e)}", exc_info=True)
                logger.warning(f"Попытка {attempt + 1} не удалась для {self.name.upper()}, повторяем...")
                await asyncio.sleep(delay)
        return self.coins


class Binance(Exchange):
    def __init__(self, name):
        super().__init__(name)
        self.__name = name

    async def __aenter__(self):
        self.__session = aiohttp.ClientSession()
        return self

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    async def __aexit__(self, exc_type, exc, tb):
        if self.__session:
            if not self.__session.closed:
                await self.__session.close()
            self.session = None

    async def get_prices(self, retries: int=3, delay: int=1) -> Dict[str, List[str]]:

        for attempt in range(retries):
            try:
                async with self.__session.get(url=BINANCE_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

                    for i in range(len(data)):
                        ask = data[i]['askPrice']
                        bid = data[i]['bidPrice']
                        if data[i]['symbol'].endswith('USDT'):
                            self.coins[(data[i]['symbol'])] = [bid, ask]
            except Exception as e:
                if attempt == retries - 1:
                    logger.error(f"Ошибка при получении данных для {self.name.upper()}: {str(e)}", exc_info=True)
                logger.warning(f"Попытка {attempt + 1} не удалась для {self.name.upper()}, повторяем...")
                await asyncio.sleep(delay)
        return self.coins


class Bybit(Exchange):
    def __init__(self, name):
        super().__init__(name)
        self.__name = name

    async def __aenter__(self):
        self.__session = aiohttp.ClientSession()
        return self

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    async def __aexit__(self, exc_type, exc, tb):
        if self.__session:
            if not self.__session.closed:
                await self.__session.close()
            self.session = None

    async def get_prices(self, retries: int=3, delay: int=1) -> Dict[str, List[str]]:

        for attempt in range(retries):
            try:
                async with self.__session.get(url=BYBIT_URL) as response:
                    response.raise_for_status()
                    data = await response.json()

                    for i in range(len(data['result']['list'])):
                        ask = data['result']['list'][i]['ask1Price']
                        bid = data['result']['list'][i]['bid1Price']
                        if data['result']['list'][i]['symbol'].endswith('USDT'):
                            self.coins[(data['result']['list'][i]['symbol'])] = [bid, ask]
            except Exception as e:
                if attempt == retries - 1:
                    logger.error(f"Ошибка при получении данных для {self.name.upper()}: {str(e)}", exc_info=True)
                logger.warning(f"Попытка {attempt + 1} не удалась для {self.name.upper()}, повторяем...")
                await asyncio.sleep(delay)
        return self.coins

