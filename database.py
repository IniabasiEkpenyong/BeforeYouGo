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
            event = {'id': row.bucket_id, 'item': row.item,
                'contact': row.contact, 'area': row.area,
                'description': row.descrip, 'category': row.category,
                'cloudinary_id': row.cloudinary_id}
            events.append(event)
    return events
#-----------------------------------------------------------------------
# For testing:

def _test():
    events = get_events('athletic')
    for event in events:
        print(event['id'])
        print(event['item'])
        print(event['contact'])
        print(event['area'])
        print(event['description'])
        print(event['category'])
        print(event['cloudinary_id'])
        print()

if __name__ == '__main__':
    _test()
