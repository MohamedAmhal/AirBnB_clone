#!/usr/bin/python3
""" Console module for AirBnB """

import cmd
import json
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """"Class for the console of AirBnB"""

    prompt = "(hbnb) "
    class_dict = {"BaseModel": BaseModel,"User": User,
        "State": State,"City": City,"Amenity": Amenity,
        "Place": Place,"Review": Review
    }

    def emptyline(self):
        """Do nothing when an empty line is entered.
        """
        pass

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """EOF (ctrl + d) to exit the program
        """
        print()
        return True

    def exception_handler(self, name, arg):
        """Handler for method's exception (helper function)
        return 0 if no error found otherwise 1
        """
        args = arg.split()

        if len(args) < 1 and name != "all":
            print("** class name missing **")
            return 1

        classes = HBNBCommand.class_dict
        if len(args) > 0 and args[0] not in classes:
            print("** class doesn't exist **")
            return 1

        if len(args) < 2 and name not in ["create", "all"]:
            print("** instance id missing **")
            return 1

        if name not in ["create", "all"]:
            instance_key = args[0] + '.' + args[1]
            if instance_key not in storage.all():
                print("** no instance found **")
                return 1

        if name == "update":
            if len(args) < 3:
                print("** attribute name missing **")
                return 1
            if len(args) < 4:
                print("** value missing **")
                return 1
        return 0

    def do_create(self, arg):
        """Creates a new instance of BaseModel,
        saves it
        """
        if not self.exception_handler("create", arg):
            classes = HBNBCommand.class_dict
            name = arg.split()[0]
            if name in classes:
                new = classes[name]()
                new.save()
                print(new.id)

    def do_show(self, arg):
        """Show the string representation of an instance:
        Usage: show <class name> <instance id>
        """
        if self.exception_handler("show", arg) == 0:
            args = arg.split()
            instance_key = args[0] + '.' + args[1]
            obj = storage.all()[instance_key]
            print(obj)

    def do_destroy(self, arg):
        """Deletes an instance
        Usage: destroy <instance id>
        """
        if self.exception_handler("destroy", arg) == 0:
            args = arg.split()
            instance_key = args[0] + '.' + args[1]
            del storage.all()[instance_key]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances
    Usage: all
    Usage: all <class name>
        """
        if not self.exception_handler("all", arg):
            args = arg.split()
            list_obj = []
            if len(args) > 0:    # Usage: all <class name>
                name = args[0]
                for key, value in storage.all().items():
                    if name in key:
                        list_obj.append(str(value))
            else:                # Usage: all
                for obj in storage.all().values():
                    list_obj.append(str(obj))
            print(list_obj)

    def do_update(self, arg):
        """Updates an instance by adding or updating attribute:
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        if not self.exception_handler("update", arg):
            args = arg.split()
            class_name = args[0]      # <class name>
            instace_id = args[1]      # <id>
            attribute_name = args[2]  # <attribute name>
            attr_value = args[3]      # <attribute value>
            instance_key = class_name + '.' + instace_id
            obj = storage.all()[instance_key]
            # remove "" and '' around <attribute value>
            if (
                attr_value[0] == '"' and attr_value[-1] == '"' or
                attr_value[0] == "'" and attr_value[-1] == "'"
            ):
                attr_value = attr_value[1:-1]
            # if <attribute name> is already exist then find it's type
            if hasattr(obj, attribute_name):
                # first store the attribute type in a variabe
                data_type = type(getattr(obj, attribute_name))
                try:
                    # cast <attribute value> to it's attribute type
                    attr_value = data_type(attr_value)
                    setattr(obj, attribute_name, attr_value)
                except ValueError:
                    print(f"can't update {attribute_name}: invalid type")
            else:
                setattr(obj, attribute_name, attr_value)
            storage.save()

    def do_count(self, arg):
        """Counts the number of instances of a class based on class name
        Usage: count <class name>
        """
        counter = 0
        arg = arg.strip()
        for instance_key in storage.all().keys():
            if arg == instance_key.split('.')[0]:
                counter += 1
        print(counter)

    def default(self, line):
        """ handle new ways of inputing data """
        method_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "count": self.do_count
        }
        args = line.strip().split(".", 1)  # split only one time
        # example: "Place.update(89, latitude, 5.2)".split(".", 1)
        # => ["Place", "update(89, latitude, 5.2)"] (to keep '.' of floats)
        if len(args) != 2:
            return super().default(line)
        class_name = args[0]
        if class_name not in HBNBCommand.class_dict.keys():
            print("** class doesn't exist **")
            return
        tmp = args[1].split('(')
        # tmp = ["update", "89, latitude, 5.2)"]
        if len(tmp) < 2:
            return super().default(line)
        method_name = tmp[0]                # => "update"
        method_args = tmp[1].split(')')[0]  # => "89, latitude, 5.2"
        if method_name not in method_dict.keys():
            return super().default(line)
        # Handle update arguments
        if method_name == "update":
            if '{' in method_args:  # Update from dictionary
                tmp = method_args.split(',', 1)
                if len(tmp) != 2 or '{' not in tmp[1] or '}' not in tmp[1]:
                    return super().default(line)
                instance_id = tmp[0]
                if "'" in instance_id:
                    instance_id = instance_id.replace("'", " ")
                if '"' in instance_id:
                    instance_id = instance_id.replace('"', " ")
                instance_id = instance_id.strip()
                list_dicts = re.findall(r'{.*?}', tmp[1])
                try:  # pay attention you must replace("'", '"') !!
                    parced_dict = json.loads(list_dicts[0].replace("'", '"'))
                    for attr_name, attr_value in parced_dict.items():
                        final_arg = class_name + " " + instance_id + " "
                        final_arg += str(attr_name) + " " + str(attr_value)
                        self.do_update(final_arg)
                except json.JSONDecodeError:
                    print(f"can't update: invalid type")
                return

            else:  # remove commas (',') and do a normal update
                method_args = method_args.replace(',', ' ')
        final_arg = class_name + " " + method_args
        return method_dict[method_name](final_arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
