import os
import threading
import pandas as pd

from pickle import dump

from .client import Client
from .servers import (
    ServerRandomSelection,
    ServerMFastestSelection,
    ServerFixedSelection,
    ServerOracleTOFLSelection,
    ServerEstimatorTOFLSelectionDL,
    ServerEstimatorTOFLSelectionMFastest,
    ServerEstimatorTOFLSelectionMFastestClients,
    ServerFixedSelection,
    ServerFixedTestSelection,
)

from utils.utils import load_config

def main(sid:int=0,
         speed:int=0,
         model_size:int=527,
         number_of_clients:int=5,
         server_type:str="random",
         n_rounds:int=3,
         datapath:str="data/processed/v2x_mobility_20_mean.csv",
         number_of_clients_to_select:int=2,
         m_clients:int=2,
         base_station_range:int=2000,
         execution:int=0):

    df = pd.read_csv(datapath)

    results_path = f"results/client_selection/raw/speed{speed}/{base_station_range}/epoch"

    os.makedirs(results_path, 
                exist_ok=True)
    
    selected_clients_path = f"results/selected_clients/speed{speed}/{base_station_range}" 
    
    os.makedirs(selected_clients_path, 
                exist_ok=True)

    log_path = "logs/clients"
    os.makedirs(log_path,
                exist_ok=True)

    file_name = f"{results_path}/server_{server_type}_n_clients_selected_{number_of_clients_to_select}_execution_{execution}"

    ''' create multiple clients objects '''
    available_clients = {}

    for client_id in range(number_of_clients):

        available_clients[str(client_id)] = Client(client_id=client_id, 
                                                   model_size=model_size,
                                                   datapath=df, 
                                                   n_rounds=n_rounds)

    if server_type == "random":
        
        server = ServerRandomSelection(avalilable_clients=available_clients,
                                       n_rounds=n_rounds,
                                       file_name=file_name,
                                       base_station_range=base_station_range,
                                       n_select_clients=number_of_clients_to_select)

    elif server_type == "fixed":
        
        server = ServerFixedSelection(avalilable_clients=available_clients,
                                    n_rounds=n_rounds,
                                    file_name=file_name,
                                    base_station_range=base_station_range,
                                    n_select_clients=number_of_clients_to_select)
        
        server.set_selected_clients(range(number_of_clients_to_select))

    # Need to test
    elif server_type == "m_fastest":
        
        server = ServerMFastestSelection(avalilable_clients=available_clients,
                                         n_rounds=n_rounds,                                              
                                         m_clients=m_clients,
                                         file_name=file_name,
                                         base_station_range=base_station_range,
                                         n_select_clients=number_of_clients_to_select)
    
    # Need to test
    elif server_type == "tofl_oracle":
        
        server = ServerOracleTOFLSelection(avalilable_clients=available_clients,
                                           n_rounds=n_rounds,
                                           datapath=df,
                                           file_name=file_name,
                                           base_station_range=base_station_range,
                                           n_select_clients=number_of_clients_to_select)
    

    elif server_type == "tofl_estimator_dl":

        server = ServerEstimatorTOFLSelectionDL(avalilable_clients=available_clients,
                                                n_rounds=n_rounds,
                                                datapath=df,
                                                file_name=file_name,
                                                n_select_clients=number_of_clients_to_select,
                                                base_station_range=base_station_range)
   
    elif server_type == "tofl_estimator_m_fastest_clients":
        
        server = ServerEstimatorTOFLSelectionMFastestClients(avalilable_clients=available_clients,
                                                             m_clients=m_clients,
                                                             n_rounds=n_rounds,
                                                             datapath=df,
                                                             file_name=file_name,
                                                             n_select_clients=number_of_clients_to_select,
                                                             base_station_range=base_station_range)
    
    elif server_type == "tofl_estimator_m_fastest":

        server = ServerEstimatorTOFLSelectionMFastest(avalilable_clients=available_clients,
                                                             m_clients=m_clients,
                                                             n_rounds=n_rounds,
                                                             datapath=df,
                                                             file_name=file_name,
                                                             n_select_clients=number_of_clients_to_select)

    elif server_type == "fixed_test":
        
        server = ServerFixedTestSelection(avalilable_clients=available_clients,
                                          n_rounds=n_rounds,
                                          file_name=file_name,
                                          base_station_range=base_station_range,
                                          n_select_clients=number_of_clients_to_select)
     
    ''' associate clients and server '''
    for client in available_clients.values():
        
        client.set_server(server)

    ''' simulate the training'''
    return server.train()


