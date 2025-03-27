 #!/usr/bin/env python
 #-----------------------------------------------------------------------
 # database.py
 # Author: Bob Dondero
 #-----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
import dotenv

#-----------------------------------------------------------------------
dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

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

_engine = sqlalchemy.create_engine(_DATABASE_URL)

#-----------------------------------------------------------------------

def get_events(category):

    events = []
    with sqlalchemy.orm.Session(_engine) as session:

        query = session.query(Bucket).filter(
            Bucket.category.ilike(category+'%'))
        table = query.all()
        for row in table:
            event = {'bucket_id': row.bucket_id, 'title': row.item,
                'contact': row.contact, 'loc': row.area,
                'descrip': row.descrip, 'cat': row.category,
                'cloudinary_id': row.cloudinary_id}
            events.append(event)
    return '', events
#-----------------------------------------------------------------------
# For testing:

def _test():
    events = get_events('athletic')[1]
    for event in events:
        print(event['bucket_id'])
        print(event['title'])
        print(event['contact'])
        print(event['loc'])
        print(event['descrip'])
        print(event['cat'])
        print(event['cloudinary_id'])
        print()

if __name__ == '__main__':
    _test()
