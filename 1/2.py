try:
    a = int(input('Введите первое число: '))
    b = int(input('Введите второе число: '))
except ValueError:
    print('Вы ввели не число')
    exit()

operation_list = ['+', '-', '*', '/']
operation = input('Введите арифметическую операцию: ')

if operation not in operation_list:
    print('Вы ввели неверный знак операции')
    exit()
else:
    try:
        if operation == '+':
            print(f'Результат арифметического действия: {a} + {b} = {a + b}')
        if operation == '-':
            print(f'Результат арифметического действия: {a} - {b} = {a - b}')
        if operation == '*':
            print(f'Результат арифметического действия: {a} * {b} = {a * b}')
        if operation == '/':
            print(f'Результат арифметического действия: {a} / {b} = {a / b}')
    except ZeroDivisionError:
        print('Деление на ноль')
