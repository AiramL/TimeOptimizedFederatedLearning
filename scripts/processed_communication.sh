#!/bin/bash

cd ..

for speed in 0 
do
	for index in $( seq 0 9)
	do
		python src/process_throughput.py $speed $index &
	done
done




