from os import listdir
from client import *
from server import *
import threading


def main(sid=0,
         model_size=527,
         number_of_clients=10,
         server_type="random",
         n_epochs=10,
         datapath="data/processed/v2x_mobility_20_mean.csv",
         number_of_clients_to_select=2,
         m_clients=2):
    
    ''' create multiple clients objects '''
    available_clients = {}
    for client_id in range(number_of_clients):
        available_clients[str(client_id)] = Client(client_id=client_id, 
                                                   model_size=model_size,
                                                   datapath=datapath, 
                                                   n_epochs=n_epochs)

    if server_type == "random":
        
        server = ServerRandomSelection(avalilable_clients=available_clients,
                                       n_epochs=n_epochs,
                                       file_name="results/server_"+server_type+
                                       "_n_clients_"+str(number_of_clients)+
                                       "_model_size_"+str(model_size),
                                       n_select_clients=number_of_clients_to_select)

    elif server_type == "fixed":
        
        server = ServerFixedSelection(avalilable_clients=available_clients,
                                    n_epochs=n_epochs,
                                    file_name="results/server_"+server_type+
                                    "_client_"+str(sid)+
                                    "_n_clients_"+str(number_of_clients)+
                                    "_model_size_"+str(model_size),
                                    n_select_clients=number_of_clients_to_select)
        
        server.set_selected_clients(range(number_of_clients_to_select))

    # Need to test
    elif server_type == "m_fastest":
        
        server = ServerMFastestSelection(avalilable_clients=available_clients,
                                         n_epochs=n_epochs,                                              
                                         m_clients=m_clients,
                                         file_name="results/server_"+server_type+
                                         "_n_clients_"+str(number_of_clients)+
                                         "_model_size_"+str(model_size),
                                         n_select_clients=number_of_clients_to_select)
    
    # Need to test
    elif server_type == "tofl_oracle":
        
        server = ServerOracleTOFLSelection(avalilable_clients=available_clients,
                                           n_epochs=n_epochs,
                                           datapath=datapath,
                                           file_name="results/server_"+server_type+
                                           "_n_clients_"+str(number_of_clients)+
                                           "_model_size_"+str(model_size),
                                           n_select_clients=number_of_clients_to_select)
    

    # Need to test
    elif server_type == "tofl_estimator_dl":

        server = ServerEstimatorTOFLSelectionDL(avalilable_clients=available_clients,
                                              n_epochs=n_epochs,
                                              datapath=datapath,
                                              file_name="results/server_"+server_type+
                                              "_n_clients_"+str(number_of_clients)+
                                              "_model_size_"+str(model_size),
                                              n_select_clients=number_of_clients_to_select)
    
    elif server_type == "fixed_test":
        
        server = ServerFixedTestSelection(avalilable_clients=available_clients,
                                    n_epochs=n_epochs,
                                    file_name="results/server_"+server_type+
                                    "_client_"+str(sid)+
                                    "_n_clients_"+str(number_of_clients)+
                                    "_model_size_"+str(model_size),
                                    n_select_clients=number_of_clients_to_select)
    

    #elif server_type == "tofl_estimator":
    #    server = ServerEstimatorTOFLSelection()
    
    ''' associate clients and server '''
    for client in available_clients.values():
        client.set_server(server)

    ''' simulate the training'''
    #total_time = server.train()
    #print("total_time: ",total_time," n_clients: ", number_of_clients_to_select, " strategy: ",server_type)
    #return total_time
    # print(server_type)
    return server.train()

def execute_results(model_sizes,servers,data):

    number_of_clients = 100
    n_epochs = 10

    dataset_path = "data/processed/"

    for model_size in model_sizes:
    
        for dataset in data:
            
            for method in servers:
            
                results = [ ]
                
                print("processing model size ",
                        model_size,
                        " dataset ",
                        dataset)
                
                for number_of_clients_to_select in range(1,number_of_clients+1):                
                    
                    results.append(main(model_size=model_size,
                                        number_of_clients_to_select=number_of_clients_to_select,
                                        number_of_clients=number_of_clients,
                                        n_epochs=n_epochs,
                                        m_clients=int(number_of_clients_to_select*0.5),
                                        server_type=method,
                                        datapath=dataset_path+str(dataset)+".csv"))

                with open("results/client_selection/model_"+method+"_size_"+str(model_size)+"_dataset_"+str(dataset),"wb") as writer:
                    dump(results,writer)


if  __name__ == "__main__":

    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl"]
    
    model_sizes=[500,1000,2000,3000]

    threads = { }
    
    for data in range(10):
        for server in servers:
            for size in model_sizes:
                threads[server+str(size)+str(data)] = threading.Thread(target=execute_results, args=([size],[server],[data]))

    for data in range(10):
        for server in servers:
            for size in model_sizes:
                threads[server+str(size)+str(data)].start()

    for data in range(10):
        for server in servers:
            for size in model_sizes:
                threads[server+str(size)+str(data)].join()

    print("experiments finished")
