# Попытка сделать middlware для обработки исключений и упорядочить код
import requests

host = 'https://api.gateio.ws'
prefix = '/api/v4'
headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
url = '/spot/order_book'
coins_list = ['BTC_USDT', 'ETH_USDT', 'SOL_USDT']


# Декоратор для отлова исключений
def error_catcher(function):
    def new_func(*args):
        msg = f'An error occurred in: {function.__name__}'
        try:
            return function(*args)
        # Решил оставить общий класс на всякий случай
        except requests.RequestException as err:
            print(msg)
            print(f'Request error: {err}')
        except Exception as err:
            print(msg)
            print(f'Other error: {err}')
    return new_func


# Получение списка параметров запроса из списка coins_list
@error_catcher
def get_query_params(list_: list) -> list:
    return [f'currency_pair={currency_pair}' for currency_pair in list_]


# Выполнение запроса и вывод результатов
@error_catcher
def get_data(query_params_list: list) -> None:
    for query_param in query_params_list:
        response = requests.get(f'{host}{prefix}{url}?{query_param}', headers=headers)

        # Рейзим HTTPError, если она есть
        response.raise_for_status()

        # Получаем название монеты из параметра запроса
        currency_name = query_param.split('=')[1].split('_')[0]

        # Получаем цены
        ask = response.json()['asks'][0][0]
        bid = response.json()['bids'][0][0]

        print(f'Текущая цена продажи для {currency_name}: {ask}')
        print(f'Текущая цена покупки для {currency_name}: {bid}')
        print('----------')


def main():
    query_params_list = get_query_params(coins_list)
    # Проверяем, что список не пустой
    if query_params_list:
        get_data(query_params_list)


if __name__ == '__main__':
    main()




# 2 вариант попроще(изначальный)
# import requests
#
# host = 'https://api.gateio.ws'
# prefix = '/api/v4'
# headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
# url = '/spot/order_book'
# coins_list = ['BTC_USDT', 'ETH_USDT', 'SOL_USDT']
#
# # В цикле выбираем торговую пару из списка и формируем url для запроса
# for currency_pair in coins_list:
#     try:
#         query_param = f'currency_pair={currency_pair}'
#         response = requests.get(f'{host}{prefix}{url}?{query_param}', headers=headers)
#
#         # Проверяем статус ответа
#         response.raise_for_status()
#
#         # Вынесем в переменные название монеты, текущие бид и аск
#         currency_name = currency_pair.split('_')[0]
#         ask = response.json()['asks'][0][0]
#         bid = response.json()['bids'][0][0]
#
#         print(f'Текущая цена продажи для {currency_name}: {ask}')
#         print(f'Текущая цена покупки для {currency_name}: {bid}')
#         print('----------')
#     except requests.ConnectionError as err:
#         print(f'Connection error occured: {err}')
#     except requests.HTTPError as err:
#         print(f'HTTP error occured: {err}')
#     except Exception as err:
#         print(f'Other error occured: {err}')


# 3 вариант
# Решил пощупать библиотеку ccxt. С гейтом работает очень медленно - бинанс намного быстрее

# import ccxt
#
# # Выбор биржи
# exchange = ccxt.gateio()
#
# coins_list = ['BTC_USDT', 'ETH_USDT', 'SOL_USDT']
#
# try:
#     for pair in coins_list:
#         pair = pair.replace('_', '/')
#
#         # Получаем данные для конкретной пары
#         order_book = exchange.fetch_order_book(pair)
#
#         bid = order_book['bids'][0][0]
#         ask = order_book['asks'][0][0]
#
#         print(f'Текущая цена продажи для {pair.split("/")[0]}: {ask}')
#         print(f'Текущая цена покупки для {pair.split("/")[0]}: {bid}')
#         print('----------')
# except Exception as err:
#     print(f'An error occured: {err}')
