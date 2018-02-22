#!/bin/sh
LIST=$1
arg2=$2
while read dir; do
	echo $dir 
	python CodeCoverage.py $dir $1 $2 
done < $LIST
