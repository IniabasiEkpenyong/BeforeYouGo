#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Judah Guggenheim
#-----------------------------------------------------------------------
import os
import sqlite3
import contextlib

#-----------------------------------------------------------------------

# _DATABASE_URL = 'file:bucket_list.sqlite?mode=ro'
#_DATABASE_URL = 'file:/Users/judahguggenheim/Desktop/COS_333/BYG/cgi-bin/bucket_list.sqlite?mode=ro'
# ^^ This is a problem that it only works on my computer??
# Automatically find the script's directory (cgi-bin) and locate the database file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # This gets the cgi-bin path
DATABASE_PATH = os.path.join(BASE_DIR, "bucket_list.sqlite")  # Path to the database

_DATABASE_URL = f"file:{DATABASE_PATH}?mode=ro"  # Use this as the database URL

#-----------------------------------------------------------------------

def get_events(category):
    events = []
    
    with sqlite3.connect(_DATABASE_URL, isolation_level=None,
                         uri=True) as connection:
            
            with contextlib.closing(connection.cursor()) as cursor:
                query_str = "SELECT isbn, title, category FROM bucket_list "
                query_str += "WHERE category LIKE ?"
                cursor.execute(query_str, [category+'%'])
            
                table = cursor.fetchall()
            for row in table:
                 event = {'isbn': row[0], 'title': row[1],
                         'category': row[2]}
                 events.append(event)
            
    return events

#-----------------------------------------------------------------------

def _test():
    print("Content-Type: text/html\n")
    print("<h1>Debugging Output</h1>")
    
    try:
        print("<p>Attempting to retrieve events...</p>")
        events = get_events('creative')
        
        if not events:
            print("<p>No events found.</p>")
        
        for event in events:
            print(f"<p>{event['isbn']} - {event['title']} - {event['category']}</p>")
    
    except Exception as e:
        print(f"<p>Error: {e}</p>")


if __name__ == '__main__':
    _test()