#!/usr/bin/python3
"""
the main app : the console
"""

import cmd

class HBNBCommand(cmd.Cmd):
    """
    the calss is the instance of the module cmd
    """
    prompt = "(hbnb)"

    def do_quit(self, arg):
        """
        this function is to quit the program
        """

        return True
    
    def help_quit(self):
        """
        Exit the interpereter with simplicity
        """
        print("Exit the interpreter")
    
    def do_EOF(self, arg):
        """
        exit the programm with CTR+D
        """
        print("Exiting...")
        return True
    
    def help_EOF(self):
        """
        Exit the interpereter with the controle+D
        """
        print("exit the interpreter")

    def default(self, line):
        """
        this function is to hadlle the lines empty
        """
        if line == '':
            pass
        else:
            print(f"The command {line} not found !!")
    

    if __name__ == '__main__':
        HBNBCommand().cmdloop()
        

    


    



