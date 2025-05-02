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
    from .database import Bucket, UserBucket, create_shared_event
    from . import database
except ImportError:
    from BYG import app
    from BYG.database import Bucket, UserBucket, create_shared_event
    import BYG.database as database

from .database import get_shared_events_for_user
from .database import mark_shared_event_completed

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
admins = ['jg2783', 'ie9117', 'cs-jiaweim']

def get_ampm():
    if time.strftime('%p') == 'AM':
        return 'morning'
    return 'afternoon'

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------

@app.route("/debug_locations")
def debug_locations():
    with sqlalchemy.orm.Session(database._engine) as session_db:
        entries = session_db.query(database.Bucket).all()

        rows = []
        for e in entries:
            rows.append(f"{e.bucket_id}: {e.item} @ ({e.lat}, {e.lng})")

    return "<br>".join(rows)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def start_page():

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

@app.route('/home', methods=['GET'])
def home_page():
    user_info = auth.authenticate()
    given_name = auth.get_name(user_info)
    is_admin = user_info['user'] in admins

    pending_count = 0
    if is_admin:
        with sqlalchemy.orm.Session(database._engine) as session_db:
            pending_count = session_db.query(Bucket).filter_by(status='pending').count()

    html_code = flask.render_template('home.html',
        ampm=get_ampm(),
        given_name = given_name,
        is_admin=is_admin,
        pending_count = pending_count
    )

    response = flask.make_response(html_code)
    return response


@app.route('/global', methods = ['GET'])
def global_page():

    search = flask.request.args.get('search', '')
    if search is None:
        title = ''
        descrip = ''
    else:
        title = search
        descrip = search

    prev_title = flask.request.cookies.get('prev_title')
    if prev_title is None:
        prev_title= ''

#    title = flask.request.args.get('title')
#    if title is None:
#        title = ''

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

#    descrip = flask.request.args.get('descrip')
#    if descrip is None:
#        descrip = ''

    lat = flask.request.args.get('lat')
    lng = flask.request.args.get('lng')

    try:
        lat = float(str(lat).replace('−', '-')) if lat else None
        lng = float(str(lng).replace('−', '-')) if lng else None
    except ValueError:
        lat = None
        lng = None

    sort = flask.request.args.get('sort', '')

    user_info = auth.authenticate()
    user_netid = user_info['user']

    with sqlalchemy.orm.Session(database._engine) as session_db:
        user_bucket_ids = session_db.query(UserBucket.bucket_id).filter_by(user_netid=user_netid).all()
        user_bucket_ids = [id for (id,) in user_bucket_ids]

    err_msg, events = database.get_events(
        title=title, cat=cat,
        loc=loc, descrip=descrip, sort=sort,
        exclude_ids=user_bucket_ids,
        lat=lat, lng =lng, status='approved')
    
    user_info = auth.authenticate()
    username = user_info['user']
    given_name = auth.get_name(user_info)
    is_admin = username in admins

    pending_count = 0
    if is_admin:
        with sqlalchemy.orm.Session(database._engine) as session_db:
            pending_count = session_db.query(Bucket).filter_by(status='pending').count()

    #TEMP hard coding until OIT whitelists
    # username = 'jg2783'
    # given_name = 'Judah'
    print(database.get_all_categories())
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
        is_admin = is_admin,
        pending_count = pending_count,
        api_key=os.getenv("GOOGLE_API_KEY")
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

    search = flask.request.form.get('search', '')
    sort = flask.request.form.get('sort', '')
    cat = flask.request.form.get('cat', '')

    response = flask.redirect('/my_bucket')
    response.set_cookie('search', search)
    response.set_cookie('sort', sort)
    response.set_cookie('cat', cat)
    return response

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
            bucket_id = ub_item.bucket_id
            session_db.delete(ub_item)
            session_db.commit()

            # Check if the item is public before deleting from the global list
            item = session_db.query(Bucket).filter_by(
                bucket_id=bucket_id).first()
            if item and not item.priv:
                # Do not delete from the global list if the item is public
                pass
            else:
                session_db.delete(item)
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

    search = flask.request.form.get('search', '')
    sort = flask.request.form.get('sort', '')
    cat = flask.request.form.get('cat', '')

    return flask.redirect(f'/global?search={search}&sort={sort}&cat={cat}')


