#!/usr/bin/python3
"""
convert the dictionary representation to a JSON string.
JSON is a standard representation of a data structure. With this format, 
humans can read and all programming languages have a JSON reader and writer.
"""
import json

class FileStorage():
    """
    the class that all files will ,be stored in a json file
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        return the dictionary object
        """

        return FileStorage.__objects
    
    def new(self, obj):
        """
        change the object to obj
        """

        a = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(a, obj.id)] = obj
    
    def save(self):
        """
        saving the obj in yhe path file json
        """

        s = FileStorage.__objects
        obd = {}
        for i in  s.keys():
            obd[i] = s.to_dict()
        
        with open(FileStorage.__file_path, "w") as d:
            json.dump(obd, d)
    

    def reload(self):
        """
        doing the deserializes the json file
        """

        try:
            with open(FileStorage.__file_path) as d:
                a = json.load(d)
                for i in a.values():
                    cls_name = i["__class__"]
                    del i["__calss__"]
                    self.new(eval(cls_name)(**i))
            
        except FileNotFoundError:
            return


            





