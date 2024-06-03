import curses
import logging

from sys import exit

from logCondenser import cleanUpLog
import enties
import maps
import Items

map = maps.testMap


def main(stdscr):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='logs/logIn.log', encoding='utf-8', level=logging.DEBUG,
                        format="%(levelname)s %(message)s", )

    # Entities
    player = enties.Merchant("Alen", 10, "@", 15, 20, 1, curses.COLOR_WHITE)
    player.addItem(Items.apple, 20)
    player.addItem(Items.orange, 15)
    testTrader = enties.Merchant("Tester", 10, "t", 18, 20)
    testTrader.setDialog(f'Hi im Jack if you want to trade with me press "b"')
    entities = [player, testTrader]

    stdscr.nodelay(True)
    curses.resizeterm(100, 100)
    curses.curs_set(0)
    itemsWindow = curses.newwin(45, 25, 1, 4)
    mapWindow = curses.newwin(45, 125, 1, 29)
    eventWindow = curses.newwin(45, 25, 1, 154)

    event_txt_line = 0
    event_txt = ''
    event_length = 1

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

        if 2 + event_txt_line + event_length > 45:
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
                    event_length += 1
                    line_length = len(word) + 2

            if 2 + event_txt_line + event_length > 45:
                eventWindow.erase()
            eventWindow.addstr(2 + event_txt_line, 1, out_txt)
            event_txt_line += event_length + 1
            event_txt = ''
            event_length = 1

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
            cleanUpLog("logs/logIn.log")
            exit()
        elif key == "KEY_LEFT":
            if player.y - 1 > 1 and player.getSurroundingsChar(mapWindow)[0] == ' ':  # don't technically need edge because
                player.y -= 1                                       # map boarder however keeping it for different maps
        elif key == "KEY_RIGHT":
            if player.y + 1 < 124 and player.getSurroundingsChar(mapWindow)[1] == ' ':
                player.y += 1
        elif key == "KEY_UP":
            if player.x - 1 > 0 and player.getSurroundingsChar(mapWindow)[2] == ' ':
                player.x -= 1
        elif key == "KEY_DOWN":
            if player.x + 1 < 44 and player.getSurroundingsChar(mapWindow)[3] == ' ':
                player.x += 1
        elif key == " ":
            for location in player.getNeighboringCords().values():
                logger.debug(f'{location}')
                for entity in entities:
                    if location == entity.getPosition():
                        event_txt = entity.dialog



curses.wrapper(main)
