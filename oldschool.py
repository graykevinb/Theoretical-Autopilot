#This module handles the font end for drive_test.py

#MIT License

#Copyright (c) [2017] [Kevin Gray]

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import curses
from curses import wrapper
import time

stdscr = curses.initscr()
def main():
    print('hi')
    wrapper(init)
    x1 = 1
    x2 = 1
    x3 = 1
    x4 = 1
    x5 = 1
    x6 = 1
    x7 = 1
    x8 = 1
    x9 = 1
    while True:
        x1 += 1
        x2 += 2
        x3 += 3
        x4 += 4
        x5 += 5
        x6 += 6
        x7 += 7
        x8 += 8
        x9 += 9
        time.sleep(0.2)
        update(x1,x2,x3,x4,x5,x6,x7,x8,x9)
def init():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    stdscr.clear()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

def update(sensor_errors, general_errors, left_sensor, right_sensor, turning_direction, pid_error, pid_output, left_wheel, right_wheel):
    arguments = [sensor_errors, general_errors, left_sensor, right_sensor, turning_direction, pid_error,
            pid_output, left_wheel, right_wheel]
    argument_names = ['sensor_errors', 'general_errors', 'left_sensor', 'right_sensor', 'turning_direction', 'pid_error',
            'pid_output', 'left_wheel', 'right_wheel']
    stdscr.clear()
    for i in range(len(arguments)):
        stdscr.addstr(i, 1, '{0}: {1}'.format(argument_names[i], arguments[i]), curses.A_REVERSE)
    stdscr.refresh()

def reset():
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
