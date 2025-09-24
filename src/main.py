from os import listdir
from .client import *
from .server import *
import threading
import sys

from utils.utils import load_config

def main(sid=0,
         speed=0,
         model_size=527,
         number_of_clients=5,
         server_type="random",
         n_epochs=3,
         datapath="data/processed/v2x_mobility_20_mean.csv",
         number_of_clients_to_select=2,
         m_clients=2):

    df = pd.read_csv(datapath)

    file_name = "results/client_selection/raw/epoch/server_"+server_type+\
                "_n_clients_selected_"+str(number_of_clients_to_select)+\
                "execution_"+datapath.split('/')[3][:-4]

    ''' create multiple clients objects '''
    available_clients = {}
    for client_id in range(number_of_clients):
        available_clients[str(client_id)] = Client(client_id=client_id, 
                                                   model_size=model_size,
                                                   datapath=df, 
                                                   n_epochs=n_epochs)

    if server_type == "random":
        
        server = ServerRandomSelection(avalilable_clients=available_clients,
                                       n_epochs=n_epochs,
                                       file_name=file_name,
                                       n_select_clients=number_of_clients_to_select)

    elif server_type == "fixed":
        
        server = ServerFixedSelection(avalilable_clients=available_clients,
                                    n_epochs=n_epochs,
                                    file_name=file_name,
                                    n_select_clients=number_of_clients_to_select)
        
        server.set_selected_clients(range(number_of_clients_to_select))

    # Need to test
    elif server_type == "m_fastest":
        
        server = ServerMFastestSelection(avalilable_clients=available_clients,
                                         n_epochs=n_epochs,                                              
                                         m_clients=m_clients,
                                         file_name=file_name,
                                         n_select_clients=number_of_clients_to_select)
    
    # Need to test
    elif server_type == "tofl_oracle":
        
        server = ServerOracleTOFLSelection(avalilable_clients=available_clients,
                                           n_epochs=n_epochs,
                                           datapath=df,
                                           file_name=file_name,
                                           n_select_clients=number_of_clients_to_select)
    

    # Need to test
    elif server_type == "tofl_estimator_dl":

        server = ServerEstimatorTOFLSelectionDL(avalilable_clients=available_clients,
                                              n_epochs=n_epochs,
                                              datapath=df,
                                              file_name=file_name,
                                              n_select_clients=number_of_clients_to_select)
   
    elif server_type == "tofl_estimator_m_fastest":
        server = ServerEstimatorTOFLSelectionMFastest(avalilable_clients=available_clients,
                                                      m_clients=m_clients,
                                                      n_epochs=n_epochs,
                                                      datapath=df,
                                                      file_name=file_name,
                                                      n_select_clients=number_of_clients_to_select)

    elif server_type == "fixed_test":
        
        server = ServerFixedTestSelection(avalilable_clients=available_clients,
                                    n_epochs=n_epochs,
                                    file_name=file_name,
                                    n_select_clients=number_of_clients_to_select)
     
    ''' associate clients and server '''
    for client in available_clients.values():
        client.set_server(server)

    ''' simulate the training'''
    return server.train()


def save_results(speed,method,model_size,dataset,number_of_clients_to_select,results):

    with open("results/client_selection/speed"+str(speed)+"/model_"+method+"_size_"+str(model_size)+"_dataset_"+str(dataset)+"_n_clients_"+str(number_of_clients_to_select),"wb") as writer:
        dump(results,writer)

def execute_results_per_client(model_sizes,
                               servers,
                               data,
                               speed, 
                               n_clients,
                               n_epochs,
                               m_ratio):

    number_of_clients = n_clients
    n_epochs = n_epochs
    m_ratio = m_ratio 

    dataset_path = "data/processed/speed"+str(speed)+"/"
    
    threads_local = {}

    for model_size in model_sizes:
    
        for dataset in data:
            
            for method in servers:
            
                print("processing model size ",
                        model_size,
                        " dataset ",
                        dataset)
                
                for number_of_clients_to_select in range(1,number_of_clients+1):                
                    
                    p = int(number_of_clients_to_select*m_ratio)
                    m_clients =  p if p > 0 else 1 
                    
                    threads[str(model_size)+str(dataset)+method+str(number_of_clients_to_select)] =   threading.Thread(target=save_results, args=(speed,method,model_size,dataset,number_of_clients_to_select, main(model_size=model_size,
                   speed=speed,
                   number_of_clients_to_select=number_of_clients_to_select,
                   number_of_clients=number_of_clients,
                   n_epochs=n_epochs,
                   m_clients=m_clients,
                   server_type=method,
                   datapath=dataset_path+str(dataset)+".csv")))
                    
                    threads[str(model_size)+str(dataset)+method+str(number_of_clients_to_select)].start()


if  __name__ == "__main__":

    cfg = load_config("config/config.yaml")


    servers = cfg["simulation"]["strategy"]
    model_sizes= cfg["simulation"]["model"]["size"]
    speeds = cfg["simulation"]["speed"]["index"] 
    n_clients = cfg["simulation"]["cars"] 
    n_epochs = cfg["simulation"]["federated_learning"]["server"]["epochs"] 
    m_ratio = cfg["simulation"]["federated_learning"]["server"]["m_ratio"] 
    

    threads = { }
    
    data_range = 10
    ranges = 1
    ranges_size = int(data_range/ranges)

    for speed in speeds:

        for data in range(data_range):
    
            for server in servers:
        
                for size in model_sizes:

                    threads[server+str(size)+str(data)+str(speed)] = threading.Thread(target=execute_results_per_client, 
                                                                                      args=([size],
                                                                                      [server],
                                                                                      [data],
                                                                                      speed,
                                                                                      n_clients,
                                                                                      n_epochs,
                                                                                      m_ratio))
    
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
