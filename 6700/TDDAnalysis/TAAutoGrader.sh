#!/usr/bin/env bash
LIST=$1
while read dir; do
	echo $dir
	python TAAutoGrader.py $dir $1
done < $LIST
