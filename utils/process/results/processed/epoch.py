import yaml
from numpy import mean, std
from pickle import load, dump
from sys import argv

from utils.utils import load_config

def process_epochs(file_path="results/client_selection/raw/epoch/",
                   n_executions=10, 
                   n_selected_list=[1,100],
                   servers = ["random",
                              "m_fastest",
                              "tofl_oracle",
                              "tofl_estimator_dl",
                              "tofl_estimator_m_fastest"]):
    
    save_path = "results/client_selection/processed/"

    results = { server+str(n_clients) : [] for server in servers for n_clients in n_selected_list }

    for n_clients in n_selected_list:
        for server in servers:
            for execution in range(n_executions):
                with open(file_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"execution_"+str(execution),"rb") as loader:
                    result_list = load(loader)
                    results[server+str(n_clients)].append(result_list)


    for n_clients in n_selected_list:

        for server in servers:

            with open(save_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"_mean","wb") as writer:

                dump(mean(results[server+str(n_clients)],axis=0),writer)
            
            with open(save_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"_std","wb") as writer:

                dump(std(results[server+str(n_clients)],axis=0),writer)


if __name__ == "__main__":
    
    if len(argv) > 1:

        name = argv[1]

    else:

        name = "results"

    cfg = load_config("config/config.yaml")

    n_selected_clients_list = cfg["simulation"]["federated_learning"]["server"]["n_clients_list"]

    process_epochs(servers=cfg["simulation"]["strategy"],
                   n_executions=cfg["simulation"]["mobility"]["repetitions"],
                   file_path=f"{name}/client_selection/raw/epoch/", 
                   n_selected_list=n_selected_clients_list)
