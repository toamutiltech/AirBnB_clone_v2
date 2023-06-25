#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel


class User(BaseModel):
    """This class defines a user by various attributes"""
    _tablename_
    email = ''
    password = ''
    first_name = ''
    last_name = ''
