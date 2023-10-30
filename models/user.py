#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes a user instance"""
        if kwargs:
            # Get the 'password' attribute from keyword arguments
            password_dt = kwarg.pop("password", None)
            if password_dt:
                # Hash the password using MD5 and update the password attribute
                password_md5 = hashlib.md5(password_dt.encode()).hexdigest()
                setattr(self, "password", password_md5)
        super().__init__(*args, **kwargs)
