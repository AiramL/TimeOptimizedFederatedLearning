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

def selection_plot():
    plt.figure(figsize=(12, 8))

    servers = ["random",
               "m_fastest",
               "tofl_oracle"]

    

    with open("all_results","rb") as loader:
        result = load(loader)
    
    for index, name in enumerate(servers):
        plt.plot(range(1,len(result[index])),result[index][1:],label=name)

    plt.xlabel("Selected Clients (#)")
    plt.ylabel("Total Training Time (s)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    selection_plot()