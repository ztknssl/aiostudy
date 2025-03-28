from json import JSONDecodeError
from typing import TypeVar, Callable
from collections.abc import Awaitable
from functools import wraps
import aiohttp
from logger import logger

T = TypeVar('T')

""" Декоратор для отлова исключений в асинхронных функциях """
def async_error_catcher(function: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    msg = f'An error occurred in: {function.__name__}'

    @wraps(function)
    async def async_func(*args, **kwargs):
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

    return async_func

""" Декоратор для отлова исключений в синхронных функциях """
#   Дополнительный синхронный логгер решил не создавать

def error_catcher(function: Callable) -> T:
    msg = f'An error occurred in: {function.__name__}'

    @wraps(function)
    def sync_func(*args, **kwargs) -> T | None:
        try:
            return function(*args, **kwargs)
        except PermissionError as err:
            print(msg)
            print(f'Permission denied: {err}')
        except JSONDecodeError as err:
            print(msg)
            print(f'JSON encoding error: {err}')
        except Exception as err:
            print(msg)
            print(f'Other error: {err}')

    return sync_func
