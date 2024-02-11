#!/usr/bin/python3
"""This is Amenity class to represent Amenity
"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represent an amenity.

    Attributes:
        name (str): The name of the amenity.
    """
    name = ""
