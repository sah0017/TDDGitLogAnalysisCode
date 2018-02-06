#!/bin/sh
echo "Script has begun"
LIST=$1
arg2=$2
echo $LIST
while read dir; do
	echo $dir 
	python CodeCoverage.py $dir $1 $2 
done < $LIST
