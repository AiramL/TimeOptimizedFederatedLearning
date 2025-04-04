from pickle import load
import matplotlib.pyplot as plt
from itertools import accumulate

def process_accuracy_delays(n_clients=95,
                            dataset="WiSec",
                            acc_path="results/classification/processed/",
                            time_path="results/client_selection/processed/",
                            n_executions=10,
                            model_size=500,
                            language="pt"):
    
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
                   "tofl_estimator_m_fastest": "TOFL Estimating and Selecting M-Fastest Clients"}
        
        plt.xlabel("Time (s)")
        plt.ylabel("Accuracy (%)")

    elif language == "pt":
        legends = {"random": "Aleatório",
                   "m_fastest": "M-Fastest (M=50%)",
                   "tofl_oracle": "TOFL Oráculo",
                   "tofl_estimator_dl" : "TOFL Estimador",
                   "tofl_estimator_m_fastest": "TOFL Estimando e Selecionando os M-Fastest Clientes"}
        
        plt.xlabel("Tempo (s)")
        plt.ylabel("Acurácia (%)")


    results_time = { }
    results = { }
    
    for server in servers:
        with open(time_path+"server_"+server+"_n_clients_selected_"+str(n_clients)+"_mean","rb") as loader:
            result_list = load(loader)
            results_time[server] =  list(accumulate(result_list))

    for server in servers:
            
        if server == "m_fastest" or server == "tofl_estimator_m_fastest":
            mean_file = acc_path+"m_fastest/"+dataset+"_mean_model"
            std_file = acc_path+"m_fastest/"+dataset+"_std_model"
            
        else:
            mean_file = acc_path+"random/"+dataset+"_mean_model"
            std_file = acc_path+"random/"+dataset+"_std_model"
        
        with open(mean_file,"rb") as loader:
            result_list = load(loader)
            results[server+"mean"] = result_list*100
        
        with open(std_file,"rb") as loader:
            result_list = load(loader)
            results[server+"std"] = result_list*100
    
    for server in servers:
        plt.errorbar(results_time[server][1:], 
                     results[server+"mean"][:40], 
                     yerr=results[server+"std"][:40], 
                     capsize=3, 
                     label=legends[server])
    
    plt.legend()
    plt.savefig("figures/"+dataset+"_time2acc.png",dpi=300,bbox_inches='tight')

if __name__ == "__main__":

    process_accuracy_delays(dataset="WiSec")
    process_accuracy_delays(dataset="VeReMi")
