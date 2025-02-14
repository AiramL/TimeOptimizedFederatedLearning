from pickle import load
import matplotlib.pyplot as plt
from numpy import mean, std

def selection_error_plot(n_clients=95, file_path="results/client_selection/processed/", PLOT=False):

    plt.figure(figsize=(12, 8))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl",
               "tofl_estimator_m_fastest"]
 
    means = []
    stds = []


    for server in servers:
        with open(file_path+"server_"+server+"_n_clients_selected"+str(n_clients)+"_mean","rb") as loader:
            result_list = load(loader)
            means.append(mean(result_list))
            stds.append(std(result_list))

    plt.bar(servers, means, yerr=stds, capsize=3)

    plt.xlabel("Strategy")
    plt.ylabel("Global Epoch Delay (s)")
    plt.legend()
    plt.savefig("figures/time_epoch.png",dpi=300,bbox_inches='tight')

if __name__ == "__main__":

    selection_error_plot()
