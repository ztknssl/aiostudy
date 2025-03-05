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


@error_catcher
def get_bybit_data() -> list:
    host = 'https://api-testnet.bybit.com'
    prefix = '/v5/market'
    url = '/tickers'
    params = {
        'category': 'spot',
    }

    response = requests.get(f'{host}{prefix}{url}', params=params)

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


@error_catcher
def main():
    data_bybit = get_bybit_data()
    data_okx = get_okx_data()
    print(len(data_bybit))
    print(len(data_okx))


if __name__ == '__main__':
    main()
