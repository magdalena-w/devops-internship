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
    local res=0
    for k in "${numbers_array[@]}"; do
        res=$((res + k ))
    done
    echo "Addition result: $res"
}

function subtraction {
    local res=${numbers_array[0]}
    for k in "${numbers_array[@]:1}"; do
        res=$((res - k))
    done
    echo "Subtraction result: $res"
}

function multiplication {
    local res=1
    for k in "${numbers_array[@]}"; do
        res=$((res * k))
    done
    echo "Multiplication result: $res"
}

function modulo {
    local res=${numbers_array[0]}
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
        elif [ "$op_parameter" = "+" ]; then
            operation="addition"
        elif [ "$op_parameter" = "*" ]; then
            operation="multiplication"
        elif [ "$op_parameter" = "%" ]; then
            operation="modulo"
        fi
        ;;
		n) # Handle the -n flag 
        numbers+="${OPTARG},"
        IFS=', ' read -r -a numbers_array <<< "$numbers"
        ;;
		d) # Handle the -d flag
        echo "User running the script: $USER" 
        echo "Name of the script: $0"
        echo "Operation: $operation"
        echo "Numbers: ${numbers_array[*]}"
        case "$operation" in
                "addition")
                    addition "${numbers_array[@]}"
                    ;;
                "subtraction")
                    subtraction "${numbers_array[@]}"
                    ;;
                "multiplication")
                    multiplication "${numbers_array[@]}"
                    ;;
                "modulo")
                    modulo "${numbers_array[@]}"
                    ;;
        esac
        ;;
        *)
        echo "Usage: $0 [-o operation_parameter] [-n sequence_of_numbers] [-d debug_flag]" 
        exit 1
	esac
done


