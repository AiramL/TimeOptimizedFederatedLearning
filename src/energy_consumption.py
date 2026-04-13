import os
import random

from utils.utils import load_config 
from pickle import (
        load, 
        dump,
)

def generate_error_list(size, 
                        error_rate):

    error_clients  = int(size * error_rate)
    health_clients = size - error_clients

    clients_ids = [True] * health_clients + [False] * error_clients
    random.shuffle(clients_ids) 

    return clients_ids


def count_true(selected_clients,
               error_list):
    
    counter = 0

    for client in selected_clients:

        value = error_list[client]

        if value:

            counter += 1

    return counter

def read_result(server,
                epoch, 
                path,
                num_selected_clients):
    
    if server == "tofl_estimator_dl":

        server = "tofl"
    
    elif server == "tofl_estimator_m_fastest_clients":

        server = "tofl_mfastest"

    file_name = f"{server}_epoch_{epoch}"

    with open(f"{path}/{file_name}","rb") as reader:

        return load(reader)[:num_selected_clients]



def process_enegy(servers:list=["random"],
                  speed:int=0,
                  base_station_range:int=2000):

    # error rate varying from 0% to 90%
    error_rate = [ x/10 for x in range(10) ]

    # store results
    results = { server:{ int(err*10):[] for err in error_rate } 
                              for server in servers           }

    # experiments configurations
    num_selected_clients = 20
    m_clients = int(num_selected_clients*0.5)
    epochs = [ str(epoch) for epoch in range(1,40) ]


    for epoch in epochs:

        for err in error_rate:
            
            error_list = generate_error_list(size=100, 
                                            error_rate=err)

            for server in servers:
                
                # select with different methods
                if ("m_fastest" == server) or ("tofl_estimator_m_fastest_clients" == server):

                    selected_clients = read_result(server,
                                                   epoch,
                                                   f"results/selected_clients/speed{speed}/{base_station_range}",
                                                   m_clients)

                else:

                    selected_clients = read_result(server,
                                                   epoch,
                                                   f"results/selected_clients/speed{speed}/{base_station_range}",
                                                   num_selected_clients)

                # compute results
                results[server][int(10*err)].append(count_true(selected_clients, error_list)/num_selected_clients)
    
    results_file = f"results/speed{speed}/{base_station_range}" 
    os.makedirs(results_file,
                exist_ok=True)

    with open(f"{results_file}/energy","wb") as writer:
        
        dump(results, writer)

if __name__ == "__main__":

    cfg = load_config('config/config.yaml')

    servers = cfg["simulation"]["strategy"]
    speeds = cfg["simulation"]["speed"]["index"]
    base_station_range = cfg['simulation']['base_station']['range']
    
    for speed in speeds:

        process_enegy(servers=servers,
                      speed=speed,
                      base_station_range=base_station_range)
    
