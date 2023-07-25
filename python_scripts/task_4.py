#!/usr/bin/env python3

"""Counts occurences of all characters within a string 
    (e.g. pythonnohtyppy -> p:3, y:3, t:2, h:2, o:2, n:2)

Usage:
        ./task_4.py [-s --string string]

Author:
        magdalena-w

"""

import argparse

parser = argparse.ArgumentParser(description='Count occurences of all characters withina  string')
parser.add_argument('-w', '--word')
args = parser.parse_args()

word_set = set(args.word)
count_of_chars = dict()

for elem in word_set:
    count_char = args.word.count(elem)
    count_of_chars[elem] = count_char
print(f"Count of characters is: {count_of_chars}")

