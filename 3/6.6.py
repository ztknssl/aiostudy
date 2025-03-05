import json
import requests


# Декоратор для отлова исключений
def error_catcher(function):
    def new_func(*args, **kwargs):
        msg = f'An error occurred in: {function.__name__}'
        try:
            return function(*args, **kwargs)
        except requests.RequestException as err:
            print(msg)
            print(f'Request error: {err}')
        except Exception as err:
            print(msg)
            print(f'Other error: {err}')
    return new_func

# Получаем список тикеров с биржи bybit
@error_catcher
def get_bybit_data() -> list:
    host = 'https://api.bybit.com'
    version = '/v5/market'
    product = '/tickers'
    params = {
        'category': 'spot',
    }

    response = requests.get(f'{host}{version}{product}', params=params)

    # Рейзим HTTPError, если она есть
    response.raise_for_status()

    # Получаем json и объявляем список тикеров
    result = response.json()
    bybit_tickers_list = []

    if isinstance(result, dict) and 'result' in result:
        if isinstance(result['result'], dict) and 'list' in result['result']:
            for data in result['result']['list']:
                ticker = ''
                pair = data['symbol']
                if pair.endswith('USDT'):
                    ticker = pair.replace('USDT', '')
                elif pair.endswith('USDC'):
                    ticker = pair.replace('USDC', '')
                else:
                    continue
                bybit_tickers_list.append(ticker)
        else:
            print('No key "list" found')
    else:
        print('No key "result" found')

    # Возвращаем список без повторных тикеров
    return list(set(bybit_tickers_list))


# Получаем список тикеров с биржи okx
@error_catcher
def get_okx_data() -> list:
    host = 'https://www.okx.com'
    prefix = '/api/v5/public/instruments'
    params = {
        'instType': 'SPOT'
    }

    response = requests.get(f'{host}{prefix}', params=params)

    # Рейзим HTTPError, если она есть
    response.raise_for_status()

    # Получаем json и объявляем список тикеров
    result = response.json()
    okx_tickers_list = []

    if isinstance(result, dict) and 'data' in result:
        for pair_info in result['data']:
            okx_tickers_list.append(pair_info['baseCcy'])
    else:
        print('No key "data" in result found')
    # Возвращаем список без повторных тикеров
    return list(set(okx_tickers_list))


# Получаем список совпадений по тикерам
@error_catcher
def ticker_intersection(list1: list, list2: list) -> list:
    return sorted(list(set(list1).intersection(set(list2))))


@error_catcher
def json_writer(list_: list, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(list_, file)


@error_catcher
def json_reader(filename: str) -> list:
    with open('final_tickers_list.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


@error_catcher
def main():
    # Получаем списки монет
    data_bybit = sorted(get_bybit_data())
    data_okx = sorted(get_okx_data())

    # Итоговый список монет
    final_tickers_list = []
    if data_bybit and data_okx:
        final_tickers_list = ticker_intersection(data_bybit, data_okx)

    filename = 'final_tickers_list.json'
    json_writer(list_=final_tickers_list, filename=filename)
    data = json_reader(filename=filename)
    print(data)






if __name__ == '__main__':
    main()
