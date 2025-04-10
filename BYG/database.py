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
#-----------------------------------------------------------------------

def get_events(title='', cat='', loc = '', descrip = ''):

    events = []
    with sqlalchemy.orm.Session(_engine) as session:

        query = session.query(Bucket).filter(
            Bucket.category.ilike('%'+ cat+'%')).filter(
                Bucket.descrip.ilike('%'+ descrip +'%')).filter(
                    Bucket.area.ilike('%'+ loc +'%')).filter(
                        Bucket.item.ilike('%'+ title +'%')
                        ).order_by(Bucket.category, Bucket.item)
        
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
