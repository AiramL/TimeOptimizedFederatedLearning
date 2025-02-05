#!/bin/bash

cd ..

for speed in $( seq 0 2) 
do
	for index in $( seq 0 9)
	do
		python src/process_throughput.py $speed $index &
	done
done




