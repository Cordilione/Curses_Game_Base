import curses
import logging

import Items

logger = logging.getLogger(__name__)
logging.basicConfig(filename='logs/logIn.log', encoding='utf-8', level=logging.DEBUG,
                    format="%(levelname)s %(message)s", )


class NPC:
    def __init__(self, name, char="?", x=1, y=1,
                 colorID=1, colorFG=curses.COLOR_WHITE, colorBG=curses.COLOR_BLACK):
        curses.init_pair(colorID, colorFG, colorBG)
        self.name = name
        self.char = char
        self.colorID = curses.color_pair(colorID)
        self.x = x
        self.y = y
        self.dialog = 'Im an NPC'

    def getSurroundingsChar(self, window) -> list:  # order Left Right Up Down
        # Get all nearby Char
        all_surroundings = []
        # Left
        attrs = window.inch(self.x, self.y - 1)
        all_surroundings.append(str(chr(attrs & 0xFF)))
        # Right
        attrs = window.inch(self.x, self.y + 1)
        all_surroundings.append(str(chr(attrs & 0xFF)))
        # Above
        attrs = window.inch(self.x - 1, self.y)
        all_surroundings.append(str(chr(attrs & 0xFF)))
        # Below
        attrs = window.inch(self.x + 1, self.y)
        all_surroundings.append(str(chr(attrs & 0xFF)))

        return all_surroundings

    def getNeighboringCords(self) -> dict:
        neihbors = {
            'Left': (self.x, self.y - 1),
            'Right': (self.x, self.y + 1),
            'Up': (self.x - 1, self.y),
            'Down': (self.x + 1, self.y)
        }
        return neihbors

    def getPosition(self) -> tuple:
        return (self.x, self.y)

    def setDialog(self, dialog):
        self.dialog = dialog


class Merchant(NPC):
    def __init__(self, name, cash=0, char="T", x=1, y=1,
                 colorID=2, colorFG=curses.COLOR_YELLOW, colorBG=curses.COLOR_BLACK):
        super().__init__(name=name, char=char, x=x, y=y, colorID=colorID, colorFG=colorFG, colorBG=colorBG)
        self.cash = cash
        self.inventory = {}

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
                # todo: Handle
        else:
            print("Error: cant find Item")
            # todo: Handle

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
