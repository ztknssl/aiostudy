filepath = input("Введите путь до файла: ")

try:
    with open(filepath) as file:
        data = file.read()
        print(data)
except FileNotFoundError:
    print("Файл по указанному пути не найден. Пожалуйста, проверьте путь и повторите попытку.")
