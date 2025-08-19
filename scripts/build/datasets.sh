#!/bin/bash

echo "Creating directories"

[ ! -d datasets/VeReMi_Extension ] && mkdir -p datasets/VeReMi_Extension
[ ! -d datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset ] && mkdir -p datasets/Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset
[ ! -d results/classification/random ] && mkdir -p results/classification/random
[ ! -d results/classification/tofl ] && mkdir -p results/classification/tofl
[ ! -d results/classification/kfastest ] && mkdir -p results/classification/kfastest

echo "Downloading dataset"

cd datasets/VeReMi_Extension
[ ! -f mixalldata_clean.csv ] && wget https://gta.ufrj.br/~airam/DATASETS/VeReMi/mixalldata_clean.csv --no-check-certificate

cd ../Modified_VeReMi/WiSec_DataModifiedVeremi_Dataset
[ ! -f attack1withlabels.mat ] && wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack1withlabels.mat --no-check-certificate
[ ! -f attack2withlabels.mat ] && wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack2withlabels.mat --no-check-certificate
[ ! -f attack4withlabels.mat ] && wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack4withlabels.mat --no-check-certificate
[ ! -f attack8withlabels.mat ] && wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack8withlabels.mat --no-check-certificate
[ ! -f attack16withlabels.mat ] && wget https://gta.ufrj.br/~airam/DATASETS/WiSec_DataModifiedVeremi_Dataset/attack16withlabels.mat --no-check-certificate

cd ../../../
