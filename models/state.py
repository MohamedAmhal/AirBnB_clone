#!/usr/bin/python3
"""The State class to represent new State
"""
from models.base_model import BaseModel


class State(BaseModel):
    """"Represents a new state
    
    Attributes:
        name : The name of state. (type str)
    """
    name = ""
