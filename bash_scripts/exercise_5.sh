#!/bin/bash

# Default values
input_file=""
output_file=""
a_word=""
b_word=""

# Flags
convert_vice_versa=false
substitute=false
reverse=false
convert_to_lower=false
convert_to_upper=false


function usage {
    echo "USAGE: $0 [-v] [-s <A_WORD> <B_WORD>] [-r] [-l] [-u] [-i <input_file>] [-o <output_file>]" 
}

function convert_vice_versa {
    local input=$1
    if [ "$convert_vice_versa" = true ]; then
        echo "$input" | tr '[:upper:][:lower:]' '[:lower:][:upper:]'
    else
        echo "$input"
    fi
}

function substitute_words {
    local input=$1
    if [ "$substitute" = true ]; then
        echo "$input" | sed "s/$a_word/$b_word/g"
    else
        echo "$input"
    fi
}

function reverse_lines {
    local input=$1
    if [ "$reverse" = true ]; then
        echo "$input" | tac
    else
        echo "$input"
    fi
}

function convert_to_lowercase {
    local input=$1
    if [ "$convert_to_lower" = true ]; then
        echo "$input" | tr '[:upper:]' '[:lower:]'
    else
        echo "$input"
    fi
}

function convert_to_uppercase {
    local input=$1
    if [ "$convert_to_upper" = true ]; then
        echo "$input" | tr '[:lower:]' '[:upper:]'
    else
        echo "$input"
    fi
}


while getopts 'vs:rlui:o:' arg; do 
    case ${arg} in 
        i) 
            input_file="${OPTARG}"
            ;;
        o)
            output_file="${OPTARG}"
            ;;
        v)
            convert_vice_versa=true
            ;;
        s)
            substitute=true
            a_word="${OPTARG}"
            shift "$((OPTIND-1))"
            b_word="${OPTARG}"
            ;;
        r)
            reverse=true
            ;;
        l)
            convert_to_lower=true
            ;;
        u) 
            convert_to_upper=true
            ;;
        *) # Handle usage option
            usage
            exit 1
            ;; 
    esac
done

# Check for input and output files
if [ -z "$input_file" ] || [ -z "$output_file" ]; then
    echo "Input and output files are mandatory"
    usage
    exit 1
fi

if [ -f "$input_file" ]; then
    text=$(cat "$input_file")

    # Apply tranformations
    transformated_text=$(convert_vice_versa "$text")
    transformated_text=$(substitute_words "$transformated_text")
    transformated_text=$(reverse_lines "$transformated_text")
    transformated_text=$(convert_to_lowercase "$transformated_text")
    transformated_text=$(convert_to_uppercase "$transformated_text")
    
# Write processed text to output file
echo "$transformated_text" > "$output_file"
echo "Text processing complete. Saved to $output_file"

else
    echo "Input file not found: $input_file"
    usage
    exit 1
fi
