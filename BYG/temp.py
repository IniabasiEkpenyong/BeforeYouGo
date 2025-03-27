import sqlalchemy
import sqlalchemy.orm
from database import _engine

with sqlalchemy.orm.Session(_engine) as session:
    session.execute("""
        CREATE TABLE user_bucket (
            id SERIAL PRIMARY KEY,
            user_netid VARCHAR NOT NULL,
            bucket_id INTEGER REFERENCES bucket_list(bucket_id),
            completed BOOLEAN DEFAULT FALSE
        );
    """)
    session.commit()