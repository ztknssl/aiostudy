# Вхождение само перезапишется последним значением
original_dict = {'apple': 'fruit', 'carrot': 'vegetable', 'banana': 'fruit', 'orange': 'fruit'}
reverse_dict = {value: key for key, value in original_dict.items()}
print(reverse_dict)

# Дополнительное задание:
reverse_dict_1 = {}

# Преобразуем значения обратного словаря в списки
for key, value in original_dict.items():
    reverse_dict_1[value] = key.split()

# Добавляем к списку новое значение, если его там ещё нет
for key, value in original_dict.items():
    if value in reverse_dict_1 and key not in reverse_dict_1[value]:
        reverse_dict_1[value].append(key)

# Распаковываем обратно списки с единственным элементом
# У вас там в примере этого не требуется, но так выглядит лучше)
for key in reverse_dict_1:
    if len(reverse_dict_1[key]) == 1:
        reverse_dict_1[key] = reverse_dict_1[key][0]

print(reverse_dict_1)
