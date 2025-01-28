from pickle import load
import matplotlib.pyplot as plt


def single_client_plot():
    plt.figure(figsize=(12, 8))

    for index in range(10):
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
               "tofl_estimator_dl"
               ]

    # servers = ["tofl_estimator_dl","fixed_test"]

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


if __name__ == "__main__":
    
    sizes = ["500",
             "1000",
             "2000",
             "3000"]
    
    for model_size in sizes:
        selection_plot("results/client_selection/","model_size"+model_size)