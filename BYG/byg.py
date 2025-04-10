#!/usr/bin/env python

#-----------------------------------------------------------------------
# byg.py
# Author: Judah Guggenheim
#-----------------------------------------------------------------------

import time
import flask
import sqlalchemy
import sqlalchemy.orm
import os
from flask import session, redirect, render_template, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash

# Import the app from package
try:
    from . import app
    from .database import Bucket, UserBucket
    from . import database
except ImportError:
    from BYG import app
    from BYG.database import Bucket, UserBucket
    import BYG.database as database

# Set the secret key
app.secret_key = os.environ['APP_SECRET_KEY']

# from models import User, UserBucket
# import sys

# Handle local vs package-relative imports
try:
    from . import database
    from . import auth
    from .database import Bucket, UserBucket
except ImportError:
    import database
    import auth

# app.secret_key = 'app-secret-key'  # Or from env


#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')
#from top import app 


# app.secret_key = 'secret_key_here'
app.secret_key = os.environ['APP_SECRET_KEY']

#-----------------------------------------------------------------------
admins = ['jg2783', 'ie9117']

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
    username = user_info['user']    
    given_name = auth.get_name(user_info)

    #TEMP hard coding until OIT whitelists
    # username = 'jg2783'
    # given_name = 'Judah'

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
    given_name = auth.get_name(user_info)
    is_admin = username in admins

    #TEMP hard coding until OIT whitelists
    # username = 'jg2783'
    # given_name = 'Judah'
    try:
        categories = database.get_all_categories()
    except:
        categories = []

    html_code = flask.render_template('global.html',
        ampm=get_ampm(),
        current_time=get_current_time(),
        err_msg = err_msg,
        events = events,
        prev_cat = prev_cat,
        username = username,
        given_name = given_name,
        categories=categories,
        is_admin = is_admin
    )

    response = flask.make_response(html_code)

    response.set_cookie('prev_title', title)
    response.set_cookie('prev_cat', cat)
    response.set_cookie('prev_loc', loc)
    response.set_cookie('prev_descrip', descrip)
    return response


@app.route('/add_to_my_list', methods=['POST'])
def add_to_my_list():
    # 1) Ensure the user is authenticated
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    #TEMP hard coding until OIT whitelists
    
    # user_netid = 'jg2783'
    # given_name = 'Judah'

    bucket_id = request.form.get('bucket_id')

    # If bucket_id is not provided, try to get it from the URL
    
    if bucket_id is None:
        return flask.redirect('/global')

    with sqlalchemy.orm.Session(database._engine) as session_db:
        # Optionally check if it's already added
        existing = session_db.query(UserBucket).filter_by(
            user_netid=user_netid, bucket_id=bucket_id).first()
        if existing is None:
            new_item = UserBucket(user_netid=user_netid, bucket_id=bucket_id)
            session_db.add(new_item)
            session_db.commit()

    return flask.redirect('/my_bucket')

@app.route('/remove_from_my_list', methods=['POST'])
def remove_from_my_list():
    # Ensure the user is authenticated
    user_info = auth.authenticate()
    user_netid = user_info['user']

    user_bucket_id = flask.request.form.get('user_bucket_id')
    if not user_bucket_id:
        return flask.redirect('/my_bucket')

    with sqlalchemy.orm.Session(database._engine) as session_db:
        # Ensure the item belongs to the user before deleting
        ub_item = session_db.query(UserBucket).filter_by(
            id=user_bucket_id, user_netid=user_netid).first()
        if ub_item:
            session_db.delete(ub_item)
            session_db.commit()

    return flask.redirect('/my_bucket')

@app.route('/remove_from_global_list', methods=['POST'])
def remove_from_global_list():
    # Ensure the user is authenticated
    user_info = auth.authenticate()
    user_netid = user_info['user']

    bucket_id = flask.request.form.get('bucket_id')
    if not bucket_id:
        return flask.redirect('/global')

    with sqlalchemy.orm.Session(database._engine) as session_db:
        # Removes the item from the user's bucket list
        ub_items = session_db.query(UserBucket).filter_by(
            bucket_id=bucket_id)
        if ub_items:
            for ub_item in ub_items:
                session_db.delete(ub_item)
                session_db.commit()

        # Removes the item from the global bucket list
        item = session_db.query(Bucket).filter_by(
            bucket_id=bucket_id).first()
        if item:
            session_db.delete(item)
            session_db.commit()

    return flask.redirect('/global')




