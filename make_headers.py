#!/usr/bin/env python3

# Author: Ben Olson
# Date: 7/4/2019

import sys
import re
from pathlib import Path

def print_usage():
    str = """
        Description: Utility to create header file for given *.cpp
        
        Arguments: <file.cpp>
        
        Result: Confirms (y/n) for each function to include,
            then adds include guard named <namespaceprefix>_<file>_H
    """
    print(str)

def main():
    file_path = sys.argv[1]
    file_stem = Path(file_path).stem
    file_ext = Path(file_path).suffix
    functions = []
    namespace_line = re.compile("namespace (.*)")
    namespace = None
    function_line = re.compile("^ *(?P<ret_type>((signed|unsigned|long|short) +)*(\S+)( *(\[\]|\*+|< *\S* *>)){0,1}) +(?P<name>\S+) *(?P<params>\(.*\)) *{{0,1} *(\/\/.*){0,1}$")
    with open(file_path) as f:
        for line in f:
            result = namespace_line.match(line)
            if result:
                namespace = result.group(1)
            result = None
            result = function_line.match(line)
            if result:
                ret_type = result.group('ret_type')
                fun_name = result.group('name')
                fun_args = result.group('params')
                s = ret_type + " " + fun_name + " " + fun_args
                functions.append(s)
    for i, fun in enumerate(functions):
        result = input(f"Add the following function to header (y/n)?\n{fun}\n\n")
        if result.lower() != "y":
           del functions[i] 

    header = file_path[:-len(file_ext)] + ".h"
    with open(header, "w+") as h:
        name = f"{file_stem}_H"
        if namespace:
            name = f"{namespace}_{name}"
        name = name.upper()
        h.write(f"#ifndef {name}\n#define {name}\n\n")
        for fun in functions:
            h.write(f"{fun};\n")
        h.write("\n#endif")

    for fun in functions:
        print(fun)

try:
    main()
except Exception as e:
    print(e)
    print_usage()
