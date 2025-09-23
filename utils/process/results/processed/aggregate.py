from pickle import load, dump

file_path = "results/client_selection/speed2/"

servers = ["random",
           "m_fastest",
           "tofl_oracle",
           "tofl_estimator_dl",
           "tofl_estimator_m_fastest"]
        

sizes=[500]

datasets = [ i for i in range(10) ]

for size in sizes:
        
    for model in servers:

        for dataset in datasets:
            
            agg_results = []
            
            for n_clients in range(1,6):
            
                file = "model_"+model+\
                       "_size_"+str(size)+\
                       "_dataset_"+str(dataset)+\
                       "_n_clients_"+str(n_clients)
                try:
                    with open(file_path+file,"rb") as reader:
                        agg_results.append(load(reader))
                except:
                    print(file)
                
            file = "model_"+model+\
                   "_size_"+str(size)+\
                   "_dataset_"+str(dataset)
            
            with open(file_path+file,"wb") as writer:
                dump(agg_results, writer)
