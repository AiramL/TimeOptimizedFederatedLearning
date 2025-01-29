import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir

def plot_fig(mean, std):
    # Plot throughput
    plt.figure(figsize=(12, 8))
    plt.errorbar(executions, mean, yerr=std, capsize=3, fmt="r--o", ecolor = "black", label="throughputs_ul mean value")
    plt.xlabel("Number of Executions (#)")
    plt.ylabel("Throughput (Mb/s)")
    plt.legend()
    plt.show()


def generate_mean_and_std(n_executions=30,origin="mobility_0_"):
    dataset_name = "data/raw/"+origin+"_v2x_simulation_"
    dataset_extension = ".csv"

    df = pd.read_csv(dataset_name+str(0)+dataset_extension)

    for execution in range(n_executions):
        df = pd.concat((df, pd.read_csv(dataset_name+
                                        str(execution)+
                                        dataset_extension)))


    df_mean = df.groupby(df.index).mean()
    df_std = df.groupby(df.index).std()

    return (df_mean,df_std)



# for origin in listdir("mobility/processed/"):
#     df_mean, df_std = generate_mean_and_std(30,origin=origin[:-4])
#     file_path =  "data/processed/"
#     file_name = file_path+origin[:-4]+"_mean.csv"
#     df_mean.to_csv(file_name)

#for origin in listdir("mobility/processed/"):
for index in range(10):
    
    df_mean, df_std = generate_mean_and_std(30,origin="mobility_"+str(index))
    file_path =  "data/processed/"
    file_name = file_path+str(index)+".csv"
    df_mean.to_csv(file_name)


    