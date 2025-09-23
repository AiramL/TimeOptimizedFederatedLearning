#!/bin/bash

speeds=$(yq '.simulation.speed.index[]' "config/config.yaml") 

for index in $( seq 0 29 )
do
		for speed in $speeds 

		do	
			
			for execution in $( seq 0 9)
			do

				python -m utils.process.results.raw.communication $execution $speed $index &

			done

		done

		wait
done

wait

echo "process finished"
