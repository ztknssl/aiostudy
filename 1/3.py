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

print()
print(f'Ваш список: {lst}')
print(f'Количество элементов в списке: {len(lst)}')
print(f'Сумма всех элементов в списке: {sum(lst)}')
print(f'Среднее арифметическое элементов списка: {sum(lst) / len(lst)}')
