 # Запрашиваем ввод до введения корректных данных
while True:
    try:
        a = int(input('Введите первое число: '))
        b = int(input('Введите второе число: '))
        break
    except ValueError:
        print('Вы ввели не число')

# Определяем список операций
operation_list = ['+', '-', '*', '/']

# Проверка операции
while True:
    operation = input('Введите арифметическую операцию: ')
    if operation not in operation_list:
        print('Вы ввели неверный знак операции')
    else:
        break

try:
    if operation == '+':
        print(f'Результат арифметического действия: {a} + {b} = {a + b}')
    elif operation == '-':
        print(f'Результат арифметического действия: {a} - {b} = {a - b}')
    elif operation == '*':
        print(f'Результат арифметического действия: {a} * {b} = {a * b}')
    elif operation == '/':
        print(f'Результат арифметического действия: {a} / {b} = {a / b}')
except ZeroDivisionError:
    print('Деление на ноль')


