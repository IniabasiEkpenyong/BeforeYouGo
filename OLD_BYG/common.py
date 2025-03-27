#!/usr/bin/env python

#-----------------------------------------------------------------------
# common.py
# Author: Judah Guggenheim
#-----------------------------------------------------------------------

import time

#-----------------------------------------------------------------------

def print_header():
    if time.strftime('%p') == "AM":
        ampm = 'morning'
    else:
        ampm = 'afternoon'
    print('<hr>')
    print('Good ')
    print(ampm)
    print(' and welcome to <strong>Before You Go!</strong>')
    print('<hr>')

#-----------------------------------------------------------------------

def print_footer():
    print('<hr>')
    print('Today is ')
    print(time.asctime(time.localtime()))
    print('.<br>')
    print('Created by ')
    print('<a href="https://www.linkedin.com/in/judah-guggenheim-6b1a39208/">')
    print('Judah Guggenheim</a>')
    print('<hr>')

#-----------------------------------------------------------------------

# For testing:

def _test():
    print_header()
    print()
    print()
    print_footer()

if __name__ == '__main__':
    _test()
