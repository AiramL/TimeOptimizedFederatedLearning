#!/bin/bash

cd ..

for index in $( seq 0 29 )
do
		for speed in $( seq 0 2 ) 
		do	
			python src/communication_delays.py 0 $speed $index &
			python src/communication_delays.py 1 $speed $index &
			python src/communication_delays.py 2 $speed $index &
			python src/communication_delays.py 3 $speed $index &
			python src/communication_delays.py 4 $speed $index &
			python src/communication_delays.py 5 $speed $index &
			python src/communication_delays.py 6 $speed $index &
			python src/communication_delays.py 7 $speed $index &
			python src/communication_delays.py 8 $speed $index &
			python src/communication_delays.py 9 $speed $index 
		done
done
