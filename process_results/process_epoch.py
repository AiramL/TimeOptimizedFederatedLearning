from numpy import mean, std
from pickle import load, dump

def process_epochs(file_path="results/client_selection/raw/epoch/",n_executions=10):
    
    save_path = "results/client_selection/processed/"

    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl",
               "tofl_estimator_m_fastest"]

    results = { server+str(n_clients) : [] for server in servers for n_clients in range(1,101) }

    for n_clients in range(1,101):
        for server in servers:
            for execution in range(n_executions):
                with open(file_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"execution_"+str(execution),"rb") as loader:
                    result_list = load(loader)
                    results[server+str(n_clients)].append(result_list)


    for n_clients in range(1,101):
        for server in servers:
            with open(save_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"_mean","wb") as writer:
                dump(mean(results[server+str(n_clients)],axis=0),writer)
            
            with open(save_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"_std","wb") as writer:
                dump(std(results[server+str(n_clients)],axis=0),writer)


if __name__ == "__main__":

    process_epochs()
