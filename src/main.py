from client import *
from server import *

number_of_clients = 10
#number_of_clients_to_select = 1
n_epochs = 100
sid = 0
model_size=527

def main(sid=0,
         model_size=527,
         number_of_clients=10,
         server_type="random",
         n_epochs=10,
         number_of_clients_to_select=2,
         m_clients=2):
    
    ''' create multiple clients objects '''
    available_clients = {}
    for client_id in range(number_of_clients):
        available_clients[str(client_id)] = Client(client_id=client_id, 
                                                   model_size=model_size, 
                                                   n_epochs=n_epochs)

    ''' create a server object ''' 
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
        
        server.set_selected_clients([sid])

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
                                           file_name="results/server_"+server_type+
                                           "_n_clients_"+str(number_of_clients)+
                                           "_model_size_"+str(model_size),
                                           n_select_clients=number_of_clients_to_select)
    

    # Need to test
    elif server_type == "tofl_estimator":

        server = ServerTOFLEstimatorSelection(avalilable_clients=available_clients,
                                              n_epochs=n_epochs,
                                              file_name="results/server_"+server_type+
                                              "_n_clients_"+str(number_of_clients)+
                                              "_model_size_"+str(model_size),
                                              n_select_clients=number_of_clients_to_select)
    

    ''' associate clients and server '''
    for client in available_clients.values():
        client.set_server(server)

    ''' simulate the training'''
    return server.train()


if  __name__ == "__main__":

    servers = ["random",
                "m_fastest",
                "tofl_oracle"]

    results = [ [] for i in range(len(servers)) ]

    for number_of_clients_to_select in range(1,number_of_clients+1):
        
    
            
        for index, method in enumerate(servers):
            results[index].append(main(model_size=model_size,
                                    number_of_clients_to_select=number_of_clients_to_select,
                                    number_of_clients=number_of_clients,
                                    n_epochs=n_epochs,
                                    m_clients=int(number_of_clients_to_select*0.5),
                                    server_type=method))

    with open("all_results","wb") as writer:
        dump(results,writer)