#!/usr/bin/environment python

import curses

import geo_shunt as gs


class App(object):
    def __init__(self, screen):

        self.screen = screen

        x1 = None  # main menu
        x2 = None  # New Shunt - IPv4/6 Menu
        x3 = None  # New Shunt - Country Code Menu
        x4 = None  # New Shunt - State/Province Menu
        x5 = None  # New Shunt - Confirm Shunt
        country_match = False
        state_match = False
        province_match = False

        while x1 != ord('0'):
            curses.start_color()
            curses.curs_set(0)
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

            x1 = screen.getch()

            if x1 == ord('1'):
                self.screen.clear()
                self.screen.border(0)
                self.ip_address = self.get_param("Enter partial or full IP address or CIDR")
                self.screen.refresh()

            if x1 == ord('2'):
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
                        while x3 != ord('0'):
                            self.screen.clear()
                            self.screen.border(0)
                            self.screen.addstr(2, 2, "Two-letter Country Code (e.g. US, NL)")
                            self.screen.addstr(4, 4, "1 - Browse Codes")
                            self.screen.addstr(5, 4, "2 - Enter Code")
                            self.screen.addstr(7, 4, "0 - Go Back")
                            self.screen.refresh()

                            x3 = self.screen.getch()

                            if x3 == ord('1'):
                                self.screen.clear()
                                curses.curs_set(0)
                                self.pad = curses.newpad(len(gs.countries) + 6, 50)
                                self.pad.bkgd(curses.color_pair(1))
                                pos = 3
                                self.pad.addstr(1, 1, "'z': page down, 'a': page up")
                                srt_cc = [(k, v) for v, k in sorted([(v, k) for k, v in gs.countries.items()])]
                                for cntry in srt_cc:
                                    self.pad.addstr(pos, 2, cntry[0] + " : " + cntry[1])
                                    pos += 1
                                self.pad.refresh(0, 0, 4, 10, 20, 75)
                                pad_pos = 0
                                cmd = self.pad.getch()
                                while cmd != ord('q'):
                                    if cmd == ord('z'):
                                        pad_pos += 5
                                        if pad_pos > len(gs.countries) - 13:
                                            pad_pos = len(gs.countries) - 13
                                        self.pad.refresh(pad_pos, 0, 4, 10, 20, 75)
                                        cmd = self.pad.getch()
                                    elif cmd == ord('a'):
                                        pad_pos -= 5
                                        if pad_pos < 1:
                                            pad_pos = 1
                                        self.pad.refresh(pad_pos, 0, 4, 10, 20, 75)
                                        cmd = self.pad.getch()
                                    else:
                                        break
                            elif x3 == ord('2'):
                                while country_match is False:
                                    self.screen.clear()
                                    self.screen.border(0)
                                    self.country_code = self.get_param("Enter Valid Country Code").strip().upper()
                                    self.screen.refresh()
                                    if self.country_code in gs.countries:
                                        country_match = True

                                    while x4 != ord('0'):
                                        if self.country_code == 'US':
                                            self.screen.clear()
                                            self.screen.border(0)
                                            self.screen.addstr(2, 2, "Two-letter US State Code (e.g. CA, NY)")
                                            self.screen.addstr(4, 4, "1 - Browse Codes")
                                            self.screen.addstr(5, 4, "2 - Enter Code")
                                            self.screen.addstr(7, 4, "0 - Go Back")
                                            self.screen.refresh()

                                            x4 = self.screen.getch()

                                            if x4 == ord('1'):
                                                self.screen.clear()
                                                curses.curs_set(0)
                                                self.pad = curses.newpad(len(gs.states) + 6, 50)
                                                self.pad.bkgd(curses.color_pair(1))
                                                pos = 3
                                                self.pad.addstr(1, 1, "'z': page down, 'a': page up")
                                                srt_st = [(k, v) for v, k in sorted([(v, k) for k, v in gs.states.items()])]
                                                for state in srt_st:
                                                    self.pad.addstr(pos, 2, state[0] + " : " + state[1])
                                                    pos += 1
                                                self.pad.refresh(0, 0, 4, 10, 20, 75)
                                                pad_pos = 0
                                                cmd = self.pad.getch()
                                                while cmd != ord('q'):
                                                    if cmd == ord('z'):
                                                        pad_pos += 5
                                                        if pad_pos > len(gs.states) - 13:
                                                            pad_pos = len(gs.states) - 13
                                                        self.pad.refresh(pad_pos, 0, 4, 10, 20, 75)
                                                        cmd = self.pad.getch()
                                                    elif cmd == ord('a'):
                                                        pad_pos -= 5
                                                        if pad_pos < 1:
                                                            pad_pos = 1
                                                        self.pad.refresh(pad_pos, 0, 4, 10, 20, 75)
                                                        cmd = self.pad.getch()
                                                    else:
                                                        break
                                            elif x4 == ord('2'):
                                                while state_match is False:
                                                    self.screen.clear()
                                                    self.screen.border(0)
                                                    self.state_code = self.get_param("Enter Valid State Code").strip().upper()
                                                    self.screen.refresh()
                                                    if self.state_code in gs.states:
                                                        state_match = True
                                                        self.screen.clear()
                                                        self.screen.border(0)
                                                        self.city_name = self.get_param("Enter City Name").strip().title()
                                                        screen.refresh()

                                        elif self.country_code == 'CA':
                                            self.screen.clear()
                                            self.screen.border(0)
                                            self.screen.addstr(2, 2, "Two-letter Canadian Province Code (e.g. BC, ON)")
                                            self.screen.addstr(4, 4, "1 - Browse Codes")
                                            self.screen.addstr(5, 4, "2 - Enter Code")
                                            self.screen.addstr(7, 4, "0 - Go Back")
                                            self.screen.refresh()

                                            x4 = self.screen.getch()

                                            if x4 == ord('1'):
                                                self.screen.clear()
                                                curses.curs_set(0)
                                                self.pad = curses.newpad(len(gs.provinces) + 6, 50)
                                                self.pad.bkgd(curses.color_pair(1))
                                                pos = 3
                                                self.pad.addstr(1, 1, "'z': page down, 'a': page up")
                                                srt_pv = [(k, v) for v, k in sorted([(v, k) for k, v in gs.provinces.items()])]
                                                for prov in srt_pv:
                                                    self.pad.addstr(pos, 2, prov[0] + " : " + prov[1])
                                                    pos += 1
                                                self.pad.refresh(0, 0, 4, 10, 20, 75)
                                                pad_pos = 0
                                                cmd = self.pad.getch()
                                                while cmd != ord('q'):
                                                    if cmd == ord('z'):
                                                        pad_pos += 5
                                                        if pad_pos > len(gs.provinces) - 13:
                                                            pad_pos = len(gs.provinces) - 13
                                                        self.pad.refresh(pad_pos, 0, 4, 10, 20, 75)
                                                        cmd = self.pad.getch()
                                                    elif cmd == ord('a'):
                                                        pad_pos -= 5
                                                        if pad_pos < 1:
                                                            pad_pos = 1
                                                        self.pad.refresh(pad_pos, 0, 4, 10, 20, 75)
                                                        cmd = self.pad.getch()
                                                    else:
                                                        break
                                            elif x4 == ord('2'):
                                                while province_match is False:
                                                    self.screen.clear()
                                                    self.screen.border(0)
                                                    self.province_code = self.get_param("Enter Valid Province Code").strip().upper()
                                                    self.screen.refresh()
                                                    if self.province_code in gs.provinces:
                                                        province_match = True
                                                        self.screen.clear()
                                                        self.screen.border(0)
                                                        self.city_name = self.get_param("Enter City Name").strip().title()
                                                        self.ipv4_addr = gs.ipv4_validate(self.get_param("Enter IPv4 CIDR").strip())
                                                        screen.refresh()

                                                        if x5 != ord('0'):

                                                            self.screen.clear()
                                                            self.screen.border(0)
                                                            self.screen.addstr(2, 2, "Proposed Shunt")
                                                            self.screen.addstr(4, 4, " Country => %s" % gs.countries[self.country_code])
                                                            self.screen.addstr(5, 4, "Province => %s" % gs.provinces[self.province_code])
                                                            self.screen.addstr(6, 4, "    City => %s" % self.city_name)
                                                            self.screen.addstr(7, 4, "IP Address => %s" % self.ipv4_addr)
                                                            screen.refresh()

                                                            x5 = self.screen.getch()

                    if x2 == ord('0'):
                        curses.endwin()

            if x1 == ord('0'):
                curses.endwin()

    def get_param(self, prompt_string):
        curses.echo()
        curses.curs_set(1)
        self.screen.clear()
        self.screen.border(0)
        self.screen.addstr(2, 2, prompt_string)
        self.screen.refresh()
        x_input = self.screen.getstr(4, 4, 20)
        curses.curs_set(0)
        curses.noecho()
        return x_input

if __name__ == '__main__':
    curses.wrapper(App)
