class Item:
    def __init__(self, name, price, count):
        self.name = name
        self.count = count
        self.price = price
        self.total = self.count * self.price
        self.total_str = self.totalCalc()

    def totalCalc(self):
        if self.total < 1000:
            return self.total
        return f'{int(self.total/1000)}K'



apple = Item("Apple", 1, 0)
orange = Item("Orange", 2, 0)
