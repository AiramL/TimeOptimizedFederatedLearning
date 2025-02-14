from pickle import load
import matplotlib.pyplot as plt
from numpy import mean, std

def selection_error_plot(file_path="results/client_selection/raw/epoch/", PLOT=False):

    plt.figure(figsize=(12, 8))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl",
               "tofl_estimator_m_fastest"]

    #results = { server : [ ] for server in servers }
    #epochs = range(1,101)
    
    means = []
    stds = []


    for server in servers:
        #for dataset in range(n_executions):
        with open(file_path+"server_"+server+"_n_clients_100_model_size_500_speed_1","rb") as loader:
            result_list = load(loader)
            #results[server].append([np.mean(result_list),np.std(result_list)])
            means.append(mean(result_list))
            stds.append(std(result_list))

    #for server in servers:
        #m = mean(results[server],axis=0)
        #s = std(results[server],axis=0)
        #plt.errorbar(epochs, m, yerr=s, capsize=3, label=server)

    plt.bar(servers, means, yerr=stds, capsize=3)

    plt.xlabel("Strategy")
    plt.ylabel("Global Epoch Delay (s)")
    plt.legend()
    plt.savefig("figures/time_epoch.png",dpi=300,bbox_inches='tight')

if __name__ == "__main__":

    selection_error_plot()
