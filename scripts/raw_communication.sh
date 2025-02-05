#!/bin/bash

cd ..

for index in $( seq 0 29 )
do
	for speed in $( seq 0 2 )
	do
		for mobility in $( seq 0 9 ) 
		do	
			python src/communication_delays.py $mobility $speed $index &
		done
	done
done
