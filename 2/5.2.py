import re

# Открываем файл на чтение и считываем все строки в список
with open('input.txt', encoding='utf-8') as file:
    lst = file.readlines()

    # Создаем счетчик линий, начиная с 1
    line_index = 1

    for item in lst:
        # С помощью регулярного выражения удаляем все знаки препинания(включая нижнее подчеркивание) из каждой строки,
        #  обрезаем её и создаем список
        words_list = re.sub(r'[_\W]+', ' ', item).strip().split()

        # На основе сгенерированного списка считаем количество слов, содержащих больше 1 символа
        long_words_list = [word for word in words_list if len(word) > 1]
        long_words_count = len(long_words_list)

        # Выводим количество слов, номер строки и всю строку из длинных слов, распаковав список через *
        print(f'В {line_index} строке {long_words_count} слов')
        print(*long_words_list)
        print()

        # Увеличиваем счетчик для новой строки
        line_index += 1
