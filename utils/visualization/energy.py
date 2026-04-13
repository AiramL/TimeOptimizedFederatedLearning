import os

import numpy as np
import matplotlib.pyplot as plt

from pickle import load
from numpy import (
        mean, 
        std
)

from utils.utils import load_config 
from .legends import (
    legends_dicts,
    colors,
    style,
)

def plot_energy(dictionary:dict, 
                PLOT:bool=False,
                speed:int=0,
                base_station_range:int=2000,
                language:str="en"):
    
    plt.figure(figsize=(14, 10))

    x_axis = [ x*10 
              for x in dictionary[list(dictionary.keys())[0]].keys() ]

    legends = legends_dicts[language]

    for server in dictionary.keys():
        
        means = []
        stds = []
        
        for err in dictionary[server].keys():
            
            means.append(mean(dictionary[server][err],axis=0))
            stds.append(std(dictionary[server][err],axis=0))
        
        m = np.array([ 100*x for x in means ])
        s = np.array([ 100*x for x in stds ])

        plt.plot(x_axis,
                 m,
                 linewidth=3,
                 label=legends[server],
                 color=colors[server],
                 linestyle=style[server])

        plt.fill_between(x_axis,
                         m - s,
                         m + s,
                         color=colors[server],
                         alpha=0.2)


    if language == "en":        

        plt.xlabel("Clients' Error Rate (%)", fontsize=16)
        plt.ylabel("Training Efficiency (%)", fontsize=16)

    elif language == "pt":
        
        plt.xlabel("Taxa de Erro por Cliente (%)", fontsize=16)
        plt.ylabel("Eficiência de Treinamento (%)", fontsize=16)


    plt.xticks(x_axis, 
               [str(x) for x in x_axis])

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=16)
    
    figure_path = f"figures/speed{speed}/{base_station_range}"
    os.makedirs(figure_path, 
                exist_ok=True)

    plt.savefig(f"{figure_path}/training_efficiency_{language}.png",
                dpi=300,
                bbox_inches='tight')
    
    if PLOT:

        plt.show()


if __name__ == "__main__":
    
    cfg = load_config('config/config.yaml')
    
    speeds = cfg["simulation"]["speed"]["index"]
    base_station_range = cfg['simulation']['base_station']['range']
    
    for speed in speeds:

        with open(f"results/speed{speed}/{base_station_range}/energy","rb") as reader:
            
            dictionary = load(reader)

        plot_energy(dictionary,
                    base_station_range=base_station_range,
                    speed=speed)
