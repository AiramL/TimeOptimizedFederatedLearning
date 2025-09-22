#!/bin/bash

speeds=$(yq '.simulation.speed.index' "config/config.yaml") 

for index in $( seq 0 29 )
do
		for speed in speeds 

		do	

			python -m process_results.raw_communication 0 $speed $index &
			python -m process_results.raw_communication 1 $speed $index &
			python -m process_results.raw_communication 2 $speed $index &
			python -m process_results.raw_communication 3 $speed $index &
			python -m process_results.raw_communication 4 $speed $index &
			python -m process_results.raw_communication 5 $speed $index &
			python -m process_results.raw_communication 6 $speed $index &
			python -m process_results.raw_communication 7 $speed $index &
			python -m process_results.raw_communication 8 $speed $index &
			python -m process_results.raw_communication 9 $speed $index &

		done

		wait
done

wait

echo "process finished"
