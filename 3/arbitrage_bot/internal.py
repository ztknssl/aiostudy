from err_handler import error_catcher

# Функция для получения списка совпадений по тикерам
@error_catcher
def ticker_intersection(list1: list, list2: list) -> list:
    return sorted(list(set(list1).intersection(set(list2))))

"""
Функция display_info получает на вход тикер, биржи, где продаем и покупаем, бид и аск.
total - условная сумма в 100к$
quantity - количество токенов, которое можно купить
profit - общий округленный профит в $
"""
@error_catcher
def display_info(ticker: str, buy_exchange: str, sell_exchange: str, bid: float, ask: float) -> None:
    total = 100000
    quantity = 0
    if bid != 0:
        quantity = total / bid
    profit = round(quantity * (bid - ask))

    print(f'Нашел спред на монете {ticker}')
    print(f'Покупка на бирже {buy_exchange} по цене {ask}')
    print(f'Продажа на бирже {sell_exchange} по цене {bid}')
    print(f'Профит: {profit} $')
    print('----------------------------------------')


"""
Функция arbitrage сравнивает бид с одной биржи и аск с другой.
Так как для получания профита нам придётся бить по биду(продавать по маркету) на бирже,
где дороже, и бить в аск(покупать по маркету), где дешевле, для достижения профитности
бид на одной бирже должен быть выше, чем аск на другой
"""
@error_catcher
def arbitrage(dict_1:dict, dict_2: dict) -> None:
    for ticker in dict_1:
        if float(dict_1[ticker][0]) > float(dict_2[ticker][1]):
            buy_exchange = 'Bybit'
            sell_exchange = 'OKX'
            bid = float(dict_1[ticker][0])
            ask = float(dict_2[ticker][1])
        elif float(dict_2[ticker][0]) > float(dict_1[ticker][1]):
            buy_exchange = 'OKX'
            sell_exchange = 'Bybit'
            bid = float(dict_2[ticker][0])
            ask = float(dict_1[ticker][1])
        else:
            continue
        display_info(ticker=ticker, buy_exchange=buy_exchange, sell_exchange=sell_exchange, bid=bid, ask=ask)