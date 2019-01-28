#!/bin/sh
LIST=$1
arg2=$2
while read dir; do
	echo $dir
	python $dir/microservice.py &
	APP_PID=$!
	sleep 1
	python CodeCoverage.py $dir $1 $2 
    kill $(lsof -t -i :5000)
done < $LIST
