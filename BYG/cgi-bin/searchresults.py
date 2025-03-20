#!/usr/bin/env python

#-----------------------------------------------------------------------
# searchresults.py
# Author: Judah Guggenheim
#-----------------------------------------------------------------------

import os
import html # html.escape() is used to thwart CSS attacks
import parseargs
import common
import database

#-----------------------------------------------------------------------

def main():

    args_str = os.environ.get('QUERY_STRING', '')
    args = parseargs.parse(args_str)
    category = args.get('category', '')

    category = category.strip()

    if category == '':
        category = '(None)'
        events = []
    else:
        events = database.get_events(category) # Exception handling omitted

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
    print('<h1>Category Search Results</h1>')
    print('<h2>Events of Category ' + html.escape(category) + ':</h2>')
    if len(events) == 0:
        print('(None)<br>')
    else:
        pattern = '%s: <strong>%s</strong>: %s<br>'
        for event in events:
            print(pattern %
                (event['isbn'], event['title'], event['category']))
    print('<br>')
    print('<br>')
    print('Click here to do another ')
    print('<a href="/cgi-bin/searchform.py">category search</a>.')
    print('<br>')
    print('<br>')
    print('<br>')
    print('<br>')
    common.print_footer()
    print('</body>')
    print('</html>')

#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
