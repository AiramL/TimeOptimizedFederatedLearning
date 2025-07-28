from pickle import load
import matplotlib.pyplot as plt
from numpy import mean, std

def selection_error_plot(n_clients=16, file_path="results/client_selection/processed/", PLOT=False, language="pt"):

    plt.figure(figsize=(14, 10))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl",
               "tofl_estimator_m_fastest"]
    

    if language == "en":
        legends = {"random": "Random",
                   "m_fastest": "M-Fastest (M=50%)",
                   "tofl_oracle": "TOFL Oracle",
                   "tofl_estimator_dl" : "TOFL Estimator",
                   "tofl_estimator_m_fastest": "TOFL Estimating \nand Selecting \nM-Fastest Clients"}
        
        plt.xlabel("Strategy", fontsize=20)
        plt.ylabel("Global Epoch Delay (s)", fontsize=20)

    elif language == "pt":
        legends = {"random": "Aleatório",
                   "m_fastest": "M-Fastest (M=50%)",
                   "tofl_oracle": "TOFL Oráculo",
                   "tofl_estimator_dl" : "TOFL Estimador",
                   "tofl_estimator_m_fastest": "TOFL Estimando e \nSelecionando os \nM-Fastest Clientes"}
        
        plt.xlabel("Estratégia", fontsize=20)
        plt.ylabel("Tempo de Trainamento de Época Global (s)", fontsize=20)

    means = []
    stds = []


    for server in servers:
        with open(file_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"_mean","rb") as loader:
            result_list = load(loader)
            means.append(mean(result_list))
            stds.append(std(result_list))

    plt.bar([ legends[server] for server in servers ], 
            means, 
            yerr=stds, 
            capsize=3)
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=20)
    plt.savefig("figures/time_epoch"+str(n_clients)+".png",dpi=300,bbox_inches='tight')

if __name__ == "__main__":

    for n_clients in [16, 95]:

        selection_error_plot(n_clients=n_clients)
