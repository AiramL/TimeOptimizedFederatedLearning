import random

def generate_error_list(size, error_rate):

    health_clients = int(size * proporcao_true)
    error_clients  = size - health_client

    clients_ids = [True] * health_clients + [False] * error_clients
    random.shuffle(clients_ids) 

    return clients_ids


def count_true(selected_clients):
    
    counter = 0

    for value in selected_clients.values():

        if value:

            counter += 1

    return counter

# error rate varying from 0% to 90%
error_rate = [ x/10 for x in range(10) ]

servers = ["random",
           "m_fastest",
           "tofl_oracle",
           "tofl_estimator_dl"]

# store results
results = { server:{ int(err*10):[] } for server in servers 
                                      for err in error_rate }

for err in error_rate:
    
    error_list = generate_error_list(size=100, 
                                     error_rate=err)

    for server in servers:
        
        # selecionar com os métodos diferentes
        selected_clients = Server(server)

        # compute results
        results[server][int(10*err)].append(count_true(selected_clients)/num_selected_clients)