@app.route('/my_bucket', methods=['GET'])
def my_bucket():
    user_info = auth.authenticate()
    user_netid = user_info['user']
    given_name = auth.get_name(user_info)

    is_admin = user_netid in admins
    
    pending_count = 0
    if is_admin:
        with sqlalchemy.orm.Session(database._engine) as session_db:
            pending_count = session_db.query(Bucket).filter_by(status='pending').count()

    #TEMP hard coding until OIT whitelists
    # user_netid = 'jg2783'
    # given_name = 'Judah'    

    with sqlalchemy.orm.Session(database._engine) as session_db:
        user_items = session_db.query(UserBucket, database.Bucket) \
            .join(database.Bucket, UserBucket.bucket_id == database.Bucket.bucket_id) \
            .filter(UserBucket.user_netid == user_netid).all()

        # Get subtasks for each user bucket and calculate progress
        subtasks_by_bucket = {}
        progress_by_bucket = {}
        
        for ub, _ in user_items:
            subtasks = session_db.query(database.SubTask).filter_by(
                user_bucket_id=ub.id).all()
            subtasks_by_bucket[ub.id] = subtasks
            
            total = len(subtasks)
            if total > 0:
                completed = sum(1 for st in subtasks if st.completed)
                progress_by_bucket[ub.id] = int((completed / total) * 100)
            else:
                progress_by_bucket[ub.id] = 100 if ub.completed else 0

    total_items = len(user_items)
    completed = sum(1 for item in user_items if item[0].completed)
    progress = 0 if total_items == 0 else (completed/total_items)* 100
    
    # user_items is a list of tuples: (UserBucket, Bucket)
    # Build the pins array for the map
    pins = [
        {
            'title': bucket.item,
            'lat': bucket.lat,
            'lng': bucket.lng,
            'completed': ub.completed,
            'description': bucket.descrip
        }
        for ub, bucket in user_items if bucket.lat and bucket.lng
    ]
    
    shared_events = get_shared_events_for_user(user_netid)
    
    # Pass it to a template
    return flask.render_template('my_bucket.html',
        given_name = given_name,
        user_netid=user_netid,
        user_items=user_items,
        ampm=get_ampm(),
        current_time=get_current_time(),
        progress=progress,
        pins=pins,
        subtasks_by_bucket = subtasks_by_bucket,
        progress_by_bucket = progress_by_bucket,
        shared_events=shared_events,
        pending_count=pending_count,
        is_admin=is_admin,
        api_key=os.getenv("GOOGLE_API_KEY")
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



# @app.route("/create_shared_event", methods=["POST"])
# def create_shared_event_route():
#     bucket_id = flask.request.form["bucket_id"]
#     netids = flask.request.form.getlist("friend_netids[]")
#     netids = [n.strip().lower() for n in netids if n.strip()]
#     
#     user_info = auth.authenticate()
#     user_netid = user_info['user']
# 
#     # if not user_netid:
#     #     return flask.redirect("/")
#     if not user_netid or not bucket_id or not netids:
#         return flask.redirect("/global")
# 
#     success, shared_event_id = database.create_shared_event(
#         bucket_id=int(bucket_id),
#         creator_netid=user_netid,
#         participant_netids=netids
#     )
# 
#     if success:
#         flask.flash("Shared event created!")
#     else:
#         flask.flash("Something went wrong.")
#     
#     return flask.redirect("/global")

@app.route("/create_shared_event", methods=["POST"])
def create_shared_event_route():
    try:
        bucket_id = int(flask.request.form["bucket_id"])
        netids = flask.request.form.getlist("friend_netids[]")
        netids = [n.strip().lower() for n in netids if n.strip()]
    except Exception as e:
        print("Error parsing form:", e)
        flask.flash("Invalid form submission.")
        return flask.redirect("/global")

    user_info = auth.authenticate()
    user_netid = user_info.get('user')

    if not user_netid or not bucket_id or not netids:
        flask.flash("Missing information for shared event.")
        return flask.redirect("/global")

    success, shared_event_id = database.create_shared_event(
        bucket_id=bucket_id,
        creator_netid=user_netid,
        participant_netids=netids
    )

    if success:
        flask.flash("Shared event created!")
    else:
        flask.flash("Something went wrong.")
    
    return flask.redirect("/global")





@app.route("/complete_shared_event", methods=["POST"])
def complete_shared_event():
    shared_event_id = flask.request.form["shared_event_id"]
    mark_shared_event_completed(shared_event_id)
    return flask.redirect("/my_bucket")

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

@app.route("/map")
def map_page():
    return render_template("map.html", api_key=os.getenv("GOOGLE_API_KEY"))


@app.route('/show_item', methods=['POST'])
def show_item():

    user_info = auth.authenticate()    
    username = user_info['user']    
    given_name = auth.get_name(user_info)
    
    priv = request.form.get('priv')
    return flask.render_template('add_item.html', 
                ampm=get_ampm(),
                current_time=get_current_time(),
                username = username,
                given_name = given_name,
                priv=priv,
                api_key=os.getenv("GOOGLE_API_KEY")
                )

@app.route('/create_item', methods=['POST'])
def add__item():
    # Get form data
    title = request.form.get('title')
    contact = request.form.get('contact')
    
    area = request.form.get('area')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    
    descrip = request.form.get('descrip')
    category = request.form.get('category')
    priv = eval(request.form.get('priv'))

    # Get user info
    user_info = auth.authenticate()
    user_netid = user_info['user']

    # Set initial status
    # If user is admin, auto-approve. Otherwise, set as pending
    initial_status = 'approved' if user_netid in admins else 'pending'

    # Add the new item to the database
    with sqlalchemy.orm.Session(database._engine) as session_db:
        new_item = Bucket(
            item=title,
            contact=contact,
            area=area,
            lat=lat,
            lng=lng,
            descrip=descrip,
            category=category,
            cloudinary_id='XXX',
            priv=priv,
            status=initial_status,
            created_by=user_netid
        )
        session_db.add(new_item)
        session_db.commit()
        
        if priv == True:
            new_user_bucket = UserBucket(user_netid=user_netid, bucket_id=new_item.bucket_id)
            session_db.add(new_user_bucket)
            session_db.commit()
   
    # Redirect back to the global list
    if priv == True:
        return flask.redirect('/my_bucket')
    else:
        if initial_status == 'pending':
            flask.flash("Your item has been submitted for approval!")
        return flask.redirect('/global')
    
# Add these routes after your existing routes

@app.route('/add_subtask', methods=['POST'])
def add_subtask():
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    user_bucket_id = int(request.form.get('user_bucket_id'))
    description = request.form.get('subtask')
    
    if not user_bucket_id or not description:
        return flask.redirect('/my_bucket')
    
    with sqlalchemy.orm.Session(database._engine) as session_db:
        ub_item = session_db.query(UserBucket).filter_by(
            id=user_bucket_id, user_netid=user_netid).first()
        
        if ub_item:
            success, result = database.add_subtask(user_bucket_id, description)
    
    return flask.redirect('/my_bucket')

@app.route('/toggle_subtask', methods=['POST'])
def toggle_subtask():
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    subtask_id = request.form.get('subtask_id')
    if not subtask_id:
        return flask.redirect('/my_bucket')
    
    with sqlalchemy.orm.Session(database._engine) as session_db:
        subtask = session_db.query(database.SubTask).join(UserBucket).filter(
            database.SubTask.id == subtask_id,
            UserBucket.user_netid == user_netid
        ).first()
        
        if subtask:
            database.toggle_subtask(subtask_id)
    
    return flask.redirect('/my_bucket')

@app.route('/delete_subtask', methods=['POST'])
def delete_subtask():
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    subtask_id = request.form.get('subtask_id')
    if not subtask_id:
        return flask.redirect('/my_bucket')
    
    with sqlalchemy.orm.Session(database._engine) as session_db:
        subtask = session_db.query(database.SubTask).join(UserBucket).filter(
            database.SubTask.id == subtask_id,
            UserBucket.user_netid == user_netid
        ).first()
        
        if subtask:
            database.delete_subtask(subtask_id)
    
    return flask.redirect('/my_bucket')

@app.route('/admin', methods=['GET'])
def admin_dashboard():
    # Verify the user is an admin
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    if user_netid not in admins:
        flask.flash("You don't have permission to access the admin dashboard")
        return flask.redirect('/')
    
    # Get filter status
    status = flask.request.args.get('status', 'pending')
    
    with sqlalchemy.orm.Session(database._engine) as session_db:
        # Count items by status
        counts = {
            'pending': session_db.query(Bucket).filter_by(status='pending').count(),
            'approved': session_db.query(Bucket).filter_by(status='approved').count(),
            'rejected': session_db.query(Bucket).filter_by(status='rejected').count(),
            'all': session_db.query(Bucket).count()
        }
        
        # Get items based on filter
        if status == 'all':
            items = session_db.query(Bucket).order_by(Bucket.created_at.desc()).all()
        else:
            items = session_db.query(Bucket).filter_by(status=status).order_by(Bucket.created_at.desc()).all()
    
    return flask.render_template('admin.html', 
                               items=items, 
                               status=status, 
                               counts=counts,
                               ampm=get_ampm(),
                               current_time=get_current_time())

@app.route('/admin/approve', methods=['POST'])
def admin_approve():
    # Verify the user is an admin
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    if user_netid not in admins:
        flask.flash("You don't have permission to perform this action")
        return flask.redirect('/')
    
    bucket_id = flask.request.form.get('bucket_id')
    
    with sqlalchemy.orm.Session(database._engine) as session_db:
        item = session_db.query(Bucket).filter_by(bucket_id=bucket_id).first()
        if item:
            item.status = 'approved'
            session_db.commit()
    
    return flask.redirect('/admin?status=pending')

@app.route('/admin/reject', methods=['POST'])
def admin_reject():
    # Verify the user is an admin
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    if user_netid not in admins:
        flask.flash("You don't have permission to perform this action")
        return flask.redirect('/')
    
    bucket_id = flask.request.form.get('bucket_id')
    
    with sqlalchemy.orm.Session(database._engine) as session_db:
        item = session_db.query(Bucket).filter_by(bucket_id=bucket_id).first()
        if item:
            item.status = 'rejected'
            session_db.commit()
    
    return flask.redirect('/admin?status=pending')

@app.route('/add_comment', methods=['POST'])
def add_comment_route():
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    event_id = request.form.get('event_id')
    comment_text = request.form.get('comment')
    
    if not event_id or not comment_text:
        return flask.jsonify({'success': False, 'message': 'Missing data'})
    
    # Add comment to database
    comment = database.add_comment(event_id, user_netid, comment_text)
    if comment:
        return flask.jsonify({
            'success': True,
            'comment': {
                'id': comment.id,
                'text': comment.text,
                'user': user_netid,
                'date': comment.created_at.strftime('%Y-%m-%d %H:%M')
            }
        })
    else:
        return flask.jsonify({'success': False, 'message': 'Failed to add comment'})

@app.route('/get_comments/<int:event_id>', methods=['GET'])
def get_comments_route(event_id):
    comments = database.get_comments(event_id)
    return flask.jsonify({'comments': comments})

@app.route('/add_rating', methods=['POST'])
def add_rating_route():
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    event_id = request.form.get('event_id')
    rating = request.form.get('rating')
    
    if not event_id or not rating:
        return flask.jsonify({'success': False, 'message': 'Missing data'})
    
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
    except ValueError:
        return flask.jsonify({'success': False, 'message': 'Invalid rating'})
    
    result = database.add_or_update_rating(event_id, user_netid, rating)
    return flask.jsonify(result)

@app.route('/get_rating/<int:event_id>', methods=['GET'])
def get_rating_route(event_id):
    user_info = auth.authenticate()
    user_netid = user_info['user']
    
    rating_info = database.get_rating_info(event_id, user_netid)
    return flask.jsonify(rating_info)

@app.route('/logoutapp')
def logout_app():
    # Clear the session data
    session.clear()
    
    # Redirect to the home page or login page
    return flask.render_template('loggedout.html')

@app.route('/logoutcas')
def logout_cas():
    # Clear the session data
    session.clear()
    
    # Additional logic to end the CAS session
    # This might involve redirecting to a CAS logout URL
    
    # Redirect to the home page or login page
    return flask.render_template('loggedout.html')


if __name__ == "__main__":
    from database import Base, _engine
    Base.metadata.create_all(_engine)
