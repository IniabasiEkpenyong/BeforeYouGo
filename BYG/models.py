 #!/usr/bin/env python
 #-----------------------------------------------------------------------
 # models.py
 # Author: Judah Guggenheim
 # NOTE that this particular file was made with the help of chatgpt
 # Also as of now, it's not being used
 #-----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
import dotenv
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password_hash = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String)


class UserBucket(Base):
    __tablename__ = 'user_bucket'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    bucket_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('bucket_list.bucket_id'))
    completed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)