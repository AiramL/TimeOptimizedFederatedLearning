import os

import matplotlib.pyplot as plt
import numpy as np

from pickle import load
from numpy import (
        mean, 
        std,
)

from utils.utils import load_config 
from .legends import (
    legends_dicts,
    colors,
    style,
)

def selection_error_plot(n_clients=95, 
                         file_path="results/client_selection/processed", 
                         PLOT=False,
                         base_station_range:int=2000,
                         speed:int=0,
                         servers=["random"],
                         language="pt"):

    plt.figure(figsize=(14, 10))
    
    legends = legends_dicts[language]

    if language == "en":
        
        plt.xlabel("Strategy", fontsize=16)
        plt.ylabel("Global Epoch Delay (s)", fontsize=16)

    elif language == "pt":

        plt.xlabel("Estratégia", fontsize=16)
        plt.ylabel("Tempo de Trainamento de Época Global (s)", fontsize=16)

    means = []
    stds = []

    multiplier = 0
    positions_x = []

    for server in servers:

        with open(f"{file_path}/server_{server}_n_clients_selected_{n_clients}_mean","rb") as loader:
        
            result_list = load(loader)

        x = np.arange(len(servers))
        width = 0.75
        
        
        offset = multiplier + 0.5
        
        rects = plt.bar(offset, 
                        mean(result_list), 
                        width, 
                        label=legends_dicts[language][server], 
                        color=colors[server],
                        ecolor="gray",
                        yerr=std(result_list),      
                        capsize=16)        
        
        positions_x.append(offset)
        multiplier += 1

    plt.yticks(fontsize=16)
    plt.xticks(positions_x,
               [ legends_dicts[language][server] for server in servers ],
               fontsize=16,
               rotation=45)

    figure_path = f"figures/time_epoch/speed{speed}/{base_station_range}"
    os.makedirs(figure_path,
                exist_ok=True)

    plt.savefig(f"{figure_path}/{n_clients}_{language}.png",
                dpi=300,
                bbox_inches='tight')

if __name__ == "__main__":

    cfg = load_config('config/config.yaml')
    
    servers = cfg["simulation"]["strategy"]
    speeds = cfg["simulation"]["speed"]["index"]
    base_station_range = cfg['simulation']['base_station']['range']
    
    languages = ["pt", "en"]

    n_clients = [10, 80]

    for speed in speeds:

        for lang in languages:

            for n_client in n_clients:

                file_path = f"results/client_selection/processed/speed{speed}/{base_station_range}"

                selection_error_plot(language=lang,
                                     file_path=file_path,
                                     servers=servers,
                                     base_station_range=base_station_range,
                                     speed=speed,
                                     n_clients=n_client)
