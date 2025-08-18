#!/bin/bash


for speed in 2 
do
	for index in $( seq 0 9)
	do
		python process_results/processed_communication.py $speed $index &
	done
done

wait 

echo "process finished"

