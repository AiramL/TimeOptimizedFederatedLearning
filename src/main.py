from client import *
from server import *

number_of_clients = 20
number_of_clients_to_select = 10
n_epochs = 100

''' create multiple clients objects '''
available_clients = {}
for client_id in range(1,number_of_clients+1):
    available_clients[str(client_id)] = Client(client_id)

''' create a server object '''
server = Server(avalilable_clients=available_clients,
                n_epochs=n_epochs,
                n_select_clients=number_of_clients_to_select)

''' simulate the training'''
server.train()

''' print results '''