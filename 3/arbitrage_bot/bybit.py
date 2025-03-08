import requests
from err_handler import error_catcher


# Функция получения списка тикеров с биржи bybit
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

    # Возвращаем список без повторных тикеров
    return sorted(list(set(bybit_tickers_list)))


# Функция получения словаря с ценами с биржи bybit
def get_bybit_prices(tickers_list: list) -> dict:
    host = 'https://api.bybit.com'
    version = '/v5/market'
    product = '/orderbook'
    bybit_prices_dict = {}

    for ticker in tickers_list:
        # Запрашиваем только пары к USDT
        response = requests.get(f'{host}{version}{product}?category=spot&symbol={ticker}USDT')

        # Рейзим HTTPError, если она есть
        response.raise_for_status()
        result = response.json()

        # Получаем лучшие цены покупки и продажи
        if isinstance(result, dict) and 'result' in result:
            best_ask = result['result']['a'][0][0]
            best_bid = result['result']['b'][0][0]

            # Добавляем в итоговый словарь с ключом в виде тикера
            bybit_prices_dict[f'{ticker}'] = [best_bid, best_ask]

    return bybit_prices_dict