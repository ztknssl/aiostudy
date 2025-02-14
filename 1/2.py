a = int(input('Введите первое число: '))
b = int(input('Введите второе число: '))

operation_list = ['+', '-', '*', '/']
operation = input('введите знак операции: ')

if operation not in operation_list:
    print('Вы ввели неверный знак операции')
    exit()
else:
    try:
        if operation == '+':
            print(a + b)
        if operation == '-':
            print(a - b)
        if operation == '*':
            print(a * b)
        if operation == '/':
            print(a / b)
    except ZeroDivisionError:
        print('Деление на ноль')
