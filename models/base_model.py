#!/usr/bin/python3

import uuid
from datetime import datetime
import models

"""
this is the model base class we will define the methods 
and attributtes!
"""

class BaseModel():
    """
    the base class of all the program!
    attributs : id , creat_at, update_at
    """
    def __init__(self, *args, **kwargs):
        """
        the instances attributtes
        id : it must be a unique id
        created_at : the time attributte
        updated_at : the time updating the variable updated_at
        *args : infinity list handling
        *kwargs : infinity dictionary handlling
        """
        if kwargs:
            for key,value in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, value)
                else:
                    self.id = str(uuid.uuid4())
                    self.created_at = datetime.now()
                    self.updated_at = datetime.now()
        
        else:
            models.storage.new(self)

    def __str__(self) -> str:
        """
        the magic method __str__
        """
        class_name = self.__class__.__name__
        print("[<{}>] (<{}>) <{}>".format(class_name, self.id, self.__dict__))
    
    def save(self) :
        """
        updating the time of the variable updated_at
        """

        self.updated_at = datetime.now()
        models.storage.save()
    
    def to_dict(self):
        """
        creating the file json that contient the attributes (class or instancces)
        """
        class_name = self.__class__.__name__
        attributtes = self.__dict__.copy()
        attributtes['__class__'] = class_name
        attributtes['created_at'] = self.created_at.isoformat()
        attributtes['updated_at'] = self.updated_at.isoformat()

        return attributtes
    

    
    
