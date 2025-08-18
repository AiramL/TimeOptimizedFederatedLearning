#!/bin/bash

eps=$1
TOFL=$2
numClients=$3
numClientsFit=$4
bs=$5
strategy=$6
dataset=$7
image_flag=0

echo "Verifying if the results directory exists"
[ ! -d ../results/classification/raw/$strategy/$dataset/ ] && mkdir -p ../results/classification/raw/$strategy/$dataset/

echo "Starting server"
cd ../src/federated_learning
if [ "$strategy" = "m_fastest" ]
then	
	[[ $(($numClientsFit/2)) = 0 ]] && numClientsFit=1 || numClientsFit=$(($numClientsFit/2))
	python3.12 server.py -ncf=$numClientsFit -tf=$TOFL -nc=$numClients -nor=$eps &
else	
	python3.12 server.py -ncf=$numClientsFit -tf=$TOFL -nc=$numClients -nor=$eps &
fi

echo "Starting clients"
sleep 3

# initialize clients
for i in $(seq $numClients)
do
	if [ $TOFL -eq 1 ]
	then
		python3.12 client.py -cid=$i -b=$bs -cf=0 >> ../../results/classification/tofl/client_"$i" &
	
	else
		python3.12 client.py -nc=$numClients -cid=$i -b=$bs -cf=0 -ncf=$numClientsFit >> ../../results/classification/raw/$strategy/$dataset/"client_""$i" &
	fi
	echo "Waiting client "$i" initialization"
	sleep 2

done
