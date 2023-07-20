#!/bin/bash

function fib {
    local num=$1

    if [ $num -eq 0 ]; then
        echo 0
    elif [ $num -eq 1 ]; then
        echo 1
    elif [ $num -gt 1 ]; then
        ans=$(( $(fib $((num-1))) + $(fib $((num-2))) ))
        echo $ans
    else
        echo "You can only type positive numbers."
    fi
    }

read -p "Enter how many numbers do you want of Fibonacci series: " n

res=$(fib $n)

echo "The Fibonacci series for $n is: $res"

