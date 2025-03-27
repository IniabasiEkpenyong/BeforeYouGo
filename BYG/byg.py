#!/usr/bin/env python

#-----------------------------------------------------------------------
# byg.py
# Author: Judah Guggenheim
#-----------------------------------------------------------------------

import time
import flask
import database as database
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
def home_page():
    html_code = flask.render_template('index.html',
        ampm=get_ampm(),
        current_time=get_current_time()
    )

    response = flask.make_response(html_code)
    return response



@app.route('/global', methods = ['GET'])
def search_form():
    prev_title = flask.request.cookies.get('prev_title')
    if prev_title is None:
        prev_title= ''

    title = flask.request.args.get('title')
    if title is None:
        title = ''

    prev_cat = flask.request.cookies.get('prev_cat')
    if prev_cat is None:
        prev_cat= ''

    cat = flask.request.args.get('cat')
    if cat is None:
        cat = ''

    prev_loc = flask.request.cookies.get('prev_loc')
    if prev_loc is None:
        prev_loc= ''

    loc = flask.request.args.get('loc')
    if loc is None:
        loc = ''

    prev_descrip = flask.request.cookies.get('prev_descrip')
    if prev_descrip is None:
        prev_descrip= ''

    descrip = flask.request.args.get('descrip')
    if descrip is None:
        descrip = ''

    err_msg, events = database.get_events(
        title=title, cat = cat,
        loc = loc, descrip = descrip)

    html_code = flask.render_template('global.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        err_msg = err_msg,
        events = events,
        prev_cat = prev_cat
    )

    response = flask.make_response(html_code)

    response.set_cookie('prev_title', title)
    response.set_cookie('prev_cat', cat)
    response.set_cookie('prev_loc', loc)
    response.set_cookie('prev_descrip', descrip)
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
