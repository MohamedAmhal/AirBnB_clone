#!/usr/bin/python3
"""This is City class to represent new City
"""
from models.base_model import BaseModel


class City(BaseModel):
    """"Represents a city
    
    Attributes:
    state_id, name (type str)
    """
    state_id = ""
    name = ""