def save_results(file_path,
                 file_name,
                 results):

    os.makedirs(file_path, exist_ok=True)

    with open(f"{file_path}/{file_name}","wb") as writer:

        dump(results,writer)

def execute_results_per_client(model_sizes:list,
                               servers:list,
                               data:list,
                               speed:int, 
                               n_clients:int,
                               n_rounds:int,
                               m_ratio:float,
                               number_of_clients_list:list,
                               base_station_range:int):

    n_rounds = n_rounds
    m_ratio = m_ratio 

    dataset_path = f"data/processed/speed{speed}/{base_station_range}"
    
    threads_local = {}

    for model_size in model_sizes:
    
        for dataset in data:
            
            for method in servers:
            
                print("processing model size ",
                        model_size,
                        " dataset ",
                        dataset)
                
                for number_of_clients_to_select in number_of_clients_list:                
                    
                    p = int(number_of_clients_to_select*m_ratio)
                    m_clients =  p if p > 0 else 1 
                    
                    file_path = f"results/client_selection/raw/speed{speed}/{base_station_range}"
                    file_name = f"model_{method}_size_{model_size}_dataset_{dataset}_n_clients_{number_of_clients_to_select}"

                    threads_local[f'{model_size}{dataset}{method}{number_of_clients_to_select}'] = threading.Thread(target=save_results, 
                                                                                                                     args=(file_path,
                                                                                                                           file_name, 
                                                                                                                           main(model_size=model_size,
                                                                                                                                speed=speed,
                                                                                                                                number_of_clients_to_select=number_of_clients_to_select,
                                                                                                                                number_of_clients=n_clients,
                                                                                                                                n_rounds=n_rounds,
                                                                                                                                m_clients=m_clients,
                                                                                                                                server_type=method,
                                                                                                                                datapath=f"{dataset_path}/{dataset}.csv",
                                                                                                                                execution=dataset,
                                                                                                                                base_station_range=base_station_range)))
                                                                                                                                    
                    threads_local[f'{model_size}{dataset}{method}{number_of_clients_to_select}'].start()


if  __name__ == "__main__":

    cfg = load_config("config/config.yaml")


    servers = cfg["simulation"]["strategy"]
    model_sizes= cfg["simulation"]["model"]["size"]
    speeds = cfg["simulation"]["speed"]["index"] 
    n_clients = cfg["simulation"]["cars"] 
    n_rounds = cfg["simulation"]["federated_learning"]["server"]["rounds"] 
    m_ratio = cfg["simulation"]["federated_learning"]["server"]["m_ratio"] 
    data_range = cfg["simulation"]["mobility"]["repetitions"] 
    n_selected_clients_list = cfg["simulation"]["federated_learning"]["server"]["n_clients_list"]
    base_station_range = cfg['simulation']['base_station']['range']

    threads = { }
    
    ranges = 1
    ranges_size = int(data_range/ranges)

    for speed in speeds:

        for data in range(data_range):
    
            for server in servers:
        
                for size in model_sizes:

                    threads[f'{server}{size}{data}{speed}'] = threading.Thread(target=execute_results_per_client, 
                                                                                      args=([size],
                                                                                            [server],
                                                                                            [data],
                                                                                            speed,
                                                                                            n_clients,
                                                                                            n_rounds,
                                                                                            m_ratio,
                                                                                            n_selected_clients_list,
                                                                                            base_station_range))
    
    for subset in range(ranges):

        for speed in speeds:

            for data in range(subset*ranges_size,(subset+1)*ranges_size):

                if data < data_range:
                
                    for server in servers:
                    
                        for size in model_sizes:
                        
                            threads[server+str(size)+str(data)+str(speed)].start()
        
        for speed in speeds:
    
            for data in range(subset*ranges_size,(subset+1)*ranges_size):

                if data < data_range:
                
                    for server in servers:
                    
                        for size in model_sizes:
                        
                            threads[server+str(size)+str(data)+str(speed)].join()

    print("experiments finished")
