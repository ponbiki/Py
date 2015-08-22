#!/usr/local/bin/python3
import psutil
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
    arg = '/dev/cuaU' + sw[selected]
    proc = subprocess.Popen(['cu', '-l', arg], shell=False)
    errval = proc.communicate()[0]
    if (proc.returncode) != 0:
        print("This console may be in use by someone else.\nWould you like to preempt the connection (y/n)")
        preempt = input()
        while preempt != "y" and preempt != "n":
            print("Please choose (y/n)")
            preempt = input()
        if preempt == "y":
            proc_cmd = ['cu', '-l', arg]
            for prc in psutil.pids():
                p = psutil.Process(prc)
                if p.cmdline() == proc_cmd:
                    p.terminate()
                    break
            subprocess.call(['cu', '-l', arg], shell=False)
        else:
            print("Exiting")
            exit()
