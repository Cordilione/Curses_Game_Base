import curses

import Items


class Trader:
    def __init__(self, name, sCash=0, char="?", x=1, y=1, colorID=1, colorFG=curses.COLOR_WHITE, colorBG=curses.COLOR_BLACK, ):
        curses.init_pair(colorID, colorFG, colorBG)
        self.name = name
        self.cash = sCash
        #self.Items = []
        self.inventory = {}
        self.char = char
        self.colorID = curses.color_pair(colorID)
        self.x = x
        self.y = y

    def addItem(self, item, amount):
        if item.name in self.inventory:
            self.inventory[item.name].count += amount
        else:
            self.inventory[item.name] = Items.Item(item.name, item.price, amount)

    def sellItem(self, item, amount):
        if item.name in self.inventory:
            if amount <= self.inventory[item.name].count:
                self.removeItem(item.name, amount)
                self.cash += item.price * amount
            else:
                print("Error: dont have enough")
                # todo: Handdle
        else:
            print("Error: cant find Item")
            # todo: Handdle

    def removeItem(self, name, amount):
        if name in self.inventory:
            if self.inventory[name].count >= amount:
                self.inventory[name].count -= amount
                if self.inventory[name].count == 0:
                    del self.inventory[name]
            else:
                print("Error: Not Enough items in inventory")
                # Todo: Handle properly
        else:
            print("Error: Item not found to remove")
            # Todo: Handle properly

    def buyItem(self, item):
        if self.cash >= item.price:
            self.cash = self.cash - item.price

            self.addItem(item, 1)
        else:
            print("Not enough Cash")
            # todo: Handle not having enough with a pop up or in other way
