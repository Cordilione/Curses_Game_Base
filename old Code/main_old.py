import curses
import logging

from sys import exit

from logCondenser import cleanUpLog
import Merchant
import maps
import Items

map = maps.testMap


def main(stdscr):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='../logs/logIn.log', encoding='utf-8', level=logging.DEBUG,
                        format="%(levelname)s %(message)s", )

    # Entities
    player = Merchant.Trader("Alen", 10, "@", 15, 20)
    player.addItem(Items.apple, 20)
    player.addItem(Items.orange, 15)
    testTrader = Merchant.Trader("Tester", 10, "t", 18, 20, 2, curses.COLOR_BLUE)
    entities = [player, testTrader]

    stdscr.nodelay(True)
    curses.resizeterm(100, 100)
    curses.curs_set(0)
    itemsWindow = curses.newwin(45, 25, 1, 4)
    mapWindow = curses.newwin(45, 125, 1, 29)
    eventWindow = curses.newwin(45, 25, 1, 154)

    event_txt_line = 0
    event_txt = ''
    event_legnth = 1

    while True:

        itemsWindow.erase()
        itemsWindow.box()
        itemsWindow.addstr(1, 1, "      Your Items       ", curses.A_UNDERLINE | curses.A_BOLD)
        itemsWindow.addstr(2, 1, f"Name  Count Price Total", curses.A_BOLD)
        line_count = 0
        player_total = 0
        for item in player.inventory:
            itemsWindow.addstr(3 + line_count, 1, f"{item}")
            itemsWindow.addstr(3 + line_count, 9, f"{player.inventory[item].count}")
            itemsWindow.addstr(3 + line_count, 14, f"${player.inventory[item].price}")
            itemsWindow.addstr(3 + line_count, 20, f"${player.inventory[item].total_str}")
            player_total += player.inventory[item].total
            line_count += 1
        itemsWindow.addstr(3 + line_count, 1, f"Total Item Value: ${player_total}", curses.A_BOLD | curses.A_ITALIC)

        if 2 + event_txt_line + event_legnth > 45:
            eventWindow.erase()
            event_txt_line = 0

        eventWindow.box()
        eventWindow.addstr(1, 1, "        Events         ", curses.A_UNDERLINE | curses.A_BOLD)
        if event_txt != '':
            event_array = event_txt.split(' ')
            line_length = 0
            out_txt = ''
            for word in event_array:
                line_length += len(word)
                if line_length < 23:
                    out_txt += word + ' '
                    line_length += 1
                else:
                    out_txt += '\n ' + word + ' '
                    event_legnth += 1
                    line_length = len(word) + 2

            if 2 + event_txt_line + event_legnth > 45:
                eventWindow.erase()
            eventWindow.addstr(2 + event_txt_line, 1, out_txt)
            event_txt_line += event_legnth + 1
            event_txt = ''
            event_legnth = 1

        mapWindow.erase()
        mapWindow.box()
        linecount = 1
        for line in map:
            mapWindow.addstr(linecount, 1, line)
            linecount += 1
        for entity in entities:
            mapWindow.addstr(entity.x, entity.y, entity.char, entity.colorID)

        itemsWindow.refresh()
        mapWindow.refresh()
        eventWindow.refresh()
        stdscr.refresh()

        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "q":
            cleanUpLog("../logs/logIn.log")
            exit()
        elif key == "KEY_LEFT":
            attrs = mapWindow.inch(player.x, player.y - 1)
            ch = str(chr(attrs & 0xFF))
            # logger.debug(f'To the Left is a "{ch}"')
            if player.y - 1 > 1 and ch == " ":
                player.y -= 1
        elif key == "KEY_RIGHT":
            attrs = mapWindow.inch(player.x, player.y + 1)
            ch = str(chr(attrs & 0xFF))
            # logger.debug(f'To the Right is a "{ch}"')
            if player.y + 1 < 124 and ch == " ":
                player.y += 1
        elif key == "KEY_UP":
            attrs = mapWindow.inch(player.x - 1, player.y)
            ch = str(chr(attrs & 0xFF))
            # logger.debug(f'Above is a "{ch}"')
            if player.x - 1 > 0 and ch == " ":
                player.x -= 1
        elif key == "KEY_DOWN":
            attrs = mapWindow.inch(player.x + 1, player.y)
            ch = str(chr(attrs & 0xFF))
            # logger.debug(f'Below is a "{ch}"')
            if player.x + 1 < 44 and ch == " ":
                player.x += 1
        elif key == "t":
            # Get all nearby Char
            allch = []
            # Left
            attrs = mapWindow.inch(player.x, player.y - 1)
            allch.append(str(chr(attrs & 0xFF)))
            # Right
            attrs = mapWindow.inch(player.x, player.y + 1)
            allch.append(str(chr(attrs & 0xFF)))
            # Above
            attrs = mapWindow.inch(player.x - 1, player.y)
            allch.append(str(chr(attrs & 0xFF)))
            # Below
            attrs = mapWindow.inch(player.x + 1, player.y)
            allch.append(str(chr(attrs & 0xFF)))

            for char in allch:
                if char == "t":
                    event_txt = "That's trader Jim he doesnt have anything right now"
                    logger.debug('We are Near a Trader Hello')
            # todo: Check for a Nearby NPC and Talk with them
            # todo: Make NPCs
            # todo: Make NPCs have Dialog
            # todo: Make Chat Box


curses.wrapper(main)
