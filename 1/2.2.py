 # Запрос ввода до введения корректных данных
while True:
    try:
        a = int(input('Введите первое число: '))
        b = int(input('Введите второе число: '))
        break
    except ValueError:
        print('Вы ввели не число')

# Определяем список операций
operation_list = ['+', '-', '*', '/']

# Проверка операции на нахождение в списке разрешенных
while True:
    operation = input('Введите арифметическую операцию: ')
    if operation not in operation_list:
        print('Вы ввели неверный знак операции')
    else:
        break

# Можно через if, но match/case короче и читабельнее
try:
    match operation:
        case '+':
            print(f'Результат арифметического действия: {a} + {b} = {a + b}')
        case '-':
            print(f'Результат арифметического действия: {a} - {b} = {a - b}')
        case '*':
            print(f'Результат арифметического действия: {a} * {b} = {a * b}')
        case '/':
            print(f'Результат арифметического действия: {a} / {b} = {a / b}')
except ZeroDivisionError:
    print('Деление на ноль')


