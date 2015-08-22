#!/usr/local/bin/python3
import subprocess
sw = {
    'cs51':          '0',
    'cs29':          '1',
    'cs30':          '2',
    'fastmail':      '3',
    'cs52':          '4',
    'cs-lab21-c':    '5',
    'cs20':          '6',
    'cs35':          '7',
    'cs22':          '8',
    'cs-lab21-b':    '9',
    'cs49':          '10',
    'cs39':          '11',
    'cs-urchin-8':   '12',
    'cs-lab-8':      '13',
    'cs-lab21-a':    '14',
    'cs34':          '15',
    'cs-dedi-1':     '16',
    'cs32':          '17',
    'cs31':          '18',
    'cs-jobdiva':    '19',
    'cs33':          '20',
    'cs-lab-21-old': '21',
    'cs21':          '22',
    'cs46':          '23',
    'cs36':          '24',
    'cs47':          '25',
    'cs59':          '26',
    'temp':          '28'
    }
sw_list = sorted(list(sw.keys()))
separator = "\n"
list_str = separator.join(sw_list)
welcome = "\nPlease select a switch:\nTo disconnect, type ~ followed by CTRL+d\n\n" + list_str + "\n"
print(welcome)
selected = input()
while selected not in sw:
    print("Try a switch name in the list!\n")
    selected = input()
else:
    proc = subprocess.call('cu -l /dev/cuaU' + sw[selected], shell=True)