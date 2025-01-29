
[ ! -d "../data/processed" ] && ./create_paths.sh

[ ! -f "../mobility/raw/scenarios/speed0/Krauss/100/manhattan_Krauss_100_0.tcl" ] && ./generate_trips.sh 

cd ..

python src/process_sumo.py

python src/communication_delays.py

python src/process_throughput.py

python src/main.py

