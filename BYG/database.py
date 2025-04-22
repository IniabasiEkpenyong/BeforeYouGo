#!/usr/bin/env python
#-----------------------------------------------------------------------
# database.py
# Author: Bob Dondero
#-----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
import dotenv
from pathlib import Path
# import queue

#-----------------------------------------------------------------------
# Load .env file from the same directory as this file
env_path = Path(__file__).resolve().parent / '.env'
dotenv.load_dotenv(env_path)

_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

# _connection_pool = queue.Queue()

#-----------------------------------------------------------------------

Base = sqlalchemy.orm.declarative_base()

class Bucket (Base):
    __tablename__ = 'bucket_list'
    bucket_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    item = sqlalchemy.Column(sqlalchemy.String)
    contact = sqlalchemy.Column(sqlalchemy.String)
    area = sqlalchemy.Column(sqlalchemy.String)
    lat = sqlalchemy.Column(sqlalchemy.Float)
    lng = sqlalchemy.Column(sqlalchemy.Float)
    descrip = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    cloudinary_id = sqlalchemy.Column(sqlalchemy.String)
    priv = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

_engine = sqlalchemy.create_engine(_DATABASE_URL)


class UserBucket(Base):
    __tablename__ = 'user_bucket'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_netid = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    bucket_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                  sqlalchemy.ForeignKey('bucket_list.bucket_id'))
    completed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

class SubTask(Base):
    __tablename__ = 'subtasks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_bucket_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                       sqlalchemy.ForeignKey('user_bucket.id', ondelete='CASCADE'),
                                       nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    completed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, 
                                   server_default=sqlalchemy.sql.func.now())
    
    user_bucket = sqlalchemy.orm.relationship("UserBucket", 
                                             back_populates="subtasks")

UserBucket.subtasks = sqlalchemy.orm.relationship("SubTask", 
                                                 back_populates="user_bucket",
                                                 cascade="all, delete-orphan")

class SharedEvent(Base):
    __tablename__ = 'shared_events'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    bucket_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('bucket_list.bucket_id'), nullable=False)
    created_by = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_completed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    bucket = sqlalchemy.orm.relationship("Bucket")
    participants = sqlalchemy.orm.relationship("SharedParticipant", back_populates="shared_event", cascade="all, delete-orphan")

class SharedParticipant(Base):
    __tablename__ = 'shared_participants'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    shared_event_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('shared_events.id', ondelete='CASCADE'), nullable=False)
    user_netid = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    shared_event = sqlalchemy.orm.relationship("SharedEvent", back_populates="participants")


#-----------------------------------------------------------------------

def get_events(title='', cat='', loc='', lat=None, lng=None, descrip='', sort='', exclude_ids=None):
    if exclude_ids is None:
        exclude_ids = []

    events = []
    with sqlalchemy.orm.Session(_engine) as session:
        print("==== LOCATION FILTER DEBUG ====")
        print("Raw lat:", lat, "type:", type(lat))
        print("Raw lng:", lng, "type:", type(lng))

        query = session.query(Bucket).filter(
            ~Bucket.bucket_id.in_(exclude_ids),
            sqlalchemy.or_(
            Bucket.descrip.ilike('%' + descrip + '%'),
            Bucket.item.ilike('%' + title + '%')
            ))

        if loc:
            query = query.filter(Bucket.area.ilike('%' + loc + '%'))

        if lat and lng:
            try:
                # lat = float(lat)
                # lng = float(lng)

                lat = float(str(lat).replace('−', '-'))
                lng = float(str(lng).replace('−', '-'))
                print("Converted lat:", lat)
                print("Converted lng:", lng)

                # Match locations within ~0.01 degrees (~1.1 km); make smaller soon
                query = query.filter(
                    sqlalchemy.and_(
                        Bucket.lat >= lat - 0.01,
                        Bucket.lat <= lat + 0.01,
                        Bucket.lng >= lng - 0.01,
                        Bucket.lng <= lng + 0.01
                    )
                )
            except ValueError as e:
                print("ERROR parsing lat/lng:", e)
                pass  # Skip filtering if lat/lng not valid floats

        if cat:
            query = query.filter(Bucket.category.ilike('%' + cat + '%'))

        if sort == 'alphabetical':
            query = query.order_by(Bucket.item)
        elif sort == 'recent':
            query = query.order_by(Bucket.bucket_id.desc())

        table = query.all()
        for row in table:
            event = {'bucket_id': row.bucket_id, 'title': row.item,
                'contact': row.contact, 'loc': row.area,
                'descrip': row.descrip, 'cat': row.category,
                'cloudinary_id': row.cloudinary_id, 'priv': row.priv}
            events.append(event)
    return '', events

