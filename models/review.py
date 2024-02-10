#!/usr/bin/python3
"""this defines deview class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represents a review.
    
    Attributes:
        place_id (str): the Place's id.
        user_id (str): the User's id.
        text (str): the text review.
    """
    place_id = ""
    user_id = ""
    text = ""
