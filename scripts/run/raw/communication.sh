#!/bin/bash

speeds=$(yq '.simulation.speed.index[]' "config/config.yaml") 
mobility=$(yq '.simulation.mobility.repetitions' "config/config.yaml")
communication=$(yq '.simulation.communication.repetitions' "config/config.yaml")

for index in $( seq 0 $(($communication-1)) )
do
		for speed in $speeds 

		do	
			
			for execution in $( seq 0 $(($mobility-1)))
			do

				python -m utils.process.results.raw.communication $execution $speed $index &

			done

		done

		wait
done

wait

echo "process finished"
