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
    ___tablename__ = 'bucket_list'
    bucket_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    item = sqlalchemy.Column(sqlalchemy.String)
    contact = sqlalchemy.Column(sqlalchemy.String)
    area = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    cloudinary_id = sqlalchemy.Column(sqlalchemy.String)

_engine = sqlalchemy.create_engine(_DATABASE_URL)

#-----------------------------------------------------------------------

def get_events(category):

    books = []

    with sqlalchemy.orm.Session(_engine) as session:

        query = session.query(Bucket).filter(
            Bucket.category.ilike(category+'%'))
        table = query.all()
        for row in table:
            event = {'isbn': row.isbn, 'author': row.author,
                'title': row.title}
            books.append(book)
    return books
#-----------------------------------------------------------------------
# For testing:

def _test():
    books = get_books('ker')
    for book in books:
        print(book['isbn'])
        print(book['author'])
        print(book['title'])
        print()

if __name__ == '__main__':
    _test()
