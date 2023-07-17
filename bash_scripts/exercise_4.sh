#!/bin/bash

# Caesar Cipher implementation

a=abcdefghijklmnopqrstuvwxyz
b=ABCDEFGHIJKLMNOPQRSTUVWXYZ

function print_usage() {
    echo "usage: $0 [-s shift_value] [-i input_file] [-o output_file]"
}

function encrypt() {
    sed "y/$a$b/${a:$shift}${a::$shift}${b:$shift}${b::$shift}/" input_file > output_file
}

shift=''
input_file=''
output_file=''

while getopts ':s:i:o' flag; do
    case "${flag}" in
        s)  # handle shift
            shift="${OPTARG}"
            ;;
        i)  # handle input file
            input_file="${OPTARG}"
            ;;
        o)  # handle output file 
            output_file="${OPTARG}"
            ;;
        *)  # handle usage
            print_usage
            exit 1
            ;;
    esac
done

encrypt

# Debug output
echo ""
echo "All ARGS: ${@}"

