#!/usr/bin/python3
""" File storage model """
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    FileStorage class for storing, serializing and deserializing data
    """

    __file_path = "file.json"
    __objects = {}

    def new(self, obj):
        """ This method adds a new object to the __objects dictionary.
        """
        obj_class_name = obj.__class__.__name__

        key = "{}.{}".format(obj_class_name, obj.id)

        FileStorage.__objects[key] = obj

    def all(self):
        """  Returns the __objects dictionary. 
        It provides access to all the stored objects.
        """
        return FileStorage.__objects

    def save(self):
        """ This method writes the current data in the __objects
        dictionary to the JSON file.
        """
        data = {}
        for key, obj in FileStorage.__objects.items():
            data[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w") as file:
            json.dump(data, file, indent=4)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path, "r") as f:
                data = json.load(f)
            for key, value in data.items():
                if "BaseModel" in key:
                    reloaded = BaseModel(**value)
                    self.new(reloaded)
                if "User" in key:
                    reloaded = User(**value)
                    self.new(reloaded)
                if "State" in key:
                    reloaded = State(**value)
                    self.new(reloaded)
                if "City" in key:
                    reloaded = City(**value)
                    self.new(reloaded)
                if "Amenity" in key:
                    reloaded = Amenity(**value)
                    self.new(reloaded)
                if "Place" in key:
                    reloaded = Place(**value)
                    self.new(reloaded)
                if "Review" in key:
                    reloaded = Review(**value)
                    self.new(reloaded)
        except Exception:
            pass
