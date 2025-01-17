from client import *
from server import *

number_of_clients = 10
number_of_clients_to_select = 1
n_epochs = 100
sid = 0

''' create multiple clients objects '''
available_clients = {}
for client_id in range(number_of_clients):
    available_clients[str(client_id)] = Client(client_id=client_id)

''' create a server object ''' 
#server = ServerRandomSelection(avalilable_clients=available_clients,
#                               n_epochs=n_epochs,
#                               n_select_clients=number_of_clients_to_select)

server = ServerFixedSelection(avalilable_clients=available_clients,
                               n_epochs=n_epochs,
                               file_name="results_client"+str(sid),
                               n_select_clients=number_of_clients_to_select)

server.set_selected_clients([sid])

''' associate clients and server '''
for client in available_clients.values():
    client.set_server(server)

''' simulate the training'''
server.train()

''' print results '''