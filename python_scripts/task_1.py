#!/usr/bin/env python3

"""Prints information about extension of the given file.

Usage:
        ./task_1.py [-f name_of_the_file.ext]

Author:
        magdalena-w

"""

import argparse
import re

parser = argparse.ArgumentParser(description="Checking extension of the given file.")
parser.add_argument("-f", "--filename", help="Name of the file you want to check")
args = parser.parse_args()

try:
    splited_str = re.split(r"\.", args.filename)
    if splited_str[0] == '':
        print(f"File '{args.filename}' is a hidden file.")
    else:
        extension = splited_str[1]
        print(f"Extension of the file '{args.filename}' is: {extension}")
except:
    print(f"File '{args.filename}' has no extension.")
