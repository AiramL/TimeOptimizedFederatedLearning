import os

from pickle import load
import matplotlib.pyplot as plt
from numpy import mean, std

from utils.utils import load_config 
from .legends import (
    legends_dicts,
    colors,
    style,
)

def selection_error_plot(file_path:str="results/client_selection",
                         model_size:int=500, 
                         base_station_range:int=2000,
                         PLOT:bool=False, 
                         n_executions:int=10, 
                         n_selected:list=[1,100],
                         language:str="pt",
                         servers:list=["random",
                                       "m_fastest",
                                       "tofl_oracle",
                                       "tofl_estimator_dl",
                                       "tofl_estimator_m_fastest"]):
    
    plt.figure(figsize=(14, 10))
    
    legends = legends_dicts[language]

    if language == "en":
        
        plt.xlabel("Selected Clients (#)", fontsize=16)
        plt.ylabel("Total Training Time (s)", fontsize=16)

    elif language == "pt":

        plt.xlabel("Quantidade de Clientes Selecionados (#)", fontsize=16)
        plt.ylabel("Tempo Total de Treinamento (s)", fontsize=16)


    results = { server : [ ] 
               for server in servers }
    
    
    for server in servers:

        for dataset in range(n_executions):
        
            with open(f"{file_path}/model_{server}_size_{model_size}_dataset_{dataset}","rb") as loader:
            
                result_list = load(loader)
                results[server].append(result_list)
    
    for server in servers:
        
        m = mean(results[server],axis=0)
        s = std(results[server],axis=0)
        x = [ index for index in range(1,1+len(m)) ]

        plt.plot(x,
                 m,
                 linewidth=3,
                 label=legends[server],
                 color=colors[server],
                 linestyle=style[server])

        plt.fill_between(x,
                         m - s,
                         m + s,
                         color=colors[server],
                         alpha=0.2)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=16)
    plt.xticks(range(1,len(n_selected)+1), n_selected)
    plt.ylim(0,70)
    
    figure_path = "figures/communication"

    os.makedirs(figure_path, 
                exist_ok=True)

    plt.savefig(f"{figure_path}/model_size_{model_size}_{base_station_range}_{language}.png",
                dpi=300,
                bbox_inches='tight')

    if PLOT:
        
        plt.show()

if __name__ == "__main__":

    cfg = load_config('config/config.yaml')
    
    sizes = cfg["simulation"]["model"]["size"]
    speeds = cfg["simulation"]["speed"]["index"]
    servers = cfg["simulation"]["strategy"]
    repetitions = cfg["simulation"]["mobility"]["repetitions"]
    rounds = cfg["simulation"]["federated_learning"]["server"]["rounds"]    
    base_station_range = cfg['simulation']['base_station']['range']
    n_selected_clients_list = cfg["simulation"]["federated_learning"]["server"]["n_clients_list"]

    for lg in ["pt", "en"]:

        for speed in speeds:

            for model_size in sizes:

                selection_error_plot(f"results/client_selection/speed{speed}/{base_station_range}", 
                                     model_size, 
                                     base_station_range=base_station_range,
                                     servers=servers,
                                     n_executions=repetitions,
                                     n_selected=n_selected_clients_list,
                                     language=lg)
        
