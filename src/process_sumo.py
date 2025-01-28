
n_nodes = 20
file_name = "mobility/raw/scenarios/speed0/Krauss/20/manhattan_Krauss_20_0.tcl"
processed_file = "mobility/processed/v2x_mobility_"+str(n_nodes)+".txt"
txt_writer = ""

with open(file_name, "r") as reader:
    current_nodes = 0
    start_process = False
    
    for line in reader:

        if current_nodes < n_nodes:
        
            if ") set Z_" in line:
                current_nodes += 1

        elif current_nodes == n_nodes and not start_process:
            time = float(line.split(' ')[2])
            start_process = True
        
        elif start_process:
            if float(line.split(' ')[2]) <= time:
                pass

            else:
                elements_list = line.split(' ')
                txt_writer += elements_list[2] + ' ' + \
                              elements_list[3][elements_list[3].find('(')+1:elements_list[3].find(')')] + ' ' + \
                              elements_list[5] + ' ' + \
                              elements_list[6] + ' ' + \
                              elements_list[7][:-2] + "\n"
                
with open(processed_file, "w") as writer:
    writer.writelines(txt_writer)