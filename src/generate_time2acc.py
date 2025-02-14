from pickle import load
from itertools import accumulate

def process_accuracy_delays(acc_path,time_path="results/client_selection/raw/epoch/",n_executions=10,model_size=500):
    
    plt.figure(figsize=(12, 8))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl",
               "tofl_estimator_m_fastest"]
    
    results_time = { server : [] for server in servers }

    for server in servers:
        #for dataset in range(n_executions):
        with open(time_path+"server_"+server+"_n_clients_100_model_size_500_speed_1","rb") as loader:
            result_list = load(loader)
            results_time[server].append(list(accumulate(result_list)))

    for server in servers:
        for dataset in range(n_executions):
            with open(acc_path+"model_"+server+model_size+"_dataset_"+str(dataset),"rb") as loader:
                result_list = load(loader)
                results[server].append(result_list)
    
    for server in servers:
        m = mean(results[server],axis=0)
        s = std(results[server],axis=0)
        plt.errorbar(results_time[server], m, yerr=s, capsize=3, label=server)

    plt.xlabel("Time (s)")
    plt.ylabel("Accuracy (%)")
    plt.legend()
    plt.savefig("figures/time2acc.png",dpi=300,bbox_inches='tight')

if __name__ == "__main__":
    process_accuracy_delays()
