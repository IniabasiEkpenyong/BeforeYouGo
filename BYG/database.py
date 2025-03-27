#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sqlite3
import contextlib
import overviewshelper
import detailshelper

#-----------------------------------------------------------------------

_DATABASE_URL = 'file:bucketlist.sqlite?mode=rw'

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

def get_courses(dept = None, num = None, area = None, title = None):
    """
    Return list of courses, with each course as a dict with keys of
    classid, dept, coursenum, area, title.
    Return 'err_msg', courses
    """
    courses = []
    try:
        with sqlite3.connect(_DATABASE_URL, isolation_level=None,
            uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:

                error_msg, table = overviewshelper.fetch_overviews(
                    cursor, dept, num, area, title)
                if error_msg != '':
                    err_msg = 'A server error occured. Please '
                    err_msg +='contact the system administrator.'
                    return err_msg, []
                for row in table:
                    course = {'classid': row[0], 'dept': row[1],
                        'coursenum': row[2], 'area': row[3], 
                        'title': row[4]}
                    courses.append(course)

        return '', courses

    except Exception as ex:
        # err_msg = str(ex)
        err_msg = 'A server error occured. '
        err_msg +='Please contact the system administrator.'
        return err_msg, []


def get_class_info(classid = ""):
    """
    return list of [class_details, course_details, 
                    cross_details, prof_details]
    return 'err_msg', class_info
    """
    try:
        with sqlite3.connect(_DATABASE_URL, isolation_level=None,
        uri=True) as connection:

            with contextlib.closing(connection.cursor()) as cursor:
                err_msg,class_details=detailshelper.fetch_class_details(
                    cursor, classid)

                if err_msg:
                    return err_msg, []

                courseid = class_details[0]

                course_details = detailshelper.fetch_course_details(
                    cursor, courseid)

                cross_details =detailshelper.fetch_crosslisting_details(
                    cursor, courseid)

                prof_details = detailshelper.fetch_prof_names(
                           cursor, courseid)
        return '', [class_details, course_details,
                cross_details, prof_details]

    except Exception as ex:
        # error_msg = str(ex)
        err_msg = 'A server error occured. '
        err_msg += 'Please contact the system administrator.'
        return err_msg, []


#-----------------------------------------------------------------------

def _test():

    courses = get_courses(dept = 'cos', area = 'qr')
    for course in courses:
        printstr = ''
        printstr += 'classid: ' + str(course['classid']) + ', '
        printstr += 'dept: ' + course['dept'] + ', '
        printstr += 'coursenum: ' + course['coursenum'] + ', '
        printstr += 'area: ' + course['area'] + ', '
        printstr += 'title: ' + course['title']
        print(printstr)

if __name__ == '__main__':
    _test()
