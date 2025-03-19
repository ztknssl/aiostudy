class Car:
    def __init__(self, make, model, year, odometer_reading=0):
        self.__make = make
        self.__model = model
        self.__year = year
        self.__odometer_reading = odometer_reading

    def get_description(self):
        print(f'Марка: {self.__make}, Модель: {self.__model}, Год: {self.__year}')

    def read_odometer(self):
        print(f'Пробег: {self.__odometer_reading} км')

    def update_odometer(self, new_reading):
        if new_reading <= self.__odometer_reading:
            print(f'Обновленный пробег {new_reading} должен быть больше текущего пробега {self.__odometer_reading}')
        else:
            self.__odometer_reading = new_reading
            print(f'Обновляем пробег на {new_reading} км')

    def increment_odometer(self, km):
        if km > 0:
            self.__odometer_reading += km
            print(f'Увеличиваем пробег на {km} км')
        else:
            print('Введите положительное число')
