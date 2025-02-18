from collections import Counter

# text = """
# Я прохожу курсы на крутом сайте ‘AIO STUDY’.
# Тут я обучусь программированию на python и коду под web3.
# Это даст мне в дальнейшем сильный буст. Тут много домашки,
# что дает мне хорошую практику. Python - идеальный выбор. Всем успехов!
# """

# Считываем ввод. Если вставить текст из коммента сверху, то работать не будет из-за наличия там переносов строк
text = input('Введите текст: ')

# Приводим к нижнему регистру, вырезаем лишнее, обрезаем строку и преобразуем в список
text = text.casefold()
text = text.strip().replace("’", '').replace("‘", '').replace('!', '')
word_list = text.replace('.', '').replace('-', '').split()

# Метод Counter вернет коллекцию вхождений в порядке убывания
word_dict = dict(Counter(word_list))

print(word_dict)


# Второй вариант длиннее, но без зависимостей

# text = input('Введите текст: ')
# text = text.casefold()
# text = text.strip().replace("’", '').replace("‘", '').replace('!', '')
# word_list = text.replace('.', '').replace('-', '').split()
#
# # Создаем пустой словарь и заполняем парами ключ:значение, предварительно проверяя наличие ключа
# word_dict = {}
# for word in word_list:
#     if word in word_dict:
#         word_dict[word] += 1
#     else:
#         word_dict[word] = 1
#
# # Вывод отсортированного по значениям словаря
# print(dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True)))
