from bybit import *
from internal import *
from json_handlers import *
from okx import *


@error_catcher
def main():

    print('Получаем списки монет...')
    data_bybit = get_bybit_data()
    data_okx = get_okx_data()

    print('Сравниваем списки и оставляем только совпадения...')
    final_tickers_list = []
    if data_bybit and data_okx:
        final_tickers_list = ticker_intersection(data_bybit, data_okx)

    filename = 'final_tickers_list.json'

    print('Пишем в файл только совпадения...')
    json_writer(data=final_tickers_list, filename=filename)

    print('Читаем файл с совпавшими тикерами...')
    data = json_reader(filename=filename)

    print('Получаем словари цен с бирж okx и bybit...')
    okx_prices_dict = {}
    bybit_prices_dict = {}
    okx_json_filename = 'okx_prices.json'
    bybit_json_filename = 'bybit_prices.json'

    # Проверяем, что из файла final_tickers_list.json данные прочитались без ошибок
    if data:
        okx_prices_dict = get_okx_prices(data)

        # Записываем данные с биржи okx в json
        json_writer(data=okx_prices_dict, filename=okx_json_filename)

        # Получаем словарь цен с биржи bybit
        bybit_prices_dict = get_bybit_prices(data)

        # Записываем данные с bybit в json
        json_writer(bybit_prices_dict, filename=bybit_json_filename)

    print()

    # Сравниваем цены и выводим в терминал сделки
    arbitrage(dict_1=okx_prices_dict, dict_2=bybit_prices_dict)


if __name__ == '__main__':
    main()