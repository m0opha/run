#!/usr/bin/python3
import sys
import re
from types import SimpleNamespace

def argumentsTree(argv: list):
    arguments_struct = {}

    unparsed_arguments = " ".join(argv)
    splited_unparsed_arguments = re.split(r" -{1,2}", unparsed_arguments)

    for _argv in splited_unparsed_arguments:

        content_argument = _argv.split(" ")
        arguemnt_name = content_argument[0]

        if len(content_argument) == 1:
            value = None

        if len(content_argument) == 2:
            value = content_argument[1]

        if len(content_argument) > 2:
            value = content_argument[1:]

        arguments_struct[arguemnt_name] = value

    return arguments_struct

class ParserArguments:
    def __init__(self):
        self.system_arguments = sys.argv
        self.filename = self.system_arguments[0]
        self.parsed_arguments = argumentsTree(self.system_arguments)

        self.arguments_added = {}
        self.arguments_allowed = []

    def add(self, *arg, text_help=None, length=1):
        arguments_allowed_forms = sorted(
            [a.strip("-") for a in arg], reverse=True)

        self.arguments_added[arguments_allowed_forms[0]] = {
            "arguments": arguments_allowed_forms,
            "text_help": text_help,
            "length": length,
        }

    def get(self):
        arguments_allowed = [arg for data in self.arguments_added.values() for arg in data["arguments"]]
        ns = SimpleNamespace()

        for arg, _values in self.parsed_arguments.items():

            if arg not in arguments_allowed and arg != self.filename:
                print(f"[-] Argument {arg} not recognized.")
                continue

            if arg == self.filename:
                setattr(ns, "free_values", _values)
                continue
            
            
            variable_name, options = self._getVarName(arg)
            length = options["length"] 
            
            # Si no se pasa ningún valor (None o vacío), se asume booleano
            if _values is None or (_values == [] or _values == ""):
                setattr(ns, variable_name, True)
                continue
            
            if length > len(_values):
                print(f"[-] Maximun values for this {arg} is {length}.")
                continue
            
            setattr(ns, variable_name, _values)

        for arg in arguments_allowed:
            if not hasattr(ns, arg):
                setattr(ns, arg, None)

        return ns

    def _getVarName(self, argument):
        for _variable_name, _values in self.arguments_added.items():
            if argument in _values["arguments"]:
                return _variable_name , self.arguments_added[_variable_name]
