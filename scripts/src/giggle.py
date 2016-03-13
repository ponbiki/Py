#!/usr/bin/environment python

import curses


def get_param(screen, prompt_string):
    screen.clear()
    screen.border(0)
    screen.addstr(2, 2, prompt_string)
    screen.refresh()
    x_input = screen.getstr(4, 4, 20)
    return x_input


def main(screen):

    x = 0
    x2 = 0

    while x != ord('0'):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        screen.bkgd(curses.color_pair(1))
        screen.refresh()

        screen.border(0)
        screen.addstr(2, 2, "Geo Shunt Tool -- Please select an action")
        screen.addstr(4, 4, "1 - Search for an existing shunt")
        screen.addstr(5, 4, "2 - Add a new shunt")
        screen.addstr(6, 4, "3 - Edit an existing shunt")
        screen.addstr(7, 4, "4 - Delete an existing shunt")
        screen.addstr(9, 4, "0 - Exit")
        screen.refresh()

        x = screen.getch()

        if x == ord('1'):
            ip_addr = get_param("Enter partial or full IP address or CIDR")
            screen.refresh()

        if x == ord('2'):
            while x2 != ord('0'):
                screen.clear()
                screen.border(0)
                screen.addstr(2, 2, "Shunt Protocol")
                screen.addstr(4, 4, "1 - IPv4")
                screen.addstr(5, 4, "2 - IPv6")
                screen.addstr(7, 4, "0 - Go Back")
                screen.refresh()

                x2 = screen.getch()

                if x2 == ord('1'):
                    screen.clear()
                    screen.border(0)
                    city_name = get_param("City Name")
                    state_name = get_param("State/Province/Territory Name")
                    country_name = get_param("Country Name")
                    time_zone = get_param("Time Zone")
                    screen.refresh()

                if x2 == ord('0'):
                    curses.endwin()

        if x == ord('0'):
            curses.endwin()

try:
    curses.wrapper(main)
except KeyboardInterrupt:
    print "User requested exti!"
    exit()