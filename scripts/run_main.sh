#!/bin/bash

cd ..

for data in 1
do
	for size in 500  
	do
		for speed in 0
		do
				for server in "random" "m_fastest" "tofl_oracle" "tofl_estimator_dl"
			do
				python3.12 src/main.py $server $size $speed $data &
			done
		done
	done
done
