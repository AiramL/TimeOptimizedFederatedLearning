import os

from sys import argv
from pickle import load
import matplotlib.pyplot as plt
from itertools import accumulate

from utils.utils import load_config 
from .legends import (
    legends_dicts,
    colors,
    style,
)

def get_result_file_name(acc_path:str,
                         dataset:str,
                         strategy:str,
                         n_selected:int):

    mean_file = f"{acc_path}/{strategy}/{dataset}/{n_selected}/mean_model"
    std_file = f"{acc_path}/{strategy}/{dataset}/{n_selected}/std_model"

    return mean_file, std_file

def process_accuracy_delays(n_clients:int=95,
                            dataset:str="WiSec",
                            acc_path:str="results/classification/processed/",
                            time_path:str="results/client_selection/processed",
                            base_station_range=2000,
                            n_executions:int=10,
                            model_size:int=500,
                            n_selected:int=16,
                            speed:int=2,
                            language:str="en",
                            servers:list=[],
                            PLOT:bool=False):
    
    plt.figure(figsize=(12, 8))
     
    legends = legends_dicts[language]
    
    if language == "en":
        
        plt.xlabel("Time (s)",fontsize=16)
        plt.ylabel("Accuracy (%)",fontsize=16)

    elif language == "pt":
        
        plt.xlabel("Tempo (s)",fontsize=16)
        plt.ylabel("Acurácia (%)",fontsize=16)


    results_time = { }
    results = { }
    
    for server in servers:
        
        with open(f"{time_path}/server_{server}_n_clients_selected_{n_clients}_mean","rb") as loader:
            
            result_list = load(loader)
            results_time[server] = list(accumulate(result_list))

    for server in servers:
            
        if server == "m_fastest" or server == "tofl_estimator_m_fastest":
            

            mean_file, std_file = get_result_file_name(acc_path, 
                                                       dataset,
                                                       strategy="m_fastest",
                                                       n_selected=n_selected)
            
        else:
            
            mean_file, std_file = get_result_file_name(acc_path, 
                                                       dataset,
                                                       strategy="random",
                                                       n_selected=n_selected)
        
        with open(mean_file,"rb") as loader:
            
            result_list = load(loader)
            results[server+"mean"] = result_list*100
        
        with open(std_file,"rb") as loader:
        
            result_list = load(loader)
            results[server+"std"] = result_list*100
    

    for server in servers:

        max_epoch = list(results[server+"mean"]).index(max(results[server+"mean"]))
            
        plt.plot(results_time[server][:max_epoch],
                 results[server+"mean"][:max_epoch],
                 linewidth=3,
                 label=legends[server],
                 color=colors[server],
                 linestyle=style[server])

        plt.fill_between(results_time[server][:max_epoch],
                         results[server+"mean"][:max_epoch] - results[server+"std"][:max_epoch],
                         results[server+"mean"][:max_epoch] + results[server+"std"][:max_epoch],
                         color=colors[server],
                         alpha=0.2)


    figure_path = f"figures/time_to_accuracy/speed{speed}/{base_station_range}/{dataset}"
    os.makedirs(figure_path, 
                exist_ok=True)

    plt.ylim(78,84)
    
    if dataset == "WiSec":

        #plt.xlim(0,9)
        plt.xlim(0,1000)
    
    elif dataset == "VeReMi":

        #plt.xlim(0,7.5)
        plt.xlim(0,1000)
    

    plt.legend()
    plt.savefig(f"{figure_path}/n_clients_{n_clients}_{language}.png",
                dpi=300,
                bbox_inches='tight')
    
    if PLOT:
        
        plt.show()
    

if __name__ == "__main__":

    if len(argv) > 1:

        name = argv[1]

    else:

        name = "results"
    
    cfg = load_config('config/config.yaml')
    
    servers = cfg["simulation"]["strategy"]
    speeds = cfg["simulation"]["speed"]["index"]
    base_station_range = cfg['simulation']['base_station']['range']
    
    n_clients = [10, 80]
    languages = ["en", "pt"]
    datasets = ["WiSec", "VeReMi"]

    for speed in speeds:
            
        for client in n_clients:

            for lang in languages:

                for dataset in datasets:

                    process_accuracy_delays(dataset=dataset,
                                            n_clients=client,
                                            acc_path=f"{name}/classification/processed",
                                            time_path=f"{name}/client_selection/processed/speed{speed}/{base_station_range}",
                                            base_station_range=base_station_range,
                                            language=lang,
                                            servers=servers)
        
