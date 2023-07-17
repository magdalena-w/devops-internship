#!/bin/bash

# Caesar Cipher implementation

a=abcdefghijklmnopqrstuvwxyz
b=ABCDEFGHIJKLMNOPQRSTUVWXYZ

function print_usage() {
    echo "usage: $0 [-s shift_value_value] [-i input_file] [-o output_file]"
}

function encrypt() {
    sed "y/$a$b/${a:$shift_value}${a::$shift_value}${b:$shift_value}${b::$shift_value}/" "$input_file" > "$output_file"
}

while getopts 's:i:o:' flag; do
    case "${flag}" in
        s)  # handle shift_value
            shift_value="${OPTARG}"
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
