import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_mean_and_std(n_executions):
    dataset_name = "executions/v2x_simulation_results"
    dataset_extension = ".csv"

    df = pd.read_csv(dataset_name+str(1)+dataset_extension)

    for execution in range(2,n_executions):
        df = pd.concat((df, pd.read_csv(dataset_name+str(execution)+dataset_extension)))


    df_mean = df.groupby(df.index).mean()
    df_std = df.groupby(df.index).std()

    return (df_mean,df_std)

mean = []
std = []

for n_execution in range(3,101):
    df_mean, df_std = generate_mean_and_std(n_execution)
    
    mean.append(df_mean['Throughput UL'][0])
    std.append(df_std['Throughput UL'][0])

print(mean)
print(std)

executions = [ index for index in range(2,len(mean)+2) ]
#error_interval = [-np.array(std),
#                  np.array(std)]

# Plot throughput
plt.figure(figsize=(12, 8))
plt.errorbar(executions, mean, yerr=std, capsize=3, fmt="r--o", ecolor = "black", label="throughputs_ul mean value")
plt.xlabel("Number of Executions (#)")
plt.ylabel("Throughput (Mb/s)")
plt.legend()
plt.show()