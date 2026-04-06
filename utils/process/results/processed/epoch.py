from numpy import (
    mean, 
    std)

from pickle import (
    load, 
    dump)

from sys import argv
from os import makedirs

from utils.utils import load_config

def process_epochs(file_path:str="results/client_selection/raw/epoch",
                   n_executions:int=10,
                   speed:int=0, 
                   n_selected_list:list=[1,100],
                   base_station_range:int=2000,
                   servers:list=["random",
                                 "m_fastest",
                                 "tofl_oracle",
                                 "tofl_estimator_dl",
                                 "tofl_estimator_m_fastest"]) -> None:
    
    save_path = f"results/client_selection/processed/speed{speed}/{base_station_range}"
    makedirs(save_path, exist_ok=True)

    results = { f'{server}{n_clients}' : [] 
                for server in servers 
                for n_clients in n_selected_list }

    for n_clients in n_selected_list:

        for server in servers:
        
            for execution in range(n_executions):
        
                with open(f"{file_path}/server_{server}_n_clients_selected_{n_clients}_execution_{execution}","rb") as loader:
        
                    result_list = load(loader)
                    results[server+str(n_clients)].append(result_list)


    for n_clients in n_selected_list:

        for server in servers:

            with open(f"{save_path}/server_{server}_n_clients_selected_{n_clients}_mean","wb") as writer:

                dump(mean(results[server+str(n_clients)],axis=0),writer)
            
            with open(f"{save_path}/server_{server}_n_clients_selected_{n_clients}_std","wb") as writer:

                dump(std(results[server+str(n_clients)],axis=0),writer)


if __name__ == "__main__":
    
    if len(argv) > 1:

        name = argv[1]

    else:

        name = "results"

    cfg = load_config("config/config.yaml")


    n_selected_clients_list = cfg["simulation"]["federated_learning"]["server"]["n_clients_list"]
    base_station_range = cfg['simulation']['base_station']['range']
    speeds = cfg['simulation']['speed']['index']

    for speed in speeds:

        process_epochs(servers=cfg["simulation"]["strategy"],
                       n_executions=cfg["simulation"]["mobility"]["repetitions"],
                       file_path=f"{name}/client_selection/raw/speed{speed}/{base_station_range}/epoch", 
                       speed=speed,
                       n_selected_list=n_selected_clients_list)
