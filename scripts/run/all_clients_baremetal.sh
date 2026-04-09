#!/bin/bash

if [ $1 ]; 
then	
	eps=$1
	TOFL=$2
	numClients=$3
	numClientsFit=$4
	bs=$5
	strategy=$6
	dataset=$7

else
	
	eps=3
	TOFL=0
	numClients=5
	numClientsFit=2
	bs=128
	strategy="random"
	dataset="VeReMi"

fi

image_flag=0

echo "Verifying if the results directory exists"
[ ! -d results/classification/raw/$strategy/$dataset/$numClientsFit/ ] && mkdir -p results/classification/raw/$strategy/$dataset/$numClientsFit/

echo "Starting server"

if [ "$strategy" = "m_fastest" ]
then	
	[[ $(($numClientsFit/2)) = 0 ]] && numClientsFit=1 || numClientsFit=$(($numClientsFit/2))
	[ ! -d results/classification/raw/$strategy/$dataset/$numClientsFit/ ] && mkdir -p results/classification/raw/$strategy/$dataset/$numClientsFit/
	python3.12 -m src.federated_learning.server -ncf=$numClientsFit -tf=$TOFL -nc=$numClients -nor=$eps &
else	
	python3.12 -m src.federated_learning.server -ncf=$numClientsFit -tf=$TOFL -nc=$numClients -nor=$eps &
fi

echo "Starting clients"
sleep 5

# initialize clients
python3.12 -m src.federated_learning.all_clients -nc=$numClients -cid=1 -b=$bs -cf=0 -ncf=$numClientsFit -st=$strategy &
wait
