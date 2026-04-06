import os

from pickle import load, dump
from sys import argv

from utils.utils import load_config

cfg = load_config("config/config.yaml")

if len(argv) > 1:

    name = argv[1]

else:

    name = "results"

servers = cfg["simulation"]["strategy"]
sizes = cfg["simulation"]["model"]["size"]
speeds = cfg["simulation"]["speed"]["index"]
datasets = [ i for i in range(cfg["simulation"]["mobility"]["repetitions"]) ]
n_clients_range = cfg["simulation"]["cars"] 
base_station_range = cfg['simulation']['base_station']['range']

for speed in speeds:

    file_path = f"{name}/client_selection/{base_station_range}/speed{speed}/"

    for size in sizes:
            
        for model in servers:

            for dataset in datasets:
                
                agg_results = []
                
                for n_clients in range(1,n_clients_range+1):
                
                    file = "model_"+model+\
                           "_size_"+str(size)+\
                           "_dataset_"+str(dataset)+\
                           "_n_clients_"+str(n_clients)
                    try:
                        with open(file_path+file,"rb") as reader:
                            agg_results.append(load(reader))
                    except:
                        print(file)
                    
                file = "model_"+model+\
                       "_size_"+str(size)+\
                       "_dataset_"+str(dataset)
                
                os.makedirs(file_path, exist_ok=True)

                with open(f"{file_path}/{file}","wb") as writer:

                    dump(agg_results, writer)
