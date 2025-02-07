from pickle import load
import matplotlib.pyplot as plt
from numpy import mean, std

def single_client_plot():
    plt.figure(figsize=(12, 8))

    for index in range(20):
        with open("results/7000/results_client"+str(index),"rb") as loader:
            result = load(loader)
            plt.plot(range(101),result,label="client_"+str(index))

    plt.xlabel("Epoch Number (#)")
    plt.ylabel("Delay (s)")
    plt.legend()
    plt.show()

def selection_plot(file_path="results/client_selection/",file_name="model_size500", PLOT=False):
    
    plt.figure(figsize=(12, 8))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl"]

    with open(file_path+file_name,"rb") as loader:
        result = load(loader)
    
    for index, name in enumerate(servers):
        plt.plot(range(1,len(result[index])+1),result[index][:],label=name)

    plt.xlabel("Selected Clients (#)")
    plt.ylabel("Total Training Time (s)")
    plt.legend()
    plt.savefig("figures/"+file_name+".png",dpi=300,bbox_inches='tight')

    if PLOT:
        plt.show()

def selection_error_plot(file_path="results/client_selection/",model_size="model_size500", PLOT=False, n_executions=10):
    
    plt.figure(figsize=(12, 8))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl"]

    results = { server : [ ] for server in servers }
    epochs = range(1,101)

    for server in servers:
        for dataset in range(n_executions):
            with open(file_path+"model_"+server+model_size+"_dataset_"+str(dataset),"rb") as loader:
                result_list = load(loader)
                results[server].append(result_list)
    
    for server in servers:
        m = mean(results[server],axis=0)
        s = std(results[server],axis=0)
        plt.errorbar(epochs, m, yerr=s, capsize=3, label=server)

    plt.xlabel("Selected Clients (#)")
    plt.ylabel("Total Training Time (s)")
    plt.legend()
    plt.savefig("figures/"+model_size[1:]+".png",dpi=300,bbox_inches='tight')

    if PLOT:
        plt.show()

if __name__ == "__main__":
    
    sizes = ["500",
             "1000",
             "2000"]#,
   #          "3000"]
    


    for model_size in sizes:
        selection_error_plot("results/client_selection/speed0/", "_size_"+model_size)
        
