#!/usr/bin/env python3

"""Gets system information like distro info, memory, CPU, current user, system load average, IP addres.

Usage:
        ./task_5.py [-d --distro] [-m --memory] [-c --cpu] [-u --user-info] [-l --load-average] [-i --ip-address]")

Author:
        magdalena-w

"""

import argparse
import os, platform, subprocess, socket, psutil

parser = argparse.ArgumentParser(description='Gets summary system info.')

parser.add_argument('-d', '--distro', action='store_const', const='distro', dest='operation')
parser.add_argument('-m', '--memory',action='store_const', const='memory', dest='operation' )
parser.add_argument('-c', '--cpu', action='store_const', const='cpu', dest='operation' )
parser.add_argument('-u', '--user-info', action='store_const', const='user', dest='operation' )
parser.add_argument('-l', '--load-average', action='store_const', const='load', dest='operation' )
parser.add_argument('-i', '--ip-address', action='store_const', const='ip', dest='operation')

args = parser.parse_args()

def usage():
    parser.print_help()

def get_distro():
    print(platform.platform(aliased=True))

def get_memory():
    virtual_mem = psutil.virtual_memory()
    usage_pct = (virtual_mem.total - virtual_mem.available) / virtual_mem.total * 100
    print(f"Total memory: {virtual_mem.total/1000000} MB")
    print(f"Available memory: {virtual_mem.available/1000000} MB")
    print(f"Used memory: {virtual_mem.used/1000000} MB")
    print(f"Free memory: {virtual_mem.free/1000000} MB")
    print(f"Percentage usage: {round(usage_pct, 2)}%")

def get_cpu():
    cpu_name = subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip()
    print(f"Name of the procesoor: {cpu_name}")
    print(f"Number of logical CPUs in the system: {psutil.cpu_count()}")
    print(f"CPU frequency: {psutil.cpu_freq()}")
    print(f"CPU usage: {psutil.cpu_percent(2)}%")

def get_user():
    print(f"Username: {os.getlogin()}")
    print(f"Home directory: {os.path.expanduser('~')}")
    print(f"Hostname: {platform.node()}")

def get_load():
    load_avg = psutil.getloadavg()
    pct_load_avg = [round(x / psutil.cpu_count(), 2) * 100 for x in load_avg]
    print(f"Load average: {load_avg}")
    print(f"Percentage load average: {pct_load_avg}%")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('8.8.8.8', 1))
        ip_addr = s.getsockname()[0]
    except Exception:
        ip_addr = '127.0.0.1'
    finally:
        s.close()
    print(f"IP Address: {ip_addr}")

def perform_operation(chosen_flag):
    flag_dict = {
        "distro": get_distro,
        "memory": get_memory,
        "cpu": get_cpu,
        "user": get_user,
        "load": get_load,
        "ip": get_ip
        }
    chosen_flag_function = flag_dict.get(chosen_flag)
    return chosen_flag_function()

if args.operation:
    perform_operation(args.operation)
else:
    usage()