@app.route('/my_bucket', methods=['GET'])
def my_bucket():
    user_info = auth.authenticate()
    user_netid = user_info['user']
    given_name = auth.get_name(user_info)

    #TEMP hard coding until OIT whitelists
    # user_netid = 'jg2783'
    # given_name = 'Judah'    

    # Query the user_bucket table, joined with the bucket_list table
    with sqlalchemy.orm.Session(database._engine) as session_db:
        user_items = session_db.query(UserBucket, database.Bucket) \
            .join(database.Bucket, UserBucket.bucket_id == database.Bucket.bucket_id) \
            .filter(UserBucket.user_netid == user_netid).all()

    # user_items is a list of tuples: (UserBucket, Bucket)
    # Pass it to a template
    return flask.render_template('my_bucket.html',
        given_name = given_name,
        user_netid=user_netid,
        user_items=user_items,
        ampm=get_ampm(),
        current_time=get_current_time()
    )

@app.route('/mark_completed', methods=['POST'])
def mark_completed():
    user_info = auth.authenticate()
    user_netid = user_info['user']

    #TEMP hard coding until OIT whitelists
    # user_netid = 'jg2783'
    # given_name = 'Judah'

    user_bucket_id = request.form.get('user_bucket_id')
    if not user_bucket_id:
        return flask.redirect('/my_bucket')

    with sqlalchemy.orm.Session(database._engine) as session_db:
        ub_item = session_db.query(UserBucket).filter_by(
            id=user_bucket_id, user_netid=user_netid).first()
        if ub_item:
            ub_item.completed = True
            session_db.commit()
    return flask.redirect('/my_bucket')

# Honestly could prob just use the same function as above,
# replace: ub_item.completed = True' 
# with:    ub_item.completed = !ub_item.completed' 
@app.route('/reset_completed', methods=['POST'])
def reset_completed():
    user_info = auth.authenticate()
    user_netid = user_info['user']

    user_bucket_id = request.form.get('user_bucket_id')
    if not user_bucket_id:
        return flask.redirect('/my_bucket')

    with sqlalchemy.orm.Session(database._engine) as session_db:
        ub_item = session_db.query(UserBucket).filter_by(
            id=user_bucket_id, user_netid=user_netid).first()
        if ub_item:
            ub_item.completed = False
            session_db.commit()
    return flask.redirect('/my_bucket')



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

@app.route('/show_item', methods=['POST'])
def show_item():
    priv = request.form.get('priv')
    return flask.render_template('add_item.html', priv=priv)

@app.route('/create_item', methods=['POST'])
def add__item():
    # Get form data
    title = request.form.get('title')
    contact = request.form.get('contact')
    area = request.form.get('area')
    descrip = request.form.get('descrip')
    category = request.form.get('category')
    priv = eval(request.form.get('priv'))
    # Validate that all required fields are present
    if not all([title, contact, area, descrip, category]):
        return flask.redirect(flask.url_for('/show_item', priv=priv))

    # Add the new item to the database
    with sqlalchemy.orm.Session(database._engine) as session_db:
        new_item = Bucket(
            item=title,
            contact=contact,
            area=area,
            descrip=descrip,
            category=category,
            cloudinary_id='XXX',
            priv=priv
        )
        session_db.add(new_item)
        session_db.commit()
        
        if priv == True:
            user_info = auth.authenticate()
            user_netid = user_info['user']
            new_item = UserBucket(user_netid=user_netid, bucket_id=new_item.bucket_id)
            session_db.add(new_item)
            session_db.commit()
   
    # Redirect back to the global list
    if priv == True:
        return flask.redirect('/my_bucket')
    else:
        return flask.redirect('/global')
