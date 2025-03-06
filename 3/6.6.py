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
                # Это решил убрать, так как она okx нет пар к USDC, но если появятся, то можно по такой логике добавлять
                # elif pair.endswith('USDC'):
                #     ticker = pair.replace('USDC', '')

                bybit_tickers_list.append(ticker)
        else:
            print('No key "list" found')
    else:
        print('No key "result" found')

    # Возвращаем список без повторных тикеров  и список с полным названием пары
    return sorted(list(set(bybit_tickers_list)))


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


def get_bybit_prices(tickers_list: list) -> dict:
    host = 'https://api.bybit.com'
    version = '/v5/market'
    product = '/orderbook'
    bybit_prices_dict = {}

    for ticker in tickers_list:
        response = requests.get(f'{host}{version}{product}?category=spot&symbol={ticker}USDT')

        # Рейзим HTTPError, если она есть
        response.raise_for_status()
        result = response.json()

        if isinstance(result, dict) and 'result' in result:
            best_ask = result['result']['a'][0][0]
            best_bid = result['result']['b'][0][0]

            bybit_prices_dict[f'{ticker}'] = [best_bid, best_ask]

    return bybit_prices_dict


@error_catcher
def main():
    # Получаем списки монет
    data_bybit = get_bybit_data()
    data_okx = get_okx_data()

    # Итоговый список монет
    final_tickers_list = []
    if data_bybit and data_okx:
        final_tickers_list = ticker_intersection(data_bybit, data_okx)

    filename = 'final_tickers_list.json'

    # Пишем и снова читаем) Не знаю зачем, но в задании так
    json_writer(data=final_tickers_list, filename=filename)
    data = json_reader(filename=filename)

    # Получаем словари цен с биржи okx и bybit
    okx_prices_dict = {}
    bybit_prices_dict = {}
    okx_json_filename = 'okx_prices.json'
    bybit_json_filename = 'bybit_prices.json'
    if data:
        okx_prices_dict = get_okx_prices(data)

        # Записываем данные с okx в json
        json_writer(data=okx_prices_dict, filename=okx_json_filename)

        # Получаем словарь цен с биржи bybit
        bybit_prices_dict = get_bybit_prices(data)

        # Записываем данные с bybit в json
        json_writer(bybit_prices_dict, filename=bybit_json_filename)


if __name__ == '__main__':
    main()