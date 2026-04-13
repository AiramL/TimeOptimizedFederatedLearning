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
n_clients_selected_list = cfg['simulation']['federated_learning']['server']['n_clients_list']

for speed in speeds:

    file_path = f"{name}/client_selection/raw/speed{speed}/{base_station_range}"
    file_path_writer = f"{name}/client_selection/processed/speed{speed}/{base_station_range}"

    for size in sizes:
            
        for model in servers:

            for dataset in datasets:
                
                agg_results = []
                
                for n_clients in n_clients_selected_list:
                
                    file = f"model_{model}_size_{size}_dataset_{dataset}_n_clients_{n_clients}"

                    try:

                        with open(f"{file_path}/{file}","rb") as reader:

                            agg_results.append(load(reader))

                    except:

                        print(file)
                    
                file = f"model_{model}_size_{size}_dataset_{dataset}"
                
                os.makedirs(file_path_writer, 
                            exist_ok=True)

                with open(f"{file_path_writer}/{file}","wb") as writer:

                    dump(agg_results, 
                         writer)
