#!/usr/bin/env python3

"""Reads access log from a file and provide the total number
    of different User Agents and statistics with the number of requests from each of them.

Usage:
        ./task_3.py

Author:
        magdalena-w

"""
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(
    description="Provides total number of different User Agents and some statistics"
)
parser.add_argument('-f', '--file', help='Name of the access log file')
args = parser.parse_args()

user_agents = defaultdict(int)

with open(args.file, 'r') as file:
    for line in file:
        # Assuming that file is in specific format
        user_agent = line.split('"')[5]
        user_agents[user_agent] += 1

print(f"Number of different user agents: {len(user_agents)}\n")
print("Statistics about every User Agent:")
for user_agent, requests in user_agents.items():
    print(f"User Agent: \n{user_agent}\nNumber of requests: {requests}\n")

