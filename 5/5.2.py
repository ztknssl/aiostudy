import asyncio
import random


async def double(value: int) -> int:
    sleep_time = random.randint(1, 3)
    print(f'Спим {sleep_time}с, исходное число: {value}')
    print('--------------')
    await asyncio.sleep(sleep_time)
    return value * 2


async def main():
    numbers = [1, 2, 3, 4, 5]

    result = await asyncio.gather(*(double(item) for item in numbers), return_exceptions=True)
    print(result)

asyncio.run(main())


# Опционально к 1 задаче

# async def print_message(message: str) -> None:
#     await asyncio.sleep(random.randint(1, 3))
#     print(message)
#
#
# async def main():
#     list_ = ['Привет!', 'Как дела?', 'До свидания!']
#
#     # Уставнавливаем return_exceptions=True, чтобы не прерывать выполнение остальных задач, если
#     # в какой-то возникнет исключение
#
#     await asyncio.gather(*(print_message(item) for item in list_), return_exceptions=True)
#
# asyncio.run(main())
