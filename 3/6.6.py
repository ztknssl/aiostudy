from json import JSONDecodeError
import okx.PublicData as PublicData
import json
from okx.app.exception import AbstractEXP


# Декоратор для отлова исключений
def error_catcher(function):
    def new_func(*args, **kwargs):
        msg = f'An error occurred in: {function.__name__}'
        try:
            return function(*args, **kwargs)
        except AbstractEXP as err:
            print(msg)
            print(f'OKX API error: {err}')
        except JSONDecodeError as err:
            print(msg)
            print(f'JSON decoding error: {err}')
        except Exception as err:
            print(msg)
            print(f'Other error: {err}')
    return new_func


@error_catcher
def get_okx_data() -> list:
    flag = "0"  # Production trading: 0, Demo trading: 1
    okx_coins_list = []

    public_data_api = PublicData.PublicAPI(flag=flag)

    # Получаем все данные со спота okx
    result = public_data_api.get_instruments(
        instType="SPOT"
    )

    # Получаем список тикеров из всех пар
    if isinstance(result, dict) and 'data' in result:
        for data in result['data']:
            okx_coins_list.append(data['baseCcy'])
        # Убираем дубликаты
        okx_coins_list = list(set(okx_coins_list))
    else:
        print('No such key in result')

    return okx_coins_list


def get_bybit_data():
    pass


@error_catcher
def json_writer(list_: list, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(list_, file)


def main():
    filename_okx = 'okx_coins_reduced.json'
    okx_data = get_okx_data()
    if okx_data:
        json_writer(okx_data, filename=filename_okx)

if __name__ == '__main__':
    main()

