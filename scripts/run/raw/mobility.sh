#!/bin/bash
export SUMO_HOME=/usr/share/sumo
export HOME=$HOME:$SUMO_HOME
export SUMO_MOBILITY_PATH=$PWD/mobility/raw
## Paths scripts
PWD_TOOL=/usr/share/sumo/tools
## Variables
NB_Cars=(5)
NB_Runs=(0 1 2 3 4 5 6 7 8 9 10)
NB_grid=2 ### for value of x grids will be x-1
carFM=Krauss ### Krauss, IDM, ACC
Simulation_duration=600


##m/sec 
declare -A speeds

#speeds[speed0]=3.638889 #13.1km/h
#speeds[speed1]=8.333333 #30km/h
speeds[speed2]=13.88889 #50km/h

for (( run=0; run<${#NB_Runs[@]}; run++ ))
do
        for key in "${!speeds[@]}";
        do
                PWD_WORK=$SUMO_MOBILITY_PATH/scenarios/$key
		[ ! -d $PWD_WORK ] &&  mkdir -p $PWD_WORK
                topology_filename=$PWD_WORK/manhattan_net_$NB_grid.xml
		
		echo "PHASE 1 -> Generating the grid topology"
                #### To generate a manhattan network topology
                #netgenerate --grid --grid.number $NB_grid --grid.x-length 600 --grid.y-length 50 --default.lanenumber 1 --rand.max-distance 100.0 --default.speed ${speeds[$key]}  --no-turnarounds.geometry false -o $topology_filename
                netgenerate --grid --grid.number $NB_grid --grid.x-length 3000 --grid.y-length 3000 --default.lanenumber 1 --rand.max-distance 100.0 --default.speed ${speeds[$key]}  --no-turnarounds.geometry false -o $topology_filename
		sleep 1
                for (( i=0; i<${#NB_Cars[@]}; i++ ))
                do

                        # define the current directory 
                        current_directory=$PWD_WORK/$carFM/${NB_Cars[$i]}
                        mkdir -p $current_directory
                        echo "....... -> Copy netfile to the current directory "
                        cp $topology_filename $current_directory
                        echo "....... -> Generate continuous rerouters "
                        rerouter_filename=$current_directory/manhatan_rerouter_${carFM}_${NB_Cars[$i]}_$run.add.xml
                        $PWD_TOOL/generateContinuousRerouters.py -n $topology_filename -o $rerouter_filename
                        echo "....... -> Generating random flows for JTRROUTER "
                        flows_filename=$current_directory/flows_file_${carFM}_${NB_Cars[$i]}_$run.xml
			$PWD_TOOL/randomTrips.py -n $topology_filename -o $flows_filename --begin 0 --end 1 --random --seed $run --flows ${NB_Cars[$i]} --jtrrouter --trip-attributes 'departPos="random" departSpeed="max"'
                        echo "....... -> Run SUMO for configuration ${carFM} ${NB_Cars[$i]} cars / iteration $run"
                        sumo_trace_file="$current_directory/manhattan_${carFM}_${NB_Cars[$i]}_$run.xml"
                        sumo --default.carfollowmodel ${carFM} --net-file $topology_filename --route-files $flows_filename --additional-files $rerouter_filename --random --max-num-vehicles ${NB_Cars[$i]} --no-step-log --step-length 0.1 --begin 0 --end $Simulation_duration --no-warnings --fcd-output $sumo_trace_file
                        echo "....... -> Generate tr file for configuration ${NB_Cars[$i]} cars / iteration $run"
                        ns2traceFile=$current_directory/manhattan_${carFM}_${NB_Cars[$i]}_$run.tcl
                        $PWD_TOOL/traceExporter.py --fcd-input $sumo_trace_file --ns2mobility-output $ns2traceFile 
                done
        done
done

