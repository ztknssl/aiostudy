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
    bybit_tickers_list_full = []

    if isinstance(result, dict) and 'result' in result:
        if isinstance(result['result'], dict) and 'list' in result['result']:
            for data in result['result']['list']:
                ticker = ''
                pair = data['symbol']
                if pair.endswith('USDT'):
                    bybit_tickers_list_full.append(pair)
                    ticker = pair.replace('USDT', '')
                elif pair.endswith('USDC'):
                    bybit_tickers_list_full.append(pair)
                    ticker = pair.replace('USDC', '')
                else:
                    continue
                bybit_tickers_list.append(ticker)
        else:
            print('No key "list" found')
    else:
        print('No key "result" found')

    # Возвращаем список без повторных тикеров  и список с полным названием пары
    return sorted(list(set(bybit_tickers_list))), sorted(list(set(bybit_tickers_list_full)))


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
    return sorted(list(set(okx_tickers_list)))


# Получаем список совпадений по тикерам
@error_catcher
def ticker_intersection(list1: list, list2: list) -> list:
    return sorted(list(set(list1).intersection(set(list2))))


@error_catcher
def json_writer(data: any, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


@error_catcher
def json_reader(filename: str) -> any:
    with open('final_tickers_list.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


@error_catcher
def get_okx_prices(tickers_list: list) -> dict:
    host = 'https://www.okx.com'
    prefix = '/api/v5/market/ticker'
    okx_prices_dict = {}
    if tickers_list:
        for ticker in tickers_list:
            response = requests.get(f'{host}{prefix}?instId={ticker}-USDT')

            # Рейзим HTTPError, если она есть
            response.raise_for_status()
            result = response.json()

            # Получаем лучшие цены покупки и продажи
            if isinstance(result, dict) and 'data' in result:
                best_ask = result['data'][0]['askPx']
                best_bid = result['data'][0]['bidPx']

                # Добавляем в итоговый словарь с ключом в виде тикера
                okx_prices_dict[f'{ticker}'] = [best_bid, best_ask]
    return okx_prices_dict


def get_bybit_prices(pairs_list: list) -> dict:
    host = 'https://api.bybit.com'
    version = '/v5/market'
    product = '/orderbook'
    bybit_prices_dict = {}

    for pair in pairs_list:
        response = requests.get(f'{host}{version}{product}?category=spot&symbol={pair}')

        # Рейзим HTTPError, если она есть
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and 'result' in result:
            best_ask = result['result']['a'][0][0]
            best_bid = result['result']['b'][0][0]

            bybit_prices_dict[f'{pair}'] = [best_bid, best_ask]

    return bybit_prices_dict


"""
{'retCode': 0,
 'retMsg': 'OK', 
 'result': 
    {'s': 'BTCUSDT', 
    'a': [['90182.27', '0.321716']], 
    'b': [['90182.26', '0.006652']], 
    'ts': 1741267981810, 
    'u': 3145017, 
    'seq': 65073795396, 
    'cts': 1741267981803}, 
    'retExtInfo': {}, 
    'time': 1741267981872}
"""


@error_catcher
def main():
    # Получаем списки монет
    data_bybit, data_bybit_full = get_bybit_data()
    data_okx = get_okx_data()

    # Итоговый список монет
    final_tickers_list = []

    if data_bybit and data_okx:
        final_tickers_list = ticker_intersection(data_bybit, data_okx)

    filename = 'final_tickers_list.json'
    json_writer(data=final_tickers_list, filename=filename)
    data = json_reader(filename=filename)

    # Получаем словарь цен с биржи okx
    okx_prices_dict = {}
    if data:
        okx_prices_dict = get_okx_prices(data)

        # Записываем данные с okx в json
    okx_json_filename = 'okx_prices.json'
    json_writer(data=okx_prices_dict, filename=okx_json_filename)


if __name__ == '__main__':
    main()