from os import listdir
from client import *
from server import *
import threading
import sys

def main(sid=0,
         speed=0,
         model_size=527,
         number_of_clients=10,
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

def execute_results(model_sizes,servers,data,speed):

    number_of_clients = 100
    n_epochs = 3
    m_ratio = 0.5 

    dataset_path = "data/processed/speed"+str(speed)+"/"

    for model_size in model_sizes:
    
        for dataset in data:
            
            for method in servers:
            
                results = [ ]
                
                print("processing model size ",
                        model_size,
                        " dataset ",
                        dataset)
                
                for number_of_clients_to_select in range(1,number_of_clients+1):                
                    
                    p = int(number_of_clients_to_select*m_ratio)
                    m_clients =  p if p > 0 else 1 
                    
                    results.append(main(model_size=model_size,
                                        speed=speed,
                                        number_of_clients_to_select=number_of_clients_to_select,
                                        number_of_clients=number_of_clients,
                                        n_epochs=n_epochs,
                                        m_clients=m_clients,
                                        server_type=method,
                                        datapath=dataset_path+str(dataset)+".csv"))

                with open("results/client_selection/speed"+str(speed)+"/model_"+method+"_size_"+str(model_size)+"_dataset_"+str(dataset),"wb") as writer:
                    dump(results,writer)

def save_results(speed,method,model_size,dataset,number_of_clients_to_select,results):

    with open("results/client_selection/speed"+str(speed)+"/model_"+method+"_size_"+str(model_size)+"_dataset_"+str(dataset)+"_n_clients_"+str(number_of_clients_to_select),"wb") as writer:
        dump(results,writer)

def execute_results_per_client(model_sizes,servers,data,speed):

    number_of_clients = 100
    n_epochs = 3
    m_ratio = 0.5 

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

    SINGLE = False
    M_CLIENT = True

    if SINGLE:
        server = sys.argv[1]        

        size = int(sys.argv[2])
        
        speed = int(sys.argv[3]) 
        
        data = int(sys.argv[4])

        execute_results([size],[server],[data],speed)

        print("experiments finished")
    
    elif M_CLIENT:
        
        servers = ["random",
                   "m_fastest",
                   "tofl_oracle",
                   "tofl_estimator_dl",
                   "tofl_estimator_m_fastest"]
        

        model_sizes=[500]

        speed = 2 

        threads = { }
        
        data_range = 10
        ranges = 5
        ranges_size = int(data_range/ranges)

        for data in range(data_range):
        
            for server in servers:
            
                for size in model_sizes:
                    threads[server+str(size)+str(data)] = threading.Thread(target=execute_results_per_client, args=([size],[server],[data],speed))
        
        for subset in range(ranges):

            for data in range(subset*ranges_size,(subset+1)*ranges_size):
                if data < data_range:
                    for server in servers:
                        for size in model_sizes:
                            threads[server+str(size)+str(data)].start()
            
            for data in range(subset*ranges_size,(subset+1)*ranges_size):
                if data < data_range:
                    for server in servers:
                        for size in model_sizes:
                            threads[server+str(size)+str(data)].join()

        print("experiments finished")


    else:
        
        servers = ["random",
                   "m_fastest",
                   "tofl_oracle",
                   "tofl_estimator_dl",
                   "tofl_estimator_m_fastest"]
        

        model_sizes=[500]

        speed = 2 

        threads = { }
        
        data_range = 10
        ranges = 1
        ranges_size = int(data_range/ranges)

        for data in range(data_range):

            for server in servers:
                for size in model_sizes:
                    threads[server+str(size)+str(data)] = threading.Thread(target=execute_results, args=([size],[server],[data],speed))
        
        for subset in range(ranges):

            for data in range(subset*ranges_size,(subset+1)*ranges_size):
                if data < data_range:
                    for server in servers:
                        for size in model_sizes:
                            threads[server+str(size)+str(data)].start()
            
            for data in range(subset*ranges_size,(subset+1)*ranges_size):
                if data < data_range:
                    for server in servers:
                        for size in model_sizes:
                            threads[server+str(size)+str(data)].join()

        print("experiments finished")
