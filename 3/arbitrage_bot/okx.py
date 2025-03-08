import requests
from err_handler import error_catcher

# Функция получения списка тикеров с биржи okx
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


# Функция получения словаря с ценами с биржи okx
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