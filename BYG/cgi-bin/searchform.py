#!/usr/bin/env python

#-----------------------------------------------------------------------
# searchform.py
# Author: Judah Guggenheim
#-----------------------------------------------------------------------

import common

#-----------------------------------------------------------------------

def main():

    # Print HTTP headers.

    print('Content-type: text/html; charset=utf-8')
    print()

    # Print content.

    print('<!DOCTYPE html>')
    print('<html>')
    print('<head>')
    print('<title>Before You Go</title>')
    print('</head>')
    print('<body>')
    common.print_header()
    print('<h1>Category Search</h1>')
    print('<form action="/cgi-bin/searchresults.py" method="get">')
    print('Please enter an event category:')
    print('<input type="text" name="category" autofocus>')
    print('<input type="submit" value="Go">')
    print('</form>')
    print('<br>')
    print('<br>')
    common.print_footer()
    print('</body>')
    print('</html>')

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
