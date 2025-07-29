from pickle import load
import matplotlib.pyplot as plt
from numpy import mean, std

from legends import legends_dicts

def single_client_plot():

    plt.figure(figsize=(14, 10))

    for index in range(20):
        with open("results/7000/results_client"+str(index),"rb") as loader:
            result = load(loader)
            plt.plot(range(101),result,label="client_"+str(index))

    plt.xlabel("Epoch Number (#)", fontsize=16)
    plt.ylabel("Delay (s)", fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=20)
    plt.show()

def selection_plot(file_path="results/client_selection/",
                   file_name="model_size500", 
                   PLOT=False):
    
    plt.figure(figsize=(12, 8))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl",
               "tofl_estimator_m_fastest"]
    
    legends = legends_dicts["en"]

    with open(file_path+file_name,"rb") as loader:
        result = load(loader)
    
    for index, name in enumerate(servers):
        plt.plot(range(1,len(result[index])+1),result[index][:],label=legends[name])

    plt.xlabel("Selected Clients (#)")
    plt.ylabel("Total Training Time (s)")
    plt.legend()
    plt.savefig("figures/"+file_name+".png",dpi=300,bbox_inches='tight')

    if PLOT:
        plt.show()

def selection_error_plot(file_path="results/client_selection/",model_size="model_size500", PLOT=False, n_executions=10, language="pt"):
    
    plt.figure(figsize=(14, 10))
    
    servers = ["random",
               "m_fastest",
               "tofl_oracle",
               "tofl_estimator_dl",
               "tofl_estimator_m_fastest"]

    legends = legends_dicts[language]

    if language == "en":
        
        plt.xlabel("Selected Clients (#)", fontsize=16)
        plt.ylabel("Total Training Time (s)", fontsize=16)

    elif language == "pt":

        plt.xlabel("Quantidade de Clientes Selecionados (#)", fontsize=16)
        plt.ylabel("Tempo Total de Treinamento (s)", fontsize=16)


    results = { server : [ ] 
               for server in servers }
    
    epochs = range(1,101)

    for server in servers:
        for dataset in range(n_executions):
            with open(file_path+"model_"+server+model_size+"_dataset_"+str(dataset),"rb") as loader:
                result_list = load(loader)
                results[server].append(result_list)
    
    for server in servers:
        m = mean(results[server],axis=0)
        s = std(results[server],axis=0)
        plt.errorbar(epochs, m, yerr=s, capsize=3, label=legends[server])

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=20)

    plt.savefig("figures/communication_model_size"+model_size[1:]+"_"+language+".png",
                dpi=300,
                bbox_inches='tight')

    if PLOT:
        plt.show()

if __name__ == "__main__":
    
    sizes = ["500"]

    for model_size in sizes:

        selection_error_plot("results/client_selection/speed2/", 
                             "_size_"+model_size, 
                             language="pt")
        
