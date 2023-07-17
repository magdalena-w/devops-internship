#!/bin/bash

function fibonacci() {
	N=$1
	f0=0
	f1=1

	echo "The Fibonacci series for $N is: "

	for (( i=0; i<N; i++ ))
	do
		echo -n "$f0 "
		fn=$((f0 + f1))
		f0=$f1
		f1=$fn
	done
}

read -p "Enter how many numbers do you want of Fibonacci series: " numbers
fibonacci $numbers
