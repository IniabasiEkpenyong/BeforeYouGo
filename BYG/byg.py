#!/usr/bin/env python

#-----------------------------------------------------------------------
# penny.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import time
import flask
import database
# import sys

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

def get_ampm():
    if time.strftime('%p') == 'AM':
        return 'morning'
    return 'afternoon'

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
# def index():
#     print("COS!!!")
#     html_code = flask.render_template('index.html',
#         ampm=get_ampm(),
#         current_time=get_current_time())
#     response = flask.make_response(html_code)
#     return response
#
# #---------------------------------------------------------------------
#
# @app.route('/index', methods=['GET'])
def search_form():
    prev_author = flask.request.cookies.get('prev_author')
    if prev_author is None:
        prev_author = '(None)'

    prev_dept = flask.request.cookies.get('prev_dept')
    if prev_dept is None:
        prev_dept = ''

    prev_num = flask.request.cookies.get('prev_num')
    if prev_num is None:
        prev_num = ''

    prev_area = flask.request.cookies.get('prev_area')
    if prev_area is None:
        prev_area = ''

    prev_title = flask.request.cookies.get('prev_title')
    if prev_title is None:
        prev_title = ''

    dept = flask.request.args.get('dept')
    if dept is None:
        dept = ''

    num = flask.request.args.get('num')
    if num is None:
        num = ''

    area = flask.request.args.get('area')
    if area is None:
        area = ''

    title = flask.request.args.get('title')
    if title is None:
        title = ''

    err_msg, courses = database.get_courses(
        dept, num, area, title)


    html_code = flask.render_template('index.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        err_msg = err_msg,
        courses = courses,
        prev_dept = prev_dept,
        prev_num = prev_num,
        prev_area = prev_area,
        prev_title = prev_title,
        prev_author=prev_author)
    response = flask.make_response(html_code)

    response.set_cookie('prev_dept', dept)
    response.set_cookie('prev_num', num)
    response.set_cookie('prev_area', area)
    response.set_cookie('prev_title', title)
    return response

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results():
    error_msg = ''

    try:
        prev_dept = flask.request.cookies.get('prev_dept', '')
        prev_num = flask.request.cookies.get('prev_num', '')
        prev_area = flask.request.cookies.get('prev_area', '')
        prev_title = flask.request.cookies.get('prev_title', '')

        classid = flask.request.args.get('classid')
        if classid is None:
            classid = ''
        # author = author.strip()

        if classid == '':
            # prev_classid = '(None)'
            class_info = []
        else:
            # prev_classid = classid
            error_msg, class_info = database.get_class_info(
                classid) # Exception handling omitted

        html_code = flask.render_template('searchresults.html',
            ampm=get_ampm(),
            current_time=get_current_time(),
            error_msg = error_msg,
            classid = classid,
            # issue here bc this could be None
            class_info = class_info,
            prev_dept = prev_dept,
            prev_num = prev_num,
            prev_area = prev_area,
            prev_title = prev_title
            # author=prev_author,
            # books=books
        )

    except Exception as ex:
        error_msg = str(ex)
        html_code = flask.render_template(
            'errmsg.html',
            error_msg = error_msg)
        response = flask.make_response(html_code)

    response = flask.make_response(html_code)

    # Do dept, num, area, title
    # response.set_cookie('prev_', prev_author)

    return response
