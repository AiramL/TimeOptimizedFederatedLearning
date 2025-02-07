#!/bin/bash

eps=20
TOFL=0
numClients=20
numClientsFit=10
bs=32
strategy="random"
dataset="VeReMi_Extension"
image_flag=0

echo "Verifying if the results directory exists"
[ ! -d ../../results/classification/$dataset/$strategy/$numClients/ ] && mkdir -p ../../results/classification/$dataset/$strategy/$numClients/

echo "Starting server"
cd ../src/federated_learning
if [ "$strategy" = "kfastest" ]
then	
	[[ $(($numClientsFit/2)) = 0 ]] && numClientsFit=1 || numClientsFit=$(($numClientsFit/2))
	python3.10 server.py -ncf=$numClientsFit -tf=$TOFL -nc=$numClients -nor=$eps &
else	
	python3.10 server.py -ncf=$numClientsFit -tf=$TOFL -nc=$numClients -nor=$eps &
fi

echo "Starting clients"
sleep 3

# initialize clients
for i in $(seq $numClients)
do
	if [ $TOFL -eq 1 ]
	then
		python3.10 client.py -cid=$i -b=$bs -cf=0 >> ../../results/classification/tofl/client_"$i" &
	
	else
		python3.10 client.py -nc=$numClients -cid=$i -b=$bs -cf=0 -ncf=$numClientsFit >> ../../results/classification/raw/$strategy/$dataset"_client_""$i" &
	fi
	echo "Waiting client "$i" initialization"
	sleep 2

done
