from pickle import load, dump

file_path = "results/client_selection/speed0/"

servers = ["random",
           "m_fastest",
           "tofl_oracle",
           "tofl_estimator_dl"]
        

sizes=[500,
       1000,
       2000,
       3000]

datasets = [ i for i in range(2) ]

for model in servers:

    for size in sizes:

        for dataset in datasets:
            
            agg_results = []
            
            for n_clients in range(1,11):
            
                file = "model_"+model+\
                       "_size_"+str(size)+\
                       "_dataset_"+str(dataset)+\
                       "_n_clients_"+str(n_clients)

                with open(file_path+file,"rb") as reader:
                    agg_results.append(load(reader))
                
            file = "model_"+model+\
                   "_size_"+str(size)+\
                   "_dataset_"+str(dataset)+"teste"

            with open(file_path+file,"wb") as writer:
                dump(agg_results, writer)
