#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import sqlite3
import contextlib
import overviewshelper
# import detailshelper

#-----------------------------------------------------------------------

_DATABASE_URL = 'file:bucket_list.sqlite?mode=rw'

#-----------------------------------------------------------------------


def get_events(title = '', cat = '', loc  = '', descrip = ''):
    events = []

    try:
        with sqlite3.connect(_DATABASE_URL, isolation_level=None,
                             uri=True) as connection:
                with contextlib.closing(connection.cursor()) as cursor:
                    query_str = "SELECT bucket_id, title, contact, area, "
                    query_str += "descrip, category, cloudinary_id "                    
                    query_str += "FROM bucket_list "
                    query_str += "WHERE title LIKE ? ESCAPE '\\' "
                    query_str += "AND category LIKE ? ESCAPE '\\' "
                    query_str += "AND area LIKE ? ESCAPE '\\' "
                    query_str += "AND descrip LIKE ? ESCAPE '\\' "
                    cursor.execute(query_str, 
                                   ['%'+title+'%', '%'+cat+'%',
                                    '%'+loc+'%', '%'+descrip+'%'])
                    table = cursor.fetchall()
                for row in table:
                     event = {'bucket_id': row[0], 'title': row[1],
                             'contact': row[2], 'loc': row[3],
                             'descrip': row[4], 'cat': row[5],
                             'cloudinary_id': row[6]}
                     events.append(event)
        return '', events
    
    except Exception as ex:
        # err_msg = str(ex)
        print(ex)
        err_msg = 'A server error occured. '
        err_msg +='Please contact the system administrator.'
        return err_msg, []
            

#def get_courses(dept = None, num = None, area = None, title = None):
#    """
#    Return list of courses, with each course as a dict with keys of
#    classid, dept, coursenum, area, title.
#    Return 'err_msg', courses
#    """
#    courses = []
#    try:
#        with sqlite3.connect(_DATABASE_URL, isolation_level=None,
#            uri=True) as connection:
#
#            with contextlib.closing(connection.cursor()) as cursor:
#
#                error_msg, table = overviewshelper.fetch_overviews(
#                    cursor, dept, num, area, title)
#                if error_msg != '':
#                    err_msg = 'A server error occured. Please '
#                    err_msg +='contact the system administrator.'
#                    return err_msg, []
#                for row in table:
#                    course = {'classid': row[0], 'dept': row[1],
#                        'coursenum': row[2], 'area': row[3], 
#                        'title': row[4]}
#                    courses.append(course)
#
#        return '', courses
#
#    except Exception as ex:
#        # err_msg = str(ex)
#        err_msg = 'A server error occured. '
#        err_msg +='Please contact the system administrator.'
#        return err_msg, []
#
#
#def get_class_info(classid = ""):
#    """
#    return list of [class_details, course_details, 
#                    cross_details, prof_details]
#    return 'err_msg', class_info
#    """
#    try:
#        with sqlite3.connect(_DATABASE_URL, isolation_level=None,
#        uri=True) as connection:
#
#            with contextlib.closing(connection.cursor()) as cursor:
#                err_msg,class_details=detailshelper.fetch_class_details(
#                    cursor, classid)
#
#                if err_msg:
#                    return err_msg, []
#
#                courseid = class_details[0]
#
#                course_details = detailshelper.fetch_course_details(
#                    cursor, courseid)
#
#                cross_details =detailshelper.fetch_crosslisting_details(
#                    cursor, courseid)
#
#                prof_details = detailshelper.fetch_prof_names(
#                           cursor, courseid)
#        return '', [class_details, course_details,
#                cross_details, prof_details]
#
#    except Exception as ex:
#        # error_msg = str(ex)
#        err_msg = 'A server error occured. '
#        err_msg += 'Please contact the system administrator.'
#        return err_msg, []
#

#-----------------------------------------------------------------------

def _test():
    err_msg, events = get_events(category= 'creative')
    print('err_msg: ', err_msg)
    for event in events:
        printstr = ''
        printstr += 'Name: ' + str(event['title'])
        print(printstr)

if __name__ == '__main__':
    _test()