def get_all_categories():
    with sqlalchemy.orm.Session(_engine) as session:
        categories = session.query(Bucket.category).filter(Bucket.priv == False).distinct().all()
    
        # Filter out categories that are private
        return sorted(set(category for category, in categories if category))
    
def get_subtasks(user_bucket_id):
    with sqlalchemy.orm.Session(_engine) as session:
        subtasks = session.query(SubTask).filter(SubTask.user_bucket_id == user_bucket_id).all()
        return subtasks

def add_subtask(user_bucket_id, description):
    with sqlalchemy.orm.Session(_engine) as session:
        user_bucket = session.query(UserBucket).filter_by(id=user_bucket_id).first()
        if not user_bucket:
            return False, "User bucket not found"
        
        new_subtask = SubTask(
            user_bucket_id=user_bucket_id,
            description=description,
            completed=False
        )
        session.add(new_subtask)
        session.commit()
        return True, new_subtask.id

def toggle_subtask(subtask_id):
    with sqlalchemy.orm.Session(_engine) as session:
        subtask = session.query(SubTask).filter(SubTask.id == subtask_id).first()
        if not subtask:
            return False, "Subtask not found"
        
        subtask.completed = not subtask.completed
        
        user_bucket = session.query(UserBucket).filter_by(id=subtask.user_bucket_id).first()
        if user_bucket:
            subtasks = session.query(SubTask).filter_by(user_bucket_id=user_bucket.id).all()
            if subtasks and all(st.completed for st in subtasks):
                user_bucket.completed = True
            else:
                user_bucket.completed = False
        
        session.commit()
        return True, subtask.completed

def delete_subtask(subtask_id):
    with sqlalchemy.orm.Session(_engine) as session:
        subtask = session.query(SubTask).filter_by(id=subtask_id).first()
        if not subtask:
            return False, "Subtask not found"
        
        user_bucket_id = subtask.user_bucket_id
        
        session.delete(subtask)
        
        user_bucket = session.query(UserBucket).filter_by(id=user_bucket_id).first()
        if user_bucket:
            remaining_subtasks = session.query(SubTask).filter_by(user_bucket_id=user_bucket_id).all()
            if remaining_subtasks and all(st.completed for st in remaining_subtasks):
                user_bucket.completed = True
            else:
                user_bucket.completed = False
        
        session.commit()
        return True, "Subtask deleted successfully"
    
def create_shared_event(bucket_id, creator_netid, participant_netids, date=None):
    with sqlalchemy.orm.Session(_engine) as session:
        event = SharedEvent(bucket_id=bucket_id, created_by=creator_netid, date=date)
        session.add(event)
        session.flush()  # get event.id before commit

        for netid in set(participant_netids + [creator_netid]):
            participant = SharedParticipant(shared_event_id=event.id, user_netid=netid)
            session.add(participant)

        session.commit()
        return True, event.id

def get_shared_events_for_user(user_netid):
    with sqlalchemy.orm.Session(_engine) as session:
        shared_items = session.query(SharedEvent).join(SharedParticipant).filter(
            SharedParticipant.user_netid == user_netid
        ).all()
        return shared_items

def mark_shared_event_completed(shared_event_id):
    with sqlalchemy.orm.Session(_engine) as session:
        event = session.query(SharedEvent).filter_by(id=shared_event_id).first()
        if event:
            event.is_completed = True
            session.commit()
            return True
        return False

    
#-----------------------------------------------------------------------
# For testing:

def _test():
    events = get_events()[1]
    for event in events:
        print(event['bucket_id'])
        print(event['title'])
        print(event['contact'])
        print(event['loc'])
        print(event['descrip'])
        print(event['cat'])
        print(event['cloudinary_id'])
        print(event['priv'])

if __name__ == '__main__':
    _test()
