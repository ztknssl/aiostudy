# Не понял задание. Откуда TypeError можно взять здесь?

msg = "Ошибка: введенное значение не является числом. Попробуйте еще раз."

try:
    number = float(input("Введите число: "))
    print(number)
except ValueError as e:
    print(e.__class__, msg)
except TypeError as e:
    print(e.__class__, msg)

