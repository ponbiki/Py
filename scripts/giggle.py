#!/usr/bin/environment python

import curses
import geo_shunt as gs
from pprint import pprint


class App(object):
    def __init__(self, screen):

        self.screen = screen

        x = 0
        x2 = 0
        x3 = 0
        cmd = None
        country_match = False

        while x != ord('0'):
            curses.start_color()
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

            self.screen.bkgd(curses.color_pair(2))
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
                        self.screen.addstr(2, 2, "Two-letter Country Code (e.g. US, NL)")
                        self.screen.addstr(4, 4, "1 - Browse Codes")
                        self.screen.addstr(5, 4, "2 - Enter Code")
                        self.screen.addstr(7, 4, "0 - Go Back")
                        self.screen.refresh()

                        x3 = self.screen.getch()

                        if x3 == ord('1'):
                            self.pad = curses.newpad(len(gs.countries) + 6, 50)
                            self.pad.bkgd(curses.color_pair(1))
                            pos = 3
                            self.pad.addstr(1, 1, "Press 'q' to exit")
                            for key in sorted(gs.countries.iterkeys()):
                                self.pad.addstr(pos, 2, key + " : " + gs.countries[key])
                                pos += 1
                            self.pad.refresh(0, 0, 5, 5, 20, 75)
                            pad_pos = 0
                            cmd = self.pad.getch()
                            while cmd != ord('q'):
                                if cmd == ord('z'):
                                    pad_pos += 5
                                    if pad_pos > len(gs.countries) - 13:
                                        pad_pos = len(gs.countries) - 13
                                    self.pad.refresh(pad_pos, 0, 5, 5, 20, 75)
                                    cmd = self.pad.getch()
                                elif cmd == ord('a'):
                                    pad_pos -= 5
                                    if pad_pos < 1:
                                        pad_pos = 1
                                    self.pad.refresh(pad_pos, 0, 5, 5, 20, 75)
                                    cmd = self.pad.getch()
                                else:
                                    pass

                        if x3 == ord('2'):
                            while country_match is False:
                                self.screen.clear()
                                self.screen.border(0)
                                self.country_code = self.get_param("Enter Valid Country Code").strip().upper()
                                if self.country_code in gs.countries:
                                    country_match = True
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

