from typing import TypeVar, Callable
from collections.abc import Awaitable
from functools import wraps
import aiohttp
from logger import logger

T = TypeVar('T')

""" Декоратор для отлова исключений только в асинхронных функциях """
def async_error_catcher(function: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    @wraps(function)
    async def new_func(*args, **kwargs):
        msg = f'An error occurred in: {function.__name__}'
        try:
            return await function(*args, **kwargs)
        except aiohttp.ClientError as err:
            await logger.error(msg)
            await logger.error(f'Request error: {err}')
            return None
        except Exception as err:
            await logger.error(msg)
            await logger.error(f'Other error: {err}')
            return None

    return new_func
