speeds=$(yq '.simulation.speed.index[]' "config/config.yaml")
base_station_range=$(yq '.simulation.base_station.range' "config/config.yaml")

for speed in $speeds; do 
	
	# verify if the estimator exists
	if [ ! -f "models/model_10_speed_"$speed"_range_"$base_station_range".pt" ]; then
		
		# train the estimator
		python -m utils.estimator.train
	fi
done

python -m src.main
