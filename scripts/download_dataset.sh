#!/bin/bash

echo "Creating directories"

[ ! -d ../datasets/VeReMi_Extension ] && mkdir -p ../datasets/VeReMi_Extension
[ ! -d ../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset ] && mkdir -p ../datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset
[ ! -d ../results/classification/random ] && mkdir -p ../results/classification/random
[ ! -d ../results/classification/tofl ] && mkdir -p ../results/classification/tofl
[ ! -d ../results/classification/kfastest ] && mkdir -p ../results/classification/kfastest

echo "Downloading dataset"

cd ../datasets/VeReMi_Extension
wget https://gta.ufrj.br/~airam/DATASETS/VeReMi/mixalldata_clean.csv --no-check-certificate

cd ../Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset
wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack1withlabels.mat --no-check-certificate
wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack2withlabels.mat --no-check-certificate
wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack4withlabels.mat --no-check-certificate
wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack8withlabels.mat --no-check-certificate
wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack16withlabels.mat --no-check-certificate

cd ../../../utils/
python3.10 get_image_datasets.py
