import flwr as fl

from sys import path
path.append("../../utils/")

from utils import *

args = get_args_server()

num_rounds = args.number_of_rounds #100
server_ip = args.server_ip #'[::]:' 
server_port = args.server_port #'8080'
num_clients_fit = args.num_clients_fit #10
num_clients = args.num_clients #10
TOFL = args.tofl_flag

if TOFL:
    strategy = fl.server.strategy.TOFL(min_available_clients=num_clients,
                                       min_fit_clients=num_clients_fit,
                                       fraction_fit=0.1)
else:
    strategy = fl.server.strategy.FedAvg(min_available_clients=num_clients,
                                         min_fit_clients=num_clients_fit,
                                         fraction_fit=0.1)

fl.server.start_server(config=fl.server.ServerConfig(num_rounds=num_rounds),
                       server_address=server_ip+":"+server_port,
                       strategy=strategy)



