import random

from pickle import load, dump

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

    file_name = server+"epoch"+epoch

    with open(path+file_name,"rb") as reader:

        return load(reader)[:num_selected_clients]

# error rate varying from 0% to 90%
error_rate = [ x/10 for x in range(10) ]

servers = ["random",
           "m_fastest",
           "tofl_oracle",
           "tofl_mfastest",
           "tofl"]

# store results
results = { server:{ int(err*10):[] for err in error_rate } 
                          for server in servers           }

# experiments configurations
num_selected_clients = 16
m_clients = int(num_selected_clients*0.5)
epochs = [ str(epoch) for epoch in range(1,11) ]


for epoch in epochs:

    for err in error_rate:
        
        error_list = generate_error_list(size=100, 
                                        error_rate=err)

        for server in servers:
            
            # select with different methods
            if server == "m_fastest":

                selected_clients = read_result(server,
                                               epoch,
                                               "results/selected_clients/",
                                               m_clients)

            else:

                selected_clients = read_result(server,
                                               epoch,
                                               "results/selected_clients/",
                                               num_selected_clients)

            # compute results
            results[server][int(10*err)].append(count_true(selected_clients, error_list)/num_selected_clients)

with open("results/energy","wb") as writer:
    
    dump(results, writer)