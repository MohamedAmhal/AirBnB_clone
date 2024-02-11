#!/usr/bin/python3
"""This is User class to represent new users
"""
from models.base_model import BaseModel


class User(BaseModel):
    """"Handles the user informations:
    
    email, password, first_name, last_name (type str)
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
