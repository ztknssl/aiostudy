import asyncio
import random


async def print_message(message: str) -> None:
    print(message)


async def main():
    list_ = ['Привет!', 'Как дела?', 'До свидания!']

    # Для произвольного порядка вывода
    random.shuffle(list_)

    # Уставнавливаем return_exceptions=True, чтобы не прерывать выполнение остальных задач, если
    # в какой-то возникнет исключение

    await asyncio.gather(*(print_message(item) for item in list_), return_exceptions=True)


asyncio.run(main())
