def calculate_average(list_: list) -> float | None:
    try:
        if len(list_) != 0:
            return sum(list_) / len(list_)
        else:
            print('Список пуст, невозможно вычислить среднее значение.')
    except TypeError as e:
        print(f'Нужно передать список чисел: {str(e)}')
