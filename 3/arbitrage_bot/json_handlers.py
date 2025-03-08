import json
from err_handler import error_catcher

# Функция записи информации в файл
@error_catcher
def json_writer(data: any, filename: str) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


# Функция чтения информации из файла
@error_catcher
def json_reader(filename: str) -> any:
    with open('final_tickers_list.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data