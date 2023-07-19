#!/bin/bash

# This script is accepting operation parameter (“-”, “+”, “*”, “%”), sequence of numbers and debug flag.
# If -d flag is passed, script prints additional information:
# - User: <username of the user running the script>
# - Script: <script name>        
# - Operation: <operation>
# - Numbers: <all space-separated numbers>

# list of arguments expected in the input
optstring="o:n:d"

function addition {
    res=0
    for k in "${numbers_array[@]}"; do
        res=$((res + k ))
    done
    echo "Addition result: $res"
}

function subtraction {
    res=${numbers_array[0]}
    for k in "${numbers_array[@]:1}"; do
        res=$((res - k))
    done
    echo "Subtraction result: $res"
}

function multiplication {
    res=0
    for k in "${numbers_array[@]}"; do
        res=$((res * k))
    done
    echo "Multiplication result: $res"
}

function modulo {
    res=${numbers_array[0]}
    for k in "${numbers_array[@]:1}"; do
        res=$(( res%k ))
    done
    echo "Modulo result: $res"
}

while getopts ${optstring} arg; do
    case "${arg}" in
	    o) # Handle the -o flag
        op_parameter=${OPTARG}
        if [ "$op_parameter" = "-" ]; then
            operation="subtraction"
            subtraction
        elif [ "$op_parameter" = "+" ]; then
            operation="addition"
            addition
        elif [ "$op_parameter" = "*" ]; then
            operation="multiplication"
            multiplication
        elif [ "$op_parameter" = "%" ]; then
            operation="modulo"
            modulo
        fi
        ;;
		n) # Handle the -n flag 
        numbers+=${OPTARG}
        IFS=', ' read -r -a numbers_array <<< "$numbers"
        ;;
		d) # Handle the -d flag
        echo "User running the script: $USER" 
        echo "Name of the script: $0"
        echo "Operation: $operation"
        echo "Numbers: ${numbers_array[*]}"
		;;
        *)
        echo "Usage: $0 [-o operation_parameter] [-n sequence_of_numbers] [-d debug_flag]" 
	esac
done


