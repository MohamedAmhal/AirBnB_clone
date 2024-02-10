#!/usr/bin/python3
""" unit test for bases """
import json
import unittest
from models.base_model import BaseModel
from datetime import datetime
import models
from io import StringIO
import sys
from unittest.mock import patch
captured_output = StringIO()
sys.stdout = captured_output


class BaseModelTestCase(unittest.TestCase):
    """ class for base test """

    def setUp(self):
        """ class for base test """
        self.filepath = models.storage._FileStorage__file_path
        with open(self.filepath, 'w') as file:
            file.truncate(0)
        models.storage.all().clear()

    def tearDown(self):
        """ class for base test """
        printed_output = captured_output.getvalue()
        sys.stdout = sys.__stdout__

    def test_basemodel_init(self):
        """ class for base test """
        new = BaseModel()

        """ check if it have methods """
        self.assertTrue(hasattr(new, "__init__"))
        self.assertTrue(hasattr(new, "__str__"))
        self.assertTrue(hasattr(new, "save"))
        self.assertTrue(hasattr(new, "to_dict"))

        """existince"""
        self.assertTrue(hasattr(new, "id"))
        self.assertTrue(hasattr(new, "created_at"))
        self.assertTrue(hasattr(new, "updated_at"))

        """type test"""
        self.assertIsInstance(new.id, str)

        """ check if save in storage """
        keyname = "BaseModel."+new.id
        """ check if object exist by keyname """
        self.assertIn(keyname, models.storage.all())
        """ check if the object found in storage with corrrect id"""
        self.assertTrue(models.storage.all()[keyname] is new)

        """ Test update """
        new.name = "My First Model"
        new.my_number = 89
        self.assertTrue(hasattr(new, "name"))
        self.assertTrue(hasattr(new, "my_number"))
        self.assertTrue(hasattr(models.storage.all()[keyname], "name"))
        self.assertTrue(hasattr(models.storage.all()[keyname], "my_number"))

        """check if save() update update_at time change"""
        old_time = new.updated_at
        new.save()
        self.assertNotEqual(old_time, new.updated_at)
        self.assertGreater(new.updated_at, old_time)

        """ check if init it call: models.storage.save() """
        with patch('models.storage.save') as mock_function:
            obj = BaseModel()
            obj.save()
            mock_function.assert_called_once()

        """check if it save in json file"""
        keyname = "BaseModel."+new.id
        with open(self.filepath, 'r') as file:
            saved_data = json.load(file)
        """ check if object exist by keyname """
        self.assertIn(keyname, saved_data)
        """ check if the value found in json is correct"""
        self.assertEqual(saved_data[keyname], new.to_dict())

    def test_basemodel_init2(self):
        """ class for base test """

        new = BaseModel()
        new.name = "John"
        new.my_number = 89
        new2 = BaseModel(**new.to_dict())
        self.assertEqual(new.id, new2.id)
        self.assertEqual(new.name, "John")
        self.assertEqual(new.my_number, 89)
        self.assertEqual(new.to_dict(), new2.to_dict())

    def test_basemodel_init3(self):
        """ DOC DOC DOC """
        new = BaseModel()
        new2 = BaseModel(new.to_dict())
        self.assertNotEqual(new, new2)
        self.assertNotEqual(new.id, new2.id)

        new = BaseModel()

        self.assertEqual(
            str(new),  "[BaseModel] ({}) {}".format(new.id, new.__dict__))

        old_time = new.updated_at
        new.save()
        self.assertGreater(new.updated_at, old_time)


if __name__ == '__main__':
    unittest.main()
