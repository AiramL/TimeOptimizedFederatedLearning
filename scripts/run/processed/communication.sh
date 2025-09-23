#!/bin/bash

speeds=$(yq '.simulation.speed.index[]' "config/config.yaml")

for speed in $speeds

do

	for index in $( seq 0 9)

	do

		python utils/process/results/processed/communication.py $speed $index &

	done

	wait
done

wait 

echo "process finished"

