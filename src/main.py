from client import *
from server import *

number_of_clients = 10
number_of_clients_to_select = 1
n_epochs = 100
sid = 0

def main(sid=0,
         model_size=527,
         server_type="random",
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
    


    server.set_selected_clients([sid])

    ''' associate clients and server '''
    for client in available_clients.values():
        client.set_server(server)

    ''' simulate the training'''
    server.train()

for sid in range(number_of_clients):
    main(sid,7000)