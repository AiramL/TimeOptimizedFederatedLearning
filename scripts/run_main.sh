#!/bin/bash

cd ..

for data in $( seq 0 9 )
do
	for size in 500 1000 2000 3000 
	do
		for speed in 0 #1 2
		do
				for server in "random" "m_fastest" "tofl_oracle" "tofl_estimator_dl"
			do
				python3.12 src/main.py $server $size $speed $data &
			done
		done
	done
done
