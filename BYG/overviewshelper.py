#!/usr/bin/env python

#-----------------------------------------------------------------------
# overviewhelpers.py (Assignment 2)
# Author: Judah Guggenheim
#-----------------------------------------------------------------------

import sys
import textwrap

#-----------------------------------------------------------------------

# Function to escape SQLite wildcards
def escape_sql_wildcards(value):
    return value.replace("_", r"\_").replace("%", r"\%")

def print_wrapped(to_print):
   # Wrap title correctly and indent subsequent lines
    wrapped_text = textwrap.fill(to_print, width=72,
                           subsequent_indent=" " * 23,
                           break_long_words=False)
    print(wrapped_text)


DATABASE_URL = 'file:reg.sqlite?mode=ro'


def fetch_overviews(cursor, d, n, a, t):
    """
    Takes department, coursenumber, area, and title
    Returns err_msg, then list of lists (tuples?), each of 
    structure:
    ['classid', 'dept', 'coursenum', 'area', 'title']
    """
    dept = '%'
    num = '%'
    area = '%'
    title = '%'

    # Conditionally assign values from param input,
    # replacing the default if a param is not None
    # NOTE: Not sure this will work, bc of the way params come in
    if d:
        dept += escape_sql_wildcards(d) + '%'
    if n:
        num += escape_sql_wildcards(n) + '%'
    if a:
        area += escape_sql_wildcards(a) + '%'
    if t:
        title += escape_sql_wildcards(t) + '%'

    try:
        # Create a prepared statement and substitute values.
        stmt_str=("SELECT classid, dept, " +
                  "coursenum, area, title " +
            "FROM classes, crosslistings, courses " +
            "WHERE classes.courseid = courses.courseid " +
            "AND classes.courseid = crosslistings.courseid " +
            "AND dept LIKE ? ESCAPE '\\' " + 
            "AND coursenum LIKE ? ESCAPE '\\' " +
            "AND area LIKE ? ESCAPE '\\' " +
            "AND title LIKE ? ESCAPE '\\' " +
            "ORDER BY dept ASC, coursenum ASC, classid ASC " )
        cursor.execute(stmt_str, [dept, num, area, title])
        table = cursor.fetchall()
        return '', table

    except Exception as ex:
        # print(ex, file=sys.stderr)
        # sys.exit(1)
        err_msg = str(ex)
        return err_msg, []



def print_overviews(table):
    try:
         #Print Column Headers
        print("ClsId Dept CrsNum Area Title")
        print("----- ---- ------ ---- -----")

        for row in table:
            r_classid, r_dept, r_coursenum, r_area, r_title =row
            row_str = '%5s %4s %6s %4s %s' % (r_classid, r_dept,
                                              r_coursenum,
                                              r_area, r_title)

        # # Wrap title correctly and indent subsequent lines
        # wrapped_text = textwrap.fill(row_str, width=72,
        #                         subsequent_indent=" " * 23,
        #                         break_long_words=False)
        # print(wrapped_text)
        print_wrapped(row_str)

    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)
