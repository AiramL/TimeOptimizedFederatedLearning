from pickle import load
import matplotlib.pyplot as plt
from numpy import mean, std

def selection_error_plot(n_clients=95, file_path="results/client_selection/processed/", PLOT=False, language="pt"):

    plt.figure(figsize=(12, 8))
    
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
                   "tofl_estimator_m_fastest": "TOFL Estimating \nand Selecting M-Fastest Clients"}
        
        plt.xlabel("Strategy")
        plt.ylabel("Global Epoch Delay (s)")

    elif language == "pt":
        legends = {"random": "Aleatório",
                   "m_fastest": "M-Fastest (M=50%)",
                   "tofl_oracle": "TOFL Oráculo",
                   "tofl_estimator_dl" : "TOFL Estimador",
                   "tofl_estimator_m_fastest": "TOFL Estimando e \nSelecionando os M-Fastest Clientes"}
        
        plt.xlabel("Estratégia")
        plt.ylabel("Tempo de Trainamento de Época Global (s)")

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

    plt.legend()
    plt.savefig("figures/time_epoch"+str(n_clients)+".png",dpi=300,bbox_inches='tight')

if __name__ == "__main__":

    selection_error_plot()
