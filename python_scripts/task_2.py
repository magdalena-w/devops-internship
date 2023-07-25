#!/usr/bin/env python3

"""Transforms given list of integers into a tuple and prints information about minimum and maximum value in the tuple.

Usage:
        ./task_2.py [-l --list num1 num2 num3]
Author:
        magdalena-w - 25.07.2023
    
"""

import argparse
from collections import OrderedDict

parser = argparse.ArgumentParser(description='Prints max and min value from the tuple')
parser.add_argument('-l', '--list', nargs='+', type=int)
args = parser.parse_args()
print(args.list)

numbers = args.list[:]
unique_numbers = tuple(OrderedDict.fromkeys(numbers))
print(f"After removing duplicates and turning into tuple: {unique_numbers}")

min_res = min(unique_numbers)
max_res = max(unique_numbers)
print(f"Min value: {min_res} \nMax value: {max_res}")
