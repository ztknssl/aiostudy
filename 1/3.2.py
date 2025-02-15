lst = []
i = 0

while len(lst) != 5:
    i += 1
    try:
        elem = int(input(f'Введите {i} элемент: '))
    except ValueError:
        print('Нужно ввести число!')
        i -= 1
        continue
    lst.append(elem)

tup = tuple(lst)

print()
print(f'Ваш кортеж: {tup}')
print(f'Длина вашего кортежа: {len(tup)}')
print(f'Сумма элементов кортежа: {sum(tup)}')

while True:
    try:
        a = int(input('Введите число, которое хотите найти в кортеже: '))
        if a in tup:
            print(f'Ваше число найдено в кортеже с индексом {tup.index(a)}!')
            break
        else:
            print(f'Данного числа в кортеже нет!')
            break
    except ValueError:
        print('Нужно ввести число!')
