#!/bin/bash

eps=100
TOFL=0
numClients=100
numClientsFit=10
bs=32
strategy="random"
datataset="VeReMi_Extension"
image_flag="False"

echo "Verifying if the results directory exists"
[ ! -d ../../results/classification/$dataset/$strategy/$numClients/ ] && mkdir -p ../../results/classification/$dataset/$strategy/$numClients/

echo "Starting server"
cd ../src/federated_learning
python3.10 server.py -ncf=$numClientsFit -tf=$TOFL -nc=$numClients -nor=$eps &

echo "Starting clients"
sleep 3

# initialize clients
for i in $(seq $numClients)
do
	if [ $TOFL -eq 1 ]
	then
		python3.10 client.py -cid=$i -b=$bs -cf=0 >> ../../results/classification/tofl/client_"$i" &
	
	else
		python client.py -nc=$numClients -cid=$i -b=$bs -cf=0 -if=$image_flag >> ../../results/classification/$dataset"_"$strategy"_client_""$i" &
	fi
	echo "Waiting client "$i" initialization"
	sleep 2

done
