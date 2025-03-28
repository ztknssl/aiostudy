from json import JSONDecodeError
from typing import TypeVar, Callable, Optional
from collections.abc import Awaitable
from functools import wraps
import aiohttp
from logger import logger

T = TypeVar('T')

""" Декоратор для отлова исключений в асинхронных функциях """
def async_error_catcher(function: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[Optional[T]]]:
    msg = f'An error occurred in: {function.__name__}'

    @wraps(function)
    async def async_func(*args, **kwargs) -> Optional[T]:
        try:
            return await function(*args, **kwargs)
        except aiohttp.ClientError as err:
            await logger.error(f"{msg}\nRequest error: {err}")
        except aiohttp.ContentTypeError as err:
            await logger.error(f"{msg}\nInvalid JSON response: {err}")
        except Exception as err:
            await logger.error(f"{msg}\nOther error: {err}")
        return None

    return async_func

""" Декоратор для отлова исключений в синхронных функциях """
#   Дополнительный синхронный логгер решил не создавать

def error_catcher(function: Callable) -> T | None:
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
            print(f"{msg}\nError: {err}")
            return None

    return sync_func
