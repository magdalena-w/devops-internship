#!/bin/bash

# This script generates report file with info about:
# 1) current date and time;
# 2) name of the current user;
# 3) internal IP address and hostname
# 4) external IP address;
# 5) name and version of linux distribution;
# 6) system uptime;
# 7) used and free space (in GB);
# 8) total and free RAM;
# 9) number and frequency of CPU cores

function seperate_sections {
    echo "--------------------------"
    echo ""
} >> report_file.txt
    
function generate_report {
    echo "--------------------------"
    echo "| This is the report file |"
    seperate_sections

    echo "1) Current date and time:"
    date
    seperate_sections
    
    echo "2) Name of the current user:"
    echo "$USER"
    seperate_sections

    echo "3) Internal IP address and hostname:"
    ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}'
    echo "$HOSTNAME"
    seperate_sections

    echo "4) External IP address:" 
    curl https://checkip.amazonaws.com 
    seperate_sections

    echo "5) Name and version of Linux distribution:" 
    uname -v 
    seperate_sections
    
    echo "6) System uptime:" 
    uptime 
    seperate_sections

    echo "7) Used and free space (in GB):" 
    df -h 
    seperate_sections

    echo "8) Total and free RAM:" 
    free -h 
    seperate_sections

    echo "9) Number and frequency of CPU cores:" 
    lscpu | grep "CPU(s)" 
    lscpu | grep "CPU Mhz" 
    seperate_sections
} >> report_file.txt
generate_report
