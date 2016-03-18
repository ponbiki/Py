#!/usr/bin/environment python

import curses


class App(object):
    def __init__(self, screen):

        self.screen = screen
        x = 0
        x2 = 0

        while x != ord('0'):
            curses.start_color()
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

            self.screen.bkgd(curses.color_pair(1))
            self.screen.refresh()

            self.screen.border(0)
            self.screen.addstr(2, 2, "Geo Shunt Tool -- Please select an action")
            self.screen.addstr(4, 4, "1 - Search for an existing shunt")
            self.screen.addstr(5, 4, "2 - Add a new shunt")
            self.screen.addstr(6, 4, "3 - Edit an existing shunt")
            self.screen.addstr(7, 4, "4 - Delete an existing shunt")
            self.screen.addstr(9, 4, "0 - Exit")
            self.screen.refresh()

            x = screen.getch()

            if x == ord('1'):
                self.ip_addr = self.get_param("Enter partial or full IP address or CIDR")
                screen.refresh()

            if x == ord('2'):
                while x2 != ord('0'):
                    self.screen.clear()
                    self.screen.border(0)
                    self.screen.addstr(2, 2, "Shunt Protocol")
                    self.screen.addstr(4, 4, "1 - IPv4")
                    self.screen.addstr(5, 4, "2 - IPv6")
                    self.screen.addstr(7, 4, "0 - Go Back")
                    self.screen.refresh()

                    x2 = self.screen.getch()

                    if x2 == ord('1'):
                        self.screen.clear()
                        self.screen.border(0)
                        self.city_name = self.get_param("City Name")
                        self.state_name = self.get_param("State/Province/Territory Name")
                        self.country_name = self.get_param("Country Name")
                        self.time_zone = self.get_param("Time Zone")
                        self.screen.refresh()

                    if x2 == ord('0'):
                        curses.endwin()

            if x == ord('0'):
                curses.endwin()

    def get_param(self, prompt_string):
        curses.echo()
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, prompt_string)
        self.screen.refresh()
        x_input = self.screen.getstr(4, 4, 20)
        return x_input

if __name__ == '__main__':
    curses.wrapper(App)
