#!/bin/bash

cd ..

for index in $( seq 0 29 )
do
		for speed in $( seq 0 2 ) 
		do	

			python process_results/raw_communication.py 0 $speed $index &
			python process_results/raw_communication.py 1 $speed $index &
			python process_results/raw_communication.py 2 $speed $index &
			python process_results/raw_communication.py 3 $speed $index &
			python process_results/raw_communication.py 4 $speed $index &
			python process_results/raw_communication.py 5 $speed $index &
			python process_results/raw_communication.py 6 $speed $index &
			python process_results/raw_communication.py 7 $speed $index &
			python process_results/raw_communication.py 8 $speed $index &
			python process_results/raw_communication.py 9 $speed $index 

		done
done
