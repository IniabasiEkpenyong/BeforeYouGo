#!/usr/bin/env python

#-----------------------------------------------------------------------
# detailshelper.py
# Author: Judah Guggenheim (Assignment 2)

# Description: a helper file with fetch and print methods for regdetails
#-----------------------------------------------------------------------

import sys
import textwrap

#-----------------------------------------------------------------------

DATABASE_URL = 'file:reg.sqlite?mode=ro'

#------------Print methods - should be its own file, imported ----------

# Function to format the wrapped string before printing
def print_wrapped(to_print):
    wrapped_text = textwrap.fill(to_print, width=72,
                                 subsequent_indent=" " * 3,
                                 break_long_words=False)
    print(wrapped_text)

def print_class_details(classid, days, starttime,
                        endtime, bldg, roomnum):
    print("-------------")
    print("Class Details")
    print("-------------")

    print("Class Id:", classid)

    day_string = ''.join(days)
    print("Days:", day_string)

    print("Start time:", starttime)
    print("End time:", endtime)
    print("Building:", bldg)
    print("Room:", roomnum)

def print_course_details(courseid, deptcoursenums, area, title,
                         descrip, prereqs, prof_names):
    print("--------------")
    print("Course Details")
    print("--------------")

    print("Course Id:", courseid)

    for deptnum_dict in deptcoursenums:
        print("Dept and Number:", deptnum_dict.get('dept'),
              deptnum_dict.get('coursenum'))

    if area:
        print("Area:", area)
    else:
        print("Area:")

    title_print = "Title: " + title
    print_wrapped(title_print)

    descrip_print = "Description: " + descrip
    print_wrapped(descrip_print)

    prereqs_print = "Prerequisites: " + prereqs
    if prereqs:
        print_wrapped(prereqs_print)
    else:
        print("Prerequisites:")

    for name in prof_names:
        print("Professor:", name)

#-----------------------------------------------------------------------


#--------------------------Fetch methods ------------------------------

# Function to escape SQLite wildcards
def escape_sql_wildcards(value):
    return value.replace("_", r"\_").replace("%", r"\%")

def fetch_class_details(cursor, classid):
    """
    If a class with this classid exists, returns a list of
    [courseid, days, starttime, endtime, bldg, roomnum]
    Otherwise, prints the error message    
    """
    try:
        int(classid)
    except Exception:
        err_msg = "non-integer classid"
        print((f"{sys.argv[0]}:"+err_msg), file=sys.stderr)
        return err_msg, []

    # Fetch class details:
    stmt_str = ("SELECT courseid, days, " +
                "starttime, endtime, bldg, roomnum " +
                "FROM classes " +
                "WHERE classid = ? ")
    cursor.execute(stmt_str, [classid])


    class_details = cursor.fetchone()

    if classid == '' or classid is None:
        err_msg = 'missing classid'

    if not class_details:
        if classid == '' or classid is None:
            err_msg = 'missing classid'
        else:
            err_msg = (" no class with classid " +
                        str(classid) + " exists")
        # err_msg = str(er)
        print((f"{sys.argv[0]}:"+err_msg), file=sys.stderr)
        # sys.exit(1)
        return err_msg, []



    return '', class_details

def fetch_crosslisting_details(cursor, courseid):
    """
    Returns a list lists of [[dept1, num1], [dept2, num2]...]
    Must be used with a valid courseid, which can be found with the
    fetch_class_details() method given a valid classid
    """
    # Fetch crosslisting details
    stmt_str = "SELECT dept, coursenum "
    stmt_str += "FROM crosslistings "
    stmt_str += "WHERE courseid = ? "
    stmt_str += "ORDER BY dept ASC, coursenum ASC "
    cursor.execute(stmt_str, [courseid])
    crosslisting_details = cursor.fetchall()
    # print(f"Debug: Crosslisting String: {stmt_str}")
    return crosslisting_details

def fetch_course_details(cursor, courseid):
    """Returns a list of [area, title, descrip, prereqs]"""
    # Fetch course details
    stmt_str = "SELECT area, title, descrip, prereqs "
    stmt_str += "FROM courses "
    stmt_str += "WHERE courseid = ? "
    cursor.execute(stmt_str, [courseid])
    course_details = cursor.fetchone()
    # print(f"Debug: CourseId: {courseid}")
    # print(f"Debug: String: {stmt_str}")
    # print(f"DEBUG: Fetched course details: {course_details}")

    return course_details

# Return a list of ['name'] of length >=0
def fetch_prof_names(cursor, courseid):
    # Fetch prof names
    stmt_str = "SELECT profname "
    stmt_str += "FROM coursesprofs, profs "
    stmt_str += "WHERE profs.profid = coursesprofs.profid "
    stmt_str += "AND coursesprofs.courseid = ? "
    cursor.execute(stmt_str, [courseid])
    prof_names = cursor.fetchall()
    return prof_names
