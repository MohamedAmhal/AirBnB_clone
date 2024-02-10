#!/usr/bin/python3
""" BaseModel """
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """ BaseModel class """

    def __init__(self, *args, **kwargs):
        """ Constructor for the BaseModel class.
        Args:
            *args: Variable number of positional arguments.
            **kwargs: Keyword arguments.
        """
        if not kwargs:
            time_format = "%Y-%m-%dT%H:%M:%S.%f"
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        value = datetime.strptime(value, time_format)
                    setattr(self, key, value)

    def __str__(self):
        """ Returns a string containing the class name, the object's ID, and its
            attributes.
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """ Updates the updated_at attribute """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ Returns a dictionary representation of the object.
        """
        my_class_dict = self.__dict__.copy()
        my_class_dict["__class__"] = self.__class__.__name__
        my_class_dict["updated_at"] = self.updated_at.isoformat()
        my_class_dict["created_at"] = self.created_at.isoformat()
        return my_class_dict
