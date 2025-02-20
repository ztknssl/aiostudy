# Открываем файл input.txt на чтение и записываем список строк
with open('input.txt', encoding='utf-8') as file:
    lst = file.readlines()

# Открываем файл output.txt на запись и записываем в него строки из обновленного через генерацию списка
with open('output.txt', 'w', encoding='utf-8') as file:
    file.writelines([item.replace(' ', '_') for item in lst])