#!/usr/bin/env python

#-----------------------------------------------------------------------
# byg.py
# Author: Judah Guggenheim
#-----------------------------------------------------------------------

import time
import flask
import database as database
from flask import Flask, session, redirect, render_template, request, make_response
import sqlalchemy
import sqlalchemy.orm
import auth
import os

from models import User, UserBucket

from werkzeug.security import generate_password_hash, check_password_hash

# import sys

#-----------------------------------------------------------------------

# app = flask.Flask(__name__, template_folder='.')
from top import app 


# app.secret_key = 'secret_key_here'
app.secret_key = os.environ['APP_SECRET_KEY']

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

    user_info = auth.authenticate()
    # print(user_info['attributes']['givenname'][0])
    username = user_info['user']
    given_name = user_info['attributes']['givenname'][0]

    html_code = flask.render_template('index.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        username = username,
        given_name = given_name
    )

    response = flask.make_response(html_code)
    return response



@app.route('/global', methods = ['GET'])
def global_page():
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
    
    user_info = auth.authenticate()
    username = user_info['user']
    given_name = user_info['attributes']['givenname'][0]
    
    html_code = flask.render_template('global.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        err_msg = err_msg,
        events = events,
        prev_cat = prev_cat,
        username = username,
        given_name = given_name
    )

    response = flask.make_response(html_code)

    response.set_cookie('prev_title', title)
    response.set_cookie('prev_cat', cat)
    response.set_cookie('prev_loc', loc)
    response.set_cookie('prev_descrip', descrip)
    return response

#-----------------------------------------------------------------------

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if flask.request.method == 'POST':
#         username = flask.request.form['username']
#         password = flask.request.form['password']
#         email = flask.request.form['email']
#         # Hash the password before storing (use werkzeug.security.generate_password_hash)
#         password_hash = generate_password_hash(password)
#         # Create the user and commit to the database
#         with sqlalchemy.orm.Session(database._engine) as session_db:
#             new_user = User(username=username, password_hash=password_hash, email=email)
#             session_db.add(new_user)
#             session_db.commit()
#         return flask.redirect('/login')
#     response = flask.render_template('signup.html',
#                                      ampm=get_ampm(),
#                     current_time=get_current_time(),)
#     return response




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
        )

    except Exception as ex:
        error_msg = str(ex)
        html_code = flask.render_template(
            'errmsg.html',
            error_msg = error_msg)
        response = flask.make_response(html_code)

    response = flask.make_response(html_code)

    return response
