class Fruit:
    def __init__(self, name: str):
        self.name = name

    def get_name(self):
        return self.name

class Apple(Fruit):
    @staticmethod
    def taste():
        print('Яблоко сладкое')

class Banana(Fruit):
    @staticmethod
    def taste():
        print('Банан мягкий')


fruit = Fruit(name="Фрукт")
print(fruit.get_name())

apple = Apple(name="Яблоко")
print(apple.get_name())
apple.taste()

banana = Banana(name="Банан")
print(banana.get_name())
banana.taste()
